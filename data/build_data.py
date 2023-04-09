import signal
import argparse
import json
import os
import requests
import time
import math
from stravalib.client import Client

CWD = os.getcwd()


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)


class StravaRuns:
    """
        Strava runs interface class
    """

    def __init__(self, athlete_id=None):

        self.data_src = "."
        self.app_data_src = "../app/public/data"
        self.token_file = f"strava_token.json"
        self.runs_src = f"runs.json"
        self.summary_file = f"runs_summary.json"
        self.client_id = "39073"
        self.client_secret = "2030883d7ee2525d1f9ea4f5d800c7a0200798a0"
        self.redirect_uri = "http://localhost/"
        self.google_maps_apikey = 'AIzaSyCuM9OTZ0fZYpAV9_04l6uXaNYV6p6jKsM'
        self.token = None
        self.athlete_id = athlete_id

        self.url_athlete = "https://www.strava.com/api/v3/athlete"
        self.url_activities = "https://www.strava.com/api/v3/athlete/activities?page={0}&per_page=60"
        self.url_activity = "https://www.strava.com/api/v3/activities/{0}?include_all_efforts=false"
        self.url_activity_photos = "https://www.strava.com/api/v3/activities/{0}/photos?size=1200"
        self.url_activity_thumbnails = "https://www.strava.com/api/v3/activities/{0}/photos?size=300"

    def request_token(self, code):
        return requests.post(
            url='https://www.strava.com/oauth/token',
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'grant_type': 'authorization_code'
            }
        )

    def refresh_token(self, refresh_token):
        return requests.post(
            url='https://www.strava.com/api/v3/oauth/token',
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
        )

    def get_access_token(self):
        if not self.token:
            strava_token = self.get_token()
            self.token = strava_token['access_token']
        return self.token

    def get_auth_header(self):
        access_token = self.get_access_token()
        return {'Authorization': f"Bearer {access_token}"}

    def athlete_filename(self, filetype='token'):
        if not self.athlete_id:
            self.athlete_id = input("Enter your Strava athlete id: ")

        file = self.token_file
        src = self.data_src
        if filetype == 'cache':
            file = self.runs_src
        elif filetype == 'summary':
            file = self.summary_file
            src = self.app_data_src

        return f"{src}/{self.athlete_id}_{file}"

    def get_token(self):

        if not os.path.exists(self.athlete_filename()):
            request_url = f'http://www.strava.com/oauth/authorize?client_id={self.client_id}' \
                          f'&response_type=code&redirect_uri={self.redirect_uri}' \
                          f'&approval_prompt=force' \
                          f'&scope=profile:read_all,activity:read_all'

            print('Click here:', request_url)
            print('Please authorize the app and copy&paste below the generated code!')
            print('P.S: you can find the code in the URL')
            code = input('Insert the code from the url: ')

            token = self.request_token(code)

            #Save json response as a variable
            strava_token = token.json()
            self.athlete_id = strava_token['athlete']['id']
            # Save tokens to file
            self.save_json_file(self.athlete_filename(), strava_token)

        else:
            strava_token = self.get_json_file(self.athlete_filename())

        if strava_token['expires_at'] < time.time():
            print('Refreshing token!')
            new_token = strava.refresh_token(strava_token['refresh_token'])
            strava_token = new_token.json()
            # Update the file
            strava.save_json_file(self.athlete_filename(), strava_token)

        return strava_token

    def get_json_file(self, file):
        print(f"get file: {file}")
        with open(file, 'r') as data:
            return json.load(data)

    def save_json_file(self, file, data):
        with open(file, 'w') as outfile:
            json.dump(data, outfile, indent=2)

    def get_activities(self, after=None, before=None):
        """
        Get list of activities
        :param after:
        :param before:
        :return:
        """
        strava = Client(access_token=self.get_access_token())
        activities = strava.get_activities(after=after, before=before)
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
        self.save_json_file(self.athlete_filename(filetype='cache'), acts)

    @staticmethod
    def meters_to_miles(meters):
        return meters * 0.000621371

    def build_summary(self):
        """
        Summarise all runs
        :return:
        """
        activities = self.get_json_file(self.athlete_filename(filetype='cache'))
        summary = {
            "totals": {
              "runs": 0,
              "distance": 0,
              "time": 0
            },
            "by_mile": {},
            "classes": {
                "half": {
                    "tot": 0,
                    "runs": []
                },
                "marathon": {
                    "tot": 0,
                    "runs": []
                },
                "ultra": {
                    "tot": 0,
                    "subclass": {},
                    "runs": []
                }
            }
        }
        subclasses = [
            {
                "min": 110,
                "max": 1000,
                "name": "Extreme"
            },
            {
                "min": 100,
                "max": 110,
                "name": "100mi"
            },
            {
                "min": 60,
                "max": 70,
                "name": "100k"
            },
            {
                "min": 50,
                "max": 60,
                "name": "50mi"
            },
            {
                "min": 30,
                "max": 50,
                "name": "50k"
            }
        ]
        for act in activities:

            if act["type"] != "Run":
                continue

            mi = math.floor(self.meters_to_miles(act['distance']))

            summary["totals"]["runs"] += 1
            summary["totals"]["distance"] += act["distance"]
            summary["totals"]["time"] += act["elapsed_time"]

            meta = {
                "id": act["id"],
                "name": act["name"],
                "distance": act["distance"],
                "moving_time": act["moving_time"],
                "elapsed_time": act["elapsed_time"],
                "total_elevation_gain": act["total_elevation_gain"],
                "type": act["type"],
                "start_date": act["start_date"],
                "start_date_local": act["start_date_local"],
                "average_heartrate": act["average_heartrate"],
                "average_cadence": act["average_cadence"],
                "race": act["workout_type"] == 1,
            }

            mi_round = f"{mi}"

            if 13 <= mi < 14:
                summary["classes"]["half"]["tot"] += 1
                summary["classes"]["half"]["runs"].append(meta)
            elif 26 <= mi < 30:
                summary["classes"]["marathon"]["tot"] += 1
                summary["classes"]["marathon"]["runs"].append(meta)
            elif mi >= 30:

                for subclass in subclasses:
                    if subclass["max"] > mi >= subclass["min"]:
                        subclass_name = subclass["name"]
                        print(mi, subclass_name)
                        if subclass_name not in summary["classes"]["ultra"]["subclass"]:
                            summary["classes"]["ultra"]["subclass"][subclass_name] = 0
                        summary["classes"]["ultra"]["subclass"][subclass_name] += 1
                        meta["subclass"] = subclass_name

                summary["classes"]["ultra"]["tot"] += 1
                summary["classes"]["ultra"]["runs"].append(meta)

            if mi_round not in summary["by_mile"]:
                summary["by_mile"][mi_round] = 0
            summary["by_mile"][mi_round] += 1

        self.save_json_file(self.athlete_filename(filetype='summary'), summary)

    def get_activity(self, activity_id):
        """
        Get an activity
        """
        print(f"getting act: {activity_id}")
        act = requests.get(self.url_activity.format(activity_id), headers=self.get_auth_header())
        data = act.json()
        return data

    def get_strava_url(self, url):
        """
        Get a url from strava
        :param url:
        :return:
        """
        response = requests.get(url, headers=self.get_auth_header())
        return response.json()

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':

    CWD = os.getcwd()

    parser = argparse.ArgumentParser(description='Call Strava optionally')
    parser.add_argument('-s', '--strava', type=str2bool, nargs='?', const=False, default=False, help='get new data from the DB')

    args = parser.parse_args()

    strava = StravaRuns(athlete_id=16055914)

    strava.get_activities()
    #strava.build_summary()
