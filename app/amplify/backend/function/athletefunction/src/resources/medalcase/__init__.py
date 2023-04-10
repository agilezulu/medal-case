"""
    Interface class for accessing Evessio data via the API
"""
import json
import uuid
import os
import time
import copy
from pony import orm
from datetime import datetime, date
from flask import current_app as app, abort
from resources.strava import Strava
from resources.db.models import Athlete, Run


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
            - create if does not exist
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
        #print("ACCESS", user)
        return self.get_or_create_athlete(user)

    @staticmethod
    def update_user_tokens(strava_id, tokens, athlete_model=None):
        """
        tokens = {
            'access_token': user['access_creds']['access_token'],
            'refresh_token': user['access_creds']['refresh_token'],
            'expires_at': user['access_creds']['expires_at']
        }

        :param strava_id: int for athlete id
        :param tokens: dict of new tokens
        :param athlete_model: optional model
        :return:
        """
        with orm.db_session:
            if not athlete_model:
                try:
                    athlete_model = Athlete.get(strava_id=strava_id)
                except orm.ObjectNotFound:
                    abort(404, description=f"Error: Cannot locate athlete")

            # update tokens from client side Strava login
            athlete_model.set(**tokens)

    def get_or_create_athlete(self, user):
        """
            ATHLETE#s-16055914
            NAME#paul~schnell
        :param user: logged in strava user - user = Strava API results for user
        :return:
        """

        # get existing user from strava
        strava_id = user['athlete'].id

        tokens = {
            'access_token': user['access_creds']['access_token'],
            'refresh_token': user['access_creds']['refresh_token'],
            'expires_at': user['access_creds']['expires_at']
        }
        with orm.db_session:

            athlete = Athlete.get(strava_id=strava_id)
            if athlete:
                print('ATHLETE=', strava_id, athlete)
                self.update_user_tokens(strava_id, tokens, athlete_model=athlete)

            else:
                # create if not exists
                created_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                print('UNITS', user['athlete'].measurement_preference)
                units = 'mi' if user['athlete'].measurement_preference == 'feet' else 'km'
                new_athelete = {
                    'uuid': str(uuid.uuid4()),
                    'strava_id': strava_id,
                    'slug': f's-{strava_id}',
                    'firstname': user['athlete'].firstname,
                    'lastname': user['athlete'].lastname,
                    'units': units,
                    'country': user['athlete'].country,
                    'city': user['athlete'].city,
                    'sex': user['athlete'].sex,
                    'date_fmt': user['athlete'].date_preference,
                    'photo_m': user['athlete'].profile_medium,
                    'photo_l': user['athlete'].profile,

                    'access_token': user['access_creds']['access_token'],
                    'refresh_token': user['access_creds']['refresh_token'],
                    'expires_at': user['access_creds']['expires_at'],
                    'created_at': created_at
                }

                athlete = Athlete(**new_athelete)
                athlete.flush()

            return {
                "user": {
                    "id": athlete.id,
                    "firstname": athlete.firstname,
                    "lastname": athlete.lastname,
                    "country": athlete.country,
                    "city": athlete.city,
                    "units": athlete.units,
                    "date_fmt": athlete.date_fmt,
                    "sex": athlete.sex,
                },
                "tokens": {
                    'access_token': user['access_creds']['access_token'],
                    'refresh_token': user['access_creds']['refresh_token'],
                    'expires_at': user['access_creds']['expires_at']
                }
            }

    def get_athletes(self):
        """
        Get all athletes summary
        :return:
        """
        with orm.db_session:
            return [
                {

                    "c_100k": a.c_100k,
                    "c_100k_race": a.c_100k_race,
                    "c_100mi": a.c_100mi,
                    "c_100mi_race": a.c_100mi_race,
                    "c_50k": a.c_50k,
                    "c_50k_race": a.c_50k_race,
                    "c_50mi": a.c_50mi,
                    "c_50mi_race": a.c_50mi_race,
                    "c_extreme": a.c_extreme,
                    "c_extreme_race": a.c_extreme_race,
                    "c_marathon": a.c_marathon,
                    "c_marathon_race": a.c_marathon_race,
                    "city": a.city,
                    "country": a.country,
                    "firstname": a.firstname,
                    "last_run_date": a.c_100k,
                    "lastname": a.lastname,
                    "photo_m": a.photo_m,
                    "sex": a.sex,
                    "slug": a.slug,
                    "uuid": a.uuid
                }
                    for a in Athlete.select().order_by(orm.desc(Athlete.total_runs))
            ]
