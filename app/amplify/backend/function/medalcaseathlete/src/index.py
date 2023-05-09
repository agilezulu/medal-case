"""
Main API interface for events
"""
import awsgi
import os
import json
import boto3
import logging
from datetime import timedelta
from flask_cors import CORS
from pony.flask import Pony
from pony import orm
from flask import Flask, jsonify, request, Response, abort
#from flask_socketio import SocketIO, emit
from resources.medalcase import MedalCase
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, decode_token
from werkzeug.exceptions import HTTPException
from botocore.exceptions import ClientError

from resources.db.models import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.config["STRAVA_VERIFY_TOKEN"] = os.getenv("STRAVA_VERIFY_TOKEN")
app.config["JWT_SECRET_KEY"] = os.getenv("MEDALCASE_JWT_SECRET")
app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=31)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=62)

# medalcase-db.cluster-cwvvfqouydfr.eu-west-1.rds.amazonaws.com
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='695f9e55521448ffa250ae6b0e93785f',
    PONY={
        'provider': 'mysql',
        'host': os.getenv('DBHOST'),
        'port': int(os.getenv('DBPORT', 3306)),
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
# socketio = SocketIO(app, cors_allowed_origins="*")

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

'''
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print('SOCKET ERROR', e)
    pass


@socketio.on('connect')
@jwt_required()
def test_connect():
    mcase_id = get_jwt_identity()
    print('Client connected', mcase_id)
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('update')
@jwt_required()
@orm.db_session
def update_athlete_runs(message):
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: socket messages
    """

    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id=mcase_id)
    print('CAll update runs for:', mcase_id)
    athlete = mcase.update_athlete_medalcase(mcase_id)

    emit('athlete_update_complete', {'data': athlete})
'''


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
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
    # print('LOGIN - code', code)
    try:
        data = mcase.user_login(code)

        # print('LOGIN - data', data)
        # set JWT expires to
        access_token = create_access_token(
            identity=data["id"]
        )
        return make_response({
            "access_token": access_token,
            "slug": data["slug"],
            "firstname": data["firstname"],
            "lastname": data["lastname"],
            "units": data["units"]
        })
    except Exception as exp:
        abort(500, description=str(exp))


@app.route(f'{BASE_PATH}/list', methods=['GET'])
def get_athlete_list():
    """
    Primary streaks builder to create new or rebuild all
    :return: streaks
    """
    mcase = MedalCase()
    athletes = mcase.get_athletes()
    return make_response(athletes)


@app.route(f'{BASE_PATH}/<slug>', methods=['GET'])
def get_athete_by_slug(slug):
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    mcase = MedalCase()
    athlete = mcase.get_athlete(slug=slug)
    return make_response(athlete)


@app.route(f'{BASE_PATH}/run/<strava_id>', methods=['PUT'])
@jwt_required()
def update_athlete_run(strava_id):
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    data = request.json
    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id)
    athlete = mcase.update_run(mcase_id, strava_id, data)
    return make_response(athlete)


@app.route(f'{BASE_PATH}/run', methods=['DELETE'])
@jwt_required()
def delete_athlete_run():
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    data = request.json
    run_id = data.get('strava_id')
    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id)
    athlete = mcase.delete_run(mcase_id, run_id)
    return make_response(athlete)


@app.route(f'{BASE_PATH}/run/<strava_id>', methods=['PATCH'])
@jwt_required()
def resync_athlete_run(strava_id):
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id)
    athlete = mcase.resync_run_from_strava(mcase_id, strava_id)
    return make_response(athlete)


@app.route(f'{BASE_PATH}', methods=['DELETE'])
@jwt_required()
def delete_athlete():
    """
    Delete athlete and runs
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id)
    resp = mcase.delete_athlete(mcase_id)
    return make_response(resp)


def handle_connect(connection_id):
    """
    Handles new connections by adding the connection ID and mcase_id to Redis
    :param mcase_id: The name of the user that started the connection.
    :param connection_id: The websocket connection ID of the new connection.
    :return: An HTTP status code that indicates the result of adding the connection
             to the DynamoDB table.
    """
    status_code = 200
    logger.info(f"Added connection {connection_id} for user")
    return status_code


def handle_disconnect(connection_id):
    """
    Handles disconnections by removing the connection record from Redis
    :param connection_id: The websocket connection ID of the connection to remove.
    :return: An HTTP status code that indicates the result of removing the connection
             from the DynamoDB table.
    """
    status_code = 200
    logger.info("Disconnected connection %s.", connection_id)
    return status_code


@orm.db_session
def handle_build_runs(mcase_id, apig_management_client, connection_id):
    """
    Build runs ands sens updates back over socket
    :param mcase_id: Athlete id
    :param connection_id: The ID of the connection that sent the message.
    :param apig_management_client: A Boto3 API Gateway Management API client.

    :return: An HTTP status code
    """
    status_code = 200

    try:
        print('CAll update runs for:', mcase_id)
        mcase = MedalCase(mcase_id=mcase_id)
        mcase.update_athlete_medalcase(mcase_id, apig_management_client, connection_id)
    except ClientError:
        logger.exception("Couldn't post to connection %s.", connection_id)
    except apig_management_client.exceptions.GoneException:
        logger.info("Connection %s is gone, removing.", connection_id)

    return status_code


def handler(event, context):
    """
    default lambda handler
    :param event:
    :param context:
    :return:
    """
    #print('EVENT', event)
    connection_id = event.get('requestContext', {}).get('connectionId')
    """
    EVENT = {
        'requestContext': {
            'routeKey': '$default', 
            'messageId': 'Ei1Jse5yDoECE9w=', 
            'eventType': 'MESSAGE',
            'extendedRequestId': 'Ei1JsFS0DoEFt8g=', 
            'requestTime': '07/May/2023:09:00:20 +0000',
            'messageDirection': 'IN', 
            'stage': 'prod', 
            'connectedAt': 1683449962688,
            'requestTimeEpoch': 1683450020160,
            'identity': {
                'apiKey': 'YkxgqM5IVEae9AViOs7Jqa3ad98Jsgmn2TACafs5', 
                'apiKeyId': 'qnf4iywhr7',
                'sourceIp': '90.194.74.138'
            }, 'requestId': 'Ei1JsFS0DoEFt8g=',
            'domainName': '8vzirn1xee.execute-api.eu-west-1.amazonaws.com',
            'connectionId': 'Ei1AtejdjoECE9w=',
            'apiId': '8vzirn1xee'
        }, 
        'body': '{ "foo": "bar" }',
        'isBase64Encoded': False
    }
    """
    # handle websocket connections
    # ------------------------------
    if connection_id:

        domain = event.get('requestContext', {}).get('domainName')
        stage = event.get('requestContext', {}).get('stage')
        apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
        try:
            with app.app_context():
                route_key = event.get('requestContext', {}).get('routeKey')

                response = {'statusCode': 200}

                if domain is None or stage is None:
                    logger.warning(f"Couldn't send message: domain '{domain}',stage '{stage}'")
                    response['statusCode'] = 400
                    return response

                if route_key == '$connect':
                    response['statusCode'] = handle_connect(connection_id)
                elif route_key == '$disconnect':
                    response['statusCode'] = handle_disconnect(connection_id)
                else:
                    body = json.loads(event.get('body', {}))
                    jwt = body.get('jwt', None)
                    if not jwt:
                        logger.error("No jwt found in body")
                        response['statusCode'] = 404
                        return response

                    token = decode_token(jwt)
                    mcase_id = token.get('sub', None)
                    if not mcase_id:
                        print("No mcase_id")
                        response['statusCode'] = 404
                        return response

                    mcase_id = int(mcase_id)

                    handle_build_runs(mcase_id, apig_management_client, connection_id)
                    message = json.dumps({'action': 'status', 'value': 'COMPLETE'}).encode('utf-8')
                    apig_management_client.post_to_connection(Data=message, ConnectionId=connection_id)

                return response
        except Exception as exp:
            message = json.dumps({'action': 'error', 'value': str(exp)}).encode('utf-8')
            print('WSS error:', exp)
            apig_management_client.post_to_connection(Data=message, ConnectionId=connection_id)
            return {'statusCode': 500}

    # regular REST API calls
    # ------------------------------
    else:
        return awsgi.response(app, event, context)


if __name__ == '__main__':
    orm.sql_debug(True)
    # socketio.run(app, host='127.0.0.1', port=5180, debug=True)
    app.run(debug=True, host='127.0.0.1', port=5180)
