"""
Main API interface for events
"""
import awsgi
import os
import json
import boto3
import redis
import logging
from datetime import timedelta
from flask_cors import CORS
from pony.flask import Pony
from pony import orm
from flask import Flask, jsonify, request, Response
from resources.medalcase import MedalCase
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from resources.db.models import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_REGION = 'eu-west-1'
SQS_URL = 'https://sqs.eu-west-1.amazonaws.com/087685034478/medalcase.fifo'
REDIS_URL = 'medalcase-redis.yc3arn.ng.0001.euw1.cache.amazonaws.com'

r = redis.Redis(host=REDIS_URL, port=6379, decode_responses=True)

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
    print('LOGIN - code', code)
    data = mcase.user_login(code)

    print('LOGIN - data', data)
    # set JWT expires to
    access_token = create_access_token(
        identity=data["id"]
    )
    return make_response({
        "access_token": access_token,
        "slug": data["slug"],
        "firstname": data["firstname"],
        "lastname": data["lastname"],
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


@app.route(f'{BASE_PATH}', methods=['POST'])
@jwt_required()
def update_athlete_runs():
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id=mcase_id)
    # check if currently processing
    is_processing = mcase.check_athlete_processing(mcase_id)
    if is_processing:
        return make_response({
            "is_processing": True
        })

    # send message to SQS
    client = boto3.client('sqs', region_name=AWS_REGION)
    #queue_url = client.get_queue_url(QueueName='medalcase.fifo')
    response = client.send_message(
        QueueUrl=SQS_URL,
        MessageBody=str(mcase_id),
        MessageDeduplicationId=f's-{mcase_id}',
        MessageGroupId='MedalcaseAthleteProcess'
    )
    print('RESPONSE', response)

    # set athlete to processing
    mcase.set_athlete_processing(mcase_id, True)

    # return message id
    message_id = response.get('MessageId')
    return make_response({
        "is_processing": True,
        "message_id": message_id
    })


@app.route(f'{BASE_PATH}/check', methods=['GET'])
@jwt_required()
def check_athlete_processing():
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    msg_id = request.args.get('msg_id')
    mcase_id = get_jwt_identity()
    mcase = MedalCase(mcase_id=mcase_id)
    # check sqs message queue

    # check database to see if athlete complete
    is_processing = mcase.check_athlete_processing(mcase_id)
    if is_processing:
        return make_response({
            "is_processing": True
        })

    athlete = mcase.update_athlete_medalcase(mcase_id)
    return make_response({
        "is_processing": False,
        "athlete": athlete
    })


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


@app.route(f'{BASE_PATH}/run', methods=['PUT'])
@jwt_required()
def update_athlete_run():
    """
    Primary streaks builder to create new or rebuild all
    :param uuid: mcase athlete uuid
    :return: streaks
    """
    data = request.json

    mcase_id = get_jwt_identity()
    mcase = MedalCase()
    athlete = mcase.update_run(mcase_id, data)
    return make_response(athlete)


def handle_connect(mcase_id, connection_id):
    """
    Handles new connections by adding the connection ID and mcase_id to Redis
    :param mcase_id: The name of the user that started the connection.
    :param connection_id: The websocket connection ID of the new connection.
    :return: An HTTP status code that indicates the result of adding the connection
             to the DynamoDB table.
    """
    status_code = 200
    try:
        r.set(connection_id, str(mcase_id))
        logger.info(f"Added connection {connection_id} for user {mcase_id}")
    except Exception as exp:
        logger.exception(f"ERROR: {exp} // user {mcase_id}")
        status_code = 503
    return status_code


def handle_disconnect(connection_id):
    """
    Handles disconnections by removing the connection record from Redis
    :param connection_id: The websocket connection ID of the connection to remove.
    :return: An HTTP status code that indicates the result of removing the connection
             from the DynamoDB table.
    """
    status_code = 200
    try:
        r.delete(connection_id)
        logger.info("Disconnected connection %s.", connection_id)
    except Exception as exp:
        logger.exception(f"ERROR: {exp} // connection {connection_id}")
        status_code = 503
    return status_code

def handle_build_runs(connection_id, event_body, apig_management_client):
    """
    Handles messages sent by a participant in the chat. Looks up all connections
    currently tracked in the DynamoDB table, and uses the API Gateway Management API
    to post the message to each other connection.
    When posting to a connection results in a GoneException, the connection is
    considered disconnected and is removed from the table. This is necessary
    because disconnect messages are not always sent when a client disconnects.
    :param table: The DynamoDB connection table.
    :param connection_id: The ID of the connection that sent the message.
    :param event_body: The body of the message sent from API Gateway. This is a
                       dict with a `msg` field that contains the message to send.
    :param apig_management_client: A Boto3 API Gateway Management API client.
    :return: An HTTP status code that indicates the result of posting the message
             to all active connections.
    """
    status_code = 200
    user_name = 'guest'
    try:
        item_response = table.get_item(Key={'connection_id': connection_id})
        user_name = item_response['Item']['user_name']
        logger.info("Got user name %s.", user_name)
    except ClientError:
        logger.exception("Couldn't find user name. Using %s.", user_name)

    connection_ids = []
    try:
        scan_response = table.scan(ProjectionExpression='connection_id')
        connection_ids = [item['connection_id'] for item in scan_response['Items']]
        logger.info("Found %s active connections.", len(connection_ids))
    except ClientError:
        logger.exception("Couldn't get connections.")
        status_code = 404

    message = f"{user_name}: {event_body['msg']}".encode('utf-8')
    logger.info("Message: %s", message)

    for other_conn_id in connection_ids:
        try:
            if other_conn_id != connection_id:
                send_response = apig_management_client.post_to_connection(
                    Data=message, ConnectionId=other_conn_id)
                logger.info(
                    "Posted message to connection %s, got response %s.",
                    other_conn_id, send_response)
        except ClientError:
            logger.exception("Couldn't post to connection %s.", other_conn_id)
        except apig_management_client.exceptions.GoneException:
            logger.info("Connection %s is gone, removing.", other_conn_id)
            try:
                table.delete_item(Key={'connection_id': other_conn_id})
            except ClientError:
                logger.exception("Couldn't remove connection %s.", other_conn_id)

    return status_code


def handler(event, context):
    """
    default lambda handler
    :param event:
    :param context:
    :return:
    """
    print('EVENT', event)
    print('CONTEXT', context)
    connection_id = event.get('requestContext', {}).get('connectionId')
    route_key = event.get('requestContext', {}).get('routeKey')
    mcase_id = event.get('queryStringParameters', {}).get('mcase_id')
    # handle websocket connections
    #------------------------------
    if connection_id:
        '''
        event["httpMethod"] = "GET"
        event["path"] = "/athlete/list"
        event["queryStringParameters"] = {}
        '''
        #if mcase_id:
        #    mcase = MedalCase(mcase_id=mcase_id)
        #    athlete = mcase.update_athlete_medalcase(mcase_id)
        response = {'statusCode': 200}
        if route_key == '$connect':
            if not mcase_id:
                return {'statusCode': 404}
            response['statusCode'] = handle_connect(mcase_id, connection_id)

        elif route_key == '$disconnect':
            response['statusCode'] = handle_disconnect(connection_id)
        elif route_key == 'buildRuns':
            body = event.get('body')
            body = json.loads(body if body is not None else '{"msg": ""}')
            domain = event.get('requestContext', {}).get('domainName')
            stage = event.get('requestContext', {}).get('stage')
            if domain is None or stage is None:
                logger.warning(f"Couldn't send message: domain '{domain}',stage '{stage}'")
                response['statusCode'] = 400
            else:
                apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
                response['statusCode'] = handle_build_runs(connection_id, body, apig_management_client)
        else:
            response['statusCode'] = 404

        return response

    # regular REST API calls
    #------------------------------
    else:
        return awsgi.response(app, event, context)


if __name__ == '__main__':
    orm.sql_debug(True)
    app.run(debug=True, host='127.0.0.1', port=5180)
