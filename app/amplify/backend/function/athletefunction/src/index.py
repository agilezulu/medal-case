"""
Main API interface for events
"""
import awsgi
import os
from datetime import timedelta, datetime
from flask_cors import CORS
from pony.orm import Database
from pony.flask import Pony
from flask import Flask, jsonify, request, Response, abort
from resources.medalcase import MedalCase
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["STRAVA_VERIFY_TOKEN"] = os.getenv("STRAVA_VERIFY_TOKEN")
app.config["JWT_SECRET_KEY"] = os.getenv("STRAVA_STREAKS_JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=31)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=62)

app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='695f9e55521448ffa250ae6b0e93785f',
    PONY={
        'provider': 'mysql',
        'host': '127.0.0.1',
        'port': 3307,
        'user': os.getenv('DBUSER'),
        'passwd': os.getenv('DBPWD'),
        'db': 'medalcase'
    }
))

db = Database()

db.bind(**app.config['PONY'])
# db.generate_mapping(create_tables=False)
db.generate_mapping(filename='models.py')


Pony(app)


jwt = JWTManager(app)
CORS(app, supports_credentials=True)


def make_response(data, tojson=True):
    """
    Add headers to responses
    :param data:
    :param tojson: boolean to json or text data
    :return:
    """
    '''
    if isinstance(data, list):
        for item in data:
            item.pop('pk', None)
            item.pop('sk', None)
    elif isinstance(data, dict):
        data.pop('pk', None)
        data.pop('sk', None)
    '''

    if tojson:
        response = jsonify(data)
    else:
        response = Response(response=data)

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    #response.headers.add('Access-Control-Allow-Methods', 'OPTIONS,POST,GET')
    return response


@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()


@app.route(f'/login', methods=['POST'])
def login():
    """
    Login to streaks with strava tokens
    :param athlete_slug:
    :return: streaks
    """
    streaks = StreaksAdmin()
    code = request.json.get('code', None)
    data = streaks.user_login(code)
    strava_expires = datetime.fromtimestamp(data['tokens']['expires_at'])
    now = datetime.now()
    diff = strava_expires - now
    # set JWT expires to
    access_token = create_access_token(
        identity=data['user']['athleteId'],
        additional_claims={
            'firstName': data['user']['firstName'],
            'lastName': data['user']['lastName']
        }
    )
    return make_response({
        "access_token": access_token,
        "user": data['user']
    })


@app.route('/athlete', methods=['GET'])
@jwt_required()
def get_athletes():
    """
    Primary streaks builder to create new or rebuild all
    :return: streaks
    """
    athlete_id = get_jwt_identity()
    mcase = MedalCase(athlete_id=athlete_id)
    athletes = mcase.get_athletes()

    return make_response(athletes)


def handler(event, context):
    """
    default lambda handler
    :param event:
    :param context:
    :return:
    """
    return awsgi.response(app, event, context)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5170)
