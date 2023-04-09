"""
    Interface class for accessing Evessio data via the API
"""
import json
import uuid
import os
import time
import copy

from datetime import datetime, date
from flask import current_app as app, abort
from resources.strava import Strava


class MedalCase:
    """
    Class for admin tasks - inherited by:
    """
    def __init__(self, athlete_id=None):

        self.athlete_attributes = [
            "pk", "sk", "athlete", "startDate", "endDate", "athleteSlug", "provider", "providerId", "meta"
        ]
        self.valid_types = ["Run"]  # use only these activity types for streak
        self.athlete_id = athlete_id
        self.cache = f"{os.getcwd()}/{self.athlete_id}_CACHE.json"
        self.use_cache = True

        if athlete_id:
            tokens = self.get_tokens()
            if tokens['expires_at'] < time.time():
                tokens = Strava().refresh_tokens(tokens['refresh_token'])
                self.update_user_tokens(self.athlete_id, tokens)

            self.strava = Strava(access_token=tokens['access_token'])
        else:
            self.strava = Strava()

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return str(obj)

    def save_cache(self, data, file=None):
        cache_file = file or self.cache
        with open(cache_file, 'w') as out:
            out.write(json.dumps(data, sort_keys=True, indent=4, default=self.json_serial))

    def get_cache(self):
        with open(self.cache, 'r') as f:
            return json.load(f)

    def get_tokens(self):
        """
        Get from ddb if exists
        :return:
        """

        try:
            aiter = Athlete.query(
                Athlete.get_pk(self.athlete_id),
                filter_condition=(Athlete.recordType == 'athlete'),
                attributes_to_get=['tokens']
            )
            athelete = next(aiter, None)
            if not athelete:
                abort(404, description=f"Error: missing data")
            athlete_data = athelete.to_dict()
            return athlete_data['tokens']

        except Athlete.DoesNotExist as noex:
            print('NO TOKENS')
            return None

    def get_user(self, athlete_id):
        """
        Get from ddb if exists
        :param athlete_id:
        :return:
        """

        try:
            return Athlete.gsiAthlete.query(
                    Athlete.get_pk(athlete_id),
                    filter_condition=Athlete.recordType == 'athlete',
                    attributes_to_get=self.athlete_attributes
                )

        except Athlete.DoesNotExist as noex:
            return None

    def user_login(self, code):
        """
        Log a user into streaks
            - create if does ot exist
            - set tokens
            - set athele info
        :param code:
        :return: JWT
        """
        if not code:
            print('NO CODE')
            return {"error": "Missing Strava code"}

        # expect Strava Code
        user = self.strava.auth(code)

        print("ACCESS", user)
        '''
        {
            'athlete': <Athlete>{
                "id": 1234567890987654400,
                "username": "marianne_t",
                "resource_state": 3,
                "firstname": "Marianne",
                "lastname": "Teutenberg",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
                "sex": "F",
                "premium": true,
                "created_at": "2017-11-14T02:30:05Z",
                "updated_at": "2018-02-06T19:32:20Z",
                "badge_type_id": 4,
                "profile_medium": "https://xxxxxx.cloudfront.net/pictures/athletes/123456789/123456789/2/medium.jpg",
                "profile": "https://xxxxx.cloudfront.net/pictures/athletes/123456789/123456789/2/large.jpg",
                "friend": null,
                "follower": null,
                "follower_count": 5,
                "friend_count": 5,
                "mutual_friend_count": 0,
                "athlete_type": 1,
                "date_preference": "%m/%d/%Y",
                "measurement_preference": "feet",
                "clubs": [],
                "ftp": null,
                "weight": 0,
                "bikes": [
                {
                  "id": "b12345678987655",
                  "primary": true,
                  "name": "EMC",
                  "resource_state": 2,
                  "distance": 0
                }
                ],
                "shoes": [
                {
                  "id": "g12345678987655",
                  "primary": true,
                  "name": "adidas",
                  "resource_state": 2,
                  "distance": 4904
                }
                ]
            }, 
            'access_creds': {
                'access_token': 'e4d0c4b65d31a429fc54203679fdcc68fb3f40bd', 
                'refresh_token': '0714c57ed8a713ffe26c551cf8581931819a76dc', 
                'expires_at': 1665406226
            }
        }
        '''
        return self.get_or_create_athlete(user)

    @staticmethod
    def update_user_tokens(athlete_id, tokens, athlete_model=None):
        """
        tokens = {
            'access_token': user['access_creds']['access_token'],
            'refresh_token': user['access_creds']['refresh_token'],
            'expires_at': user['access_creds']['expires_at']
        }

        :param athlete_id: int for athlete id
        :param tokens: dict of new tokens
        :param athlete_model: optional model
        :return:
        """
        if not athlete_model:
            a_ddb = Athlete()
            pk_athlete = a_ddb.get_pk(athlete_id)

            athlete_model = list(a_ddb.query(
                pk_athlete,
                filter_condition=(Athlete.recordType == 'athlete')))[0]
            if not athlete_model:
                abort(404, description=f"Error: Cannot locate athlete")

        # update tokens from client side Strava login
        athlete_model.update(actions=[
            Athlete.tokens.set(tokens),
        ])

    def get_or_create_athlete(self, user):
        """
            ATHLETE#s-16055914
            NAME#paul~schnell
        :param user: logged in strava user - user = Strava API results for user
        :return:
        """
        provider = 'Strava'

        # get existing user from strava
        athlete_id = user['athlete'].id

        a_ddb = Athlete()
        pk_athlete = a_ddb.get_pk(athlete_id)
        sk_athlete = a_ddb.get_sk(user['athlete'].firstname, user['athlete'].lastname)
        tokens = {
            'access_token': user['access_creds']['access_token'],
            'refresh_token': user['access_creds']['refresh_token'],
            'expires_at': user['access_creds']['expires_at']
        }
        try:
            athlete_model = a_ddb.get(pk_athlete, sk_athlete)
            self.update_user_tokens(athlete_id, tokens, athlete_model=athlete_model)

        except Athlete.DoesNotExist as noex:
            # create if not exists
            created_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            new_athelete = {
                'athleteId': athlete_id,
                'athlete': {
                    'uuid': str(uuid.uuid4()),
                    'id': user['athlete'].id,
                    'slug': athlete_id,
                    'firstName': user['athlete'].firstname,
                    'lastName': user['athlete'].lastname,
                    'country': user['athlete'].country,
                    'city': user['athlete'].city,
                    'gender': user['athlete'].sex,
                    'dateFmt': user['athlete'].date_preference,
                    'profileMedium': user['athlete'].profile_medium,
                    'profileLarge': user['athlete'].profile,
                    'units': user['athlete'].measurement_preference,
                    'emoji': ''
                },
                'tokens': tokens,
                'subscription': {},
                'athleteSlug': athlete_id,
                'providerId': app.config["PROVIDERS"][provider]['id'],
                'provider': provider,
                'recordType': 'athlete',
                'createdAt': created_at
            }

            athlete_model = Athlete(pk_athlete, sk_athlete, **new_athelete)
        athlete_model.save()

        return {
            "user": {
                "athleteId": athlete_model.athlete.id,
                "firstName": athlete_model.athlete.firstName,
                "lastName": athlete_model.athlete.lastName,
                "city": athlete_model.athlete.city,
                "country": athlete_model.athlete.country,
                "units": athlete_model.athlete.units,
                "dateFmt": athlete_model.athlete.dateFmt,
                "gender": athlete_model.athlete.gender,
            },
            "tokens": {
                'access_token': user['access_creds']['access_token'],
                'refresh_token': user['access_creds']['refresh_token'],
                'expires_at': user['access_creds']['expires_at']
            }
        }


    def get_history(self):
        """
        Get all actis summarised
        :return:
        """
        all_acts = self.get_cache()
        summary = {}
