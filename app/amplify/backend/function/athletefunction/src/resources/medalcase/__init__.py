"""
    Interface class for accessing Evessio data via the API
"""
import uuid
import time
import json
from bisect import bisect_right
from pony import orm
from datetime import datetime, date
from geopy.geocoders import GoogleV3
from flask import current_app as app, abort
from resources.strava import Strava
from resources.db.models import Athlete, Run, RunClass


class MedalCase:
    """
    Class for admin tasks - inherited by:
    """
    def __init__(self, mcase_id=None):
        self.valid_types = ["Run"]  # use only these activity types for streak
        self.mcase_id = mcase_id
        self.class_bins = None
        self.run_classes = []

        if mcase_id:
            tokens = self.get_tokens(mcase_id)
            self.strava = Strava(access_token=tokens['access_token'])
        else:
            self.strava = Strava()

    @staticmethod
    def meters_to_miles(meters):
        return int(meters * 0.000621371)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return str(obj)

    def get_tokens(self, mcase_id):
        """
        :param mcase_id: medalcase.id
        :return" tokens dict
        """
        athlete = Athlete[mcase_id]
        if athlete:
            if athlete.expires_at < time.time():
                tokens = Strava().refresh_tokens(athlete.refresh_token)
                self.update_user_tokens(mcase_id, tokens, athlete_model=athlete)

            return {
                "access_token": athlete.access_token,
                "refresh_token": athlete.refresh_token,
                "expires_at": athlete.expires_at,
            }

        else:
            print('NO TOKENS')
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
        return self.get_or_create_athlete(user)

    def update_user_tokens(self, mcase_id, tokens, athlete_model=None):
        """
        tokens = {
            'access_token': user['access_creds']['access_token'],
            'refresh_token': user['access_creds']['refresh_token'],
            'expires_at': user['access_creds']['expires_at']
        }

        :param mcase_id: int for medalcase.id
        :param tokens: dict of new tokens
        :param athlete_model: optional model
        :return:
        """
        with orm.db_session:
            if not athlete_model:
                athlete_model = self.get_athlete(mcase_id)

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
                self.update_user_tokens(athlete.id, tokens, athlete_model=athlete)

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

    def get_athlete_by_slug(self, slug):
        """
        Get from ddb if exists
        :param slug:
        :return:
        """
        with orm.db_session:
            athlete = Athlete.get(slug=slug)
            if athlete:
                return athlete
        abort(404, description=f"Error: Cannot locate athlete")

    def get_athlete(self, mcase_id):
        """
        Get from ddb if exists
        :param mcase_id:
        :return:
        """
        try:
            return Athlete[mcase_id]
        except orm.ObjectNotFound:
            abort(404, description=f"Error: Cannot locate athlete")

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

    def get_strava_activities(self, after=None):
        """
        Get list of activities
        :param after:
        :param before:
        :return:
        """

        activities = self.strava.get_activities(after=after)
        acts = []
        drop_keys = [
            "segment_efforts", "laps", "similar_activities", "splits_metric",
            "splits_standard", "best_efforts", "stats_visibility", "athlete"
        ]
        for activity in activities:
            act = activity.to_dict()
            for key in drop_keys:
                act.pop(key, None)
            acts.append(act)
        return acts

    def update_athlete_totals(self, athlete):
        """

        """
        counts = orm.select(
            (r.run_class.key, orm.count(r.run_class))
            for r in athlete.runs
        )
        print(counts[:])

    def get_start_location(self, lat_lng):
        """
        Get country and city of start
        """
        geolocator = GoogleV3(api_key=app.config["GOOGLE_API_KEY"])
        location = geolocator.reverse(lat_lng)
        data = {
            'country': 'Unknown',
            'city': 'Unknown'
        }
        if location:
            #print(json.dumps(location.raw['address_components'], indent=4))
            for field in location.raw['address_components']:
                if 'postal_town' in field['types'] or 'locality' in field['types']:
                    data['city'] = field['long_name']
                if 'country' in field['types']:
                    data['country'] = field['long_name']

        return data

    def get_run_class(self, dist_mi):
        """
            get the run class base on the distance
        """
        if not self.class_bins:
            self.run_classes = list(RunClass.select().order_by(RunClass.min))
            self.class_bins = [c.min for c in self.run_classes]

        bin_idx = bisect_right(self.class_bins, dist_mi) - 1
        return self.run_classes[bin_idx]

    def update_athlete_medalcase(self, mcase_id):
        """
        Update an athlete's runs since their last run or build all for the first time
        """

        athlete = self.get_athlete(mcase_id)
        self.update_athlete_totals(athlete)
        last_run_date = athlete.last_run_date

        with orm.db_session:
            min_medal_dist = min(c.min for c in RunClass.select())
            for activity in self.strava.get_activities(after=athlete.last_run_date):
                act = activity.to_dict()
                dist_mi = self.meters_to_miles(activity.distance)
                if activity.type in self.valid_types and dist_mi >= min_medal_dist:
                    run_class = self.get_run_class(dist_mi)
                    activity.start_date = activity.start_date.replace(tzinfo=None)
                    location = self.get_start_location(activity.start_latlng)
                    print(location)
                    run_params = {
                        "strava_id":  activity.id,
                        "name":  activity.name,
                        "distance":  activity.distance,
                        "moving_time":  act["moving_time"],
                        "elapsed_time":  act["elapsed_time"],
                        "total_elevation_gain":  activity.total_elevation_gain,
                        "start_date":  activity.start_date,
                        "start_date_local":  activity.start_date_local,
                        "utc_offset":  activity.utc_offset,
                        "timezone":  act["timezone"],
                        "start_latlng":  act["start_latlng"] or '',
                        "location_country":  location['country'],
                        "location_city":  location['city'],
                        "average_heartrate":  activity.average_heartrate,
                        "average_cadence":  activity.average_cadence,
                        "race": activity.workout_type == 1,
                        "summary_polyline":  activity.map.summary_polyline,
                        "athlete": athlete,
                        "run_class": run_class
                    }
                    run = Run[activity.id]
                    if run:
                        # if we already have the run just update some meta to allow for local editing
                        run.set(
                            name=run_params["name"],
                            location_country=location['country'],
                            location_city=location['location_city'],
                        )
                    else:
                        Run(**run_params)

                    # update athlete totals
                    if not last_run_date or activity.start_date > last_run_date:
                        last_run_date = activity.start_date

            athlete.last_run_date = last_run_date

            return {
                "athlete": athlete.to_dict(),
                "runs": [
                    {
                        "strava_id":  r.strava_id,
                        "name":  r.name,
                        "distance":  r.distance,
                        "moving_time":  r.moving_time,
                        "elapsed_time":  r.elapsed_time,
                        "total_elevation_gain":  r.total_elevation_gain,
                        "start_date":  r.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                        "start_date_local":  r.start_date_local.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "location_country":  r.location_country,
                        "race": r.race == 1,
                        "summary_polyline": r.run_class.name,
                        "class": r.run_class.name,
                        "class_key": r.run_class.key,
                        "class_parent": r.run_class.parent,
                    } for r in athlete.runs
                ]
            }
