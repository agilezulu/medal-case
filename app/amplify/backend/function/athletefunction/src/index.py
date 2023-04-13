"""
Main API interface for events
"""
import awsgi
import os
from datetime import timedelta, datetime
from flask_cors import CORS
from pony.flask import Pony
from pony import orm
from flask import Flask, jsonify, request, Response, abort
from resources.medalcase import MedalCase
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from resources.db.models import *

app = Flask(__name__)
app.config["STRAVA_VERIFY_TOKEN"] = os.getenv("STRAVA_VERIFY_TOKEN")
app.config["JWT_SECRET_KEY"] = os.getenv("STRAVA_STREAKS_JWT_SECRET")
app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
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
        'db': 'medalcase',
        'charset': 'utf8mb4'
    }
))

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=False)

Pony(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

BASE_PATH = '/athlete'


def make_response(data, tojson=True):
    """
    Add headers to responses
    :param data:
    :param tojson: boolean to json or text data
    :return:
    """
    if tojson:
        response = jsonify(data)
    else:
        response = Response(response=data)

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'OPTIONS,POST,GET')
    return response


@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()


@app.route(f'{BASE_PATH}/login', methods=['POST'])
def athlete_login():
    """
    Login to streaks with strava tokens
    :param athlete_slug:
    :return: streaks
    """
    mcase = MedalCase()
    code = request.json.get('code', None)
    data = mcase.user_login(code)

    # set JWT expires to
    access_token = create_access_token(
        identity=data['user']['id'],
        additional_claims={
            'firstname': data['user']['firstname'],
            'lastname': data['user']['lastname']
        }
    )
    data['user'].pop('id')
    return make_response({
        "access_token": access_token,
        "user": data['user']
    })


@app.route(f'{BASE_PATH}/list', methods=['GET'])
def get_athlete_list():
    """
    Primary streaks builder to create new or rebuild all
    :return: streaks
    """
    mcase = MedalCase()
    athletes = mcase.get_athletes()

    return make_response(athletes)


@app.route(f'{BASE_PATH}', methods=['GET'])
@jwt_required()
def update_athlete_runs():
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id=mcase_id)
    runs = mcase.update_athlete_medalcase(mcase_id)

    return make_response(runs)


@app.route(f'{BASE_PATH}/<slug>', methods=['GET'])
def get_athete_by_slug(slug):
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    mcase = MedalCase()
    athlete = mcase.get_athlete_by_slug(slug)

    return make_response(athlete.to_dict())


def handler(event, context):
    """
    default lambda handler
    :param event:
    :param context:
    :return:
    """
    return awsgi.response(app, event, context)


if __name__ == '__main__':
    orm.sql_debug(True)
    app.run(debug=True, host='127.0.0.1', port=5180)
