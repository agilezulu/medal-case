import os
import requests
import json
from stravalib.client import Client
from flask import abort


class Strava:

    def __init__(self, access_token=None):
        self.STRAVA_CLIENT_ID = int(os.getenv('STRAVA_STREAKS_CLIENT_ID'))
        self.STRAVA_CLIENT_SECRET = os.getenv('STRAVA_STREAKS_CLIENT_SECRET')
        self.STRAVA_AUTH_URL = os.getenv('STRAVA_AUTH_URL', 'http://localhost:5170/auth')

        if access_token:
            self.access_token = access_token
            self.client = Client(access_token=access_token)
        else:
            self.client = Client()

    def refresh_tokens(self, last_refresh_token):
        token_response = Client().refresh_access_token(
            client_id=self.STRAVA_CLIENT_ID,
            client_secret=self.STRAVA_CLIENT_SECRET,
            refresh_token=last_refresh_token
        )
        return token_response

    def auth(self, code):
        """
        Method called by Strava (redirect) that includes parameters.
        - state
        - code
        - error
        """
        #print(f"STRAVA => {self.STRAVA_CLIENT_ID} {code} << {self.STRAVA_CLIENT_SECRET}")

        access_creds = self.client.exchange_code_for_token(
            client_id=self.STRAVA_CLIENT_ID,
            client_secret=self.STRAVA_CLIENT_SECRET,
            code=code)

        '''
        access_creds = {
          "access_token": "b83a97faa0767e5caaf9...",
          "expires_at": 1661967666,
          "refresh_token": "5d5dd6699633d471d..."
        }
        '''
        # Probably here you'd want to store this somewhere -- e.g. in a database.
        strava_athlete = self.client.get_athlete()
        return {
            "athlete": strava_athlete,
            "access_creds": access_creds
        }

    def get_activities(self, after=None, before=None):
        """
        Get activites after give date or no date for all
        :param after:
        :param activity_ids: optional list of ids e.g. [123123,324234,567567]
        :return:
        """
        return self.client.get_activities(after=after, before=before)
