"""
    Interface class for accessing Evessio data via the API
"""
import uuid
import time
import json
from bisect import bisect_right
from pony import orm
from datetime import datetime, date, timezone
from geopy.geocoders import GoogleV3
from flask import current_app as app, abort
from stravalib import unithelper
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
                "slug": athlete.slug,
                "firstname": athlete.firstname,
                "lastname": athlete.lastname,
                "id": athlete.id,
                "tokens": {
                    'access_token': user['access_creds']['access_token'],
                    'refresh_token': user['access_creds']['refresh_token'],
                    'expires_at': user['access_creds']['expires_at']
                }
            }

    def _get_athlete_by_slug(self, slug):
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

    def _get_athlete_by_id(self, mcase_id):
        """
        Get from ddb if exists
        :param mcase_id:
        :return:
        """
        try:
            with orm.db_session:
                return Athlete[mcase_id]
        except orm.core.ObjectNotFound:
            abort(404, description=f"Error: Cannot locate athlete")

    @staticmethod
    def template_athlete(athlete):
        """
        Build athlete return structure
        :param athlete: 
        :return: 
        """
        last_run_date = athlete.last_run_date.strftime('%Y-%m-%dT%H:%M:%S') if athlete.last_run_date else ''
        return {
            "c_100k": athlete.c_100k,
            "c_100k_race": athlete.c_100k_race,
            "c_100mi": athlete.c_100mi,
            "c_100mi_race": athlete.c_100mi_race,
            "c_50k": athlete.c_50k,
            "c_50k_race": athlete.c_50k_race,
            "c_50mi": athlete.c_50mi,
            "c_50mi_race": athlete.c_50mi_race,
            "c_extreme": athlete.c_extreme,
            "c_extreme_race": athlete.c_extreme_race,
            "c_marathon": athlete.c_marathon,
            "c_marathon_race": athlete.c_marathon_race,
            "city": athlete.city,
            "country": athlete.country,
            "firstname": athlete.firstname,
            "last_run_date": last_run_date,
            "lastname": athlete.lastname,
            "photo": athlete.photo_l,
            "sex": athlete.sex,
            "slug": athlete.slug,
            "uuid": athlete.uuid,
            "total_distance": athlete.total_distance,
            "total_runs": athlete.total_runs,
            "total_medals": athlete.total_medals,
        }

    @staticmethod
    def template_run(run):
        """
        Run dict template
        :param run: 
        :return: 
        """
        return {
            "strava_id":  run.strava_id,
            "name":  run.name,
            "distance":  run.distance,
            "moving_time":  run.moving_time,
            "elapsed_time":  run.elapsed_time,
            "total_elevation_gain":  run.total_elevation_gain,
            "start_date":  run.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            "start_date_local":  run.start_date_local.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "location_country":  run.location_country,
            "race": run.race == 1,
            "summary_polyline": run.summary_polyline,
            "class": run.run_class.name,
            "class_key": run.run_class.key,
            "class_parent": run.run_class.parent,
        }

    def get_athletes(self):
        """
        Get all athletes summary
        :return:
        """
        with orm.db_session:
            return [
                self.template_athlete(a)
                    for a in Athlete.select(lambda p: p.last_run_date is not None and p.total_medals > 0).order_by(orm.desc(Athlete.total_runs))
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
        Update medal count totals
        """
        counts = orm.select(
            (r.run_class.key, orm.count(r.strava_id), orm.count(r.race == 1))
            for r in athlete.runs
        )
        total_medals = 0
        for class_key, run_count, race_count in counts:
            athlete.set(**{
                f"{class_key}": run_count,
                f"{class_key}_race": race_count,
            })
            total_medals += run_count
        athlete.set(total_medals=total_medals)

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
        :param dist_mi: distance in miles
        :return:
        """
        if not self.class_bins:
            self.run_classes = list(RunClass.select().order_by(RunClass.min))
            self.class_bins = [c.min for c in self.run_classes]

        bin_idx = bisect_right(self.class_bins, dist_mi) - 1
        return self.run_classes[bin_idx]

    def update_athlete_medalcase(self, mcase_id):
        """
        Update an athlete's runs since their last run or build all for the first time
        :param mcase_id:
        :return:
        """
        athlete = self._get_athlete_by_id(mcase_id)
        last_scanned_utc = athlete.last_run_date if athlete.last_run_date else None
        last_run_date_epoch = last_scanned_utc.timestamp() if last_scanned_utc else None
        last_run_date = None
        new_medals = {}
        scanned_runs = 0
        new_distance = 0
        after = last_scanned_utc if last_scanned_utc else datetime.strptime('2009-01-01T00:00:00', '%Y-%m-%dT%H:%M:%S')
        before = datetime.utcnow()
        with orm.db_session:
            min_medal_dist = min(c.min for c in RunClass.select())
            for activity in self.strava.get_activities(after=after, before=before):
                dist_mi = self.meters_to_miles(activity.distance)
                athlete.total_runs += 1
                if last_scanned_utc is None or last_scanned_utc < activity.start_date.replace(tzinfo=None):
                    last_scanned_utc = activity.start_date.replace(tzinfo=None)

                if activity.type in self.valid_types and dist_mi >= min_medal_dist:
                    act = activity.to_dict()
                    scanned_runs += 1
                    new_distance += int(unithelper.meters(activity.distance))
                    run_class = self.get_run_class(dist_mi)
                    #activity.start_date = activity.start_date.replace(tzinfo=timezone.utc)
                    activity_start_date_epoch = activity.start_date.timestamp()
                    location = self.get_start_location(activity.start_latlng)
                    print(activity.id, str(activity.start_date))
                    run_params = {
                        "strava_id":  activity.id,
                        "name":  activity.name,
                        "distance":  activity.distance,
                        "moving_time":  act["moving_time"],
                        "elapsed_time":  act["elapsed_time"],
                        "total_elevation_gain":  activity.total_elevation_gain,
                        "start_date":  activity.start_date.replace(tzinfo=None),
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
                    try:
                        run = Run[activity.id]
                        # if we already have the run just update some meta to allow for local editing
                        run.set(
                            name=run_params["name"],
                            location_country=location.get('country', 'Unknown'),
                            location_city=location.get('location_city', 'Unknown'),
                        )
                    except orm.core.ObjectNotFound:
                        if run_class.key not in new_medals:
                            new_medals[run_class.key] = 0
                        new_medals[run_class.key] += 1
                        Run(**run_params)

                    # update last checked run
                    if not last_run_date_epoch or activity_start_date_epoch > last_run_date_epoch:
                        last_run_date_epoch = activity_start_date_epoch
                        last_run_date = activity.start_date

            # update athlete totals
            existing_total = athlete.total_runs
            if athlete.total_runs is None:
                existing_total = 0
            athlete.set(
                last_run_date=last_run_date,
                total_runs=(existing_total + scanned_runs),
                total_distance=(athlete.total_distance + new_distance)
            )
            self.update_athlete_totals(athlete)
            athlete_data = self.get_athlete(athlete_model=athlete)
            athlete_data['meta'] = {
                'new_runs': new_medals,
                'scanned_runs': scanned_runs,
                'last_scan_date': last_scanned_utc.strftime('%Y-%m-%dT%H:%M:%S')
            }
            return athlete_data
    
    def get_athlete(self, mcase_id=None, slug=None, athlete_model=None):
        """
        Get an athele from DB
        :param mcase_id:
        :param slug:
        :param athlete_model:
        :return:
        """
        athlete = None
        if slug:
            athlete = self._get_athlete_by_slug(slug)
        elif mcase_id:
            athlete = self._get_athlete_by_id(mcase_id)
        elif athlete_model:
            athlete = athlete_model
        else:
            abort(404, description=f"Error: Cannot locate athlete")

        return {
            **self.template_athlete(athlete),
            "runs": [self.template_run(run) for run in athlete.runs]
        }

    def update_run(self, mcase_id, data):
        """
        Update an athlete run
        :param mcase_id:
        :param data:
        :return:
        """
        run_id = data.get('strava_id')
        run = Run[run_id]

        if run and run.athlete.id == mcase_id:
            run_class = RunClass.get(key=data.get("class_key"))
            with orm.db_session:
                run.set(
                    name=data.get("name"),
                    race=data.get("race"),
                    run_class=run_class
                )
            return self.get_athlete(mcase_id=mcase_id)
        abort(404, description=f"Error: Invalid access to update a run")