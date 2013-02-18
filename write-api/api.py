from flask import Flask
from flask import abort, request, Response
from pymongo import MongoClient

import re

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)

DATABASE_NAME = 'performance_platform'
VALID_KEYWORD = re.compile('^[a-z0-9_\.-]+$')
VALID_BUCKET_NAME = re.compile('^[a-z0-9\.-][a-z0-9_\.-]*$')

RESERVED_KEYWORDS = (
    '_timestamp',
    '_start_at',
    '_end_at',
)


@app.route('/_status/')
def health_check():
    if mongo.alive():
        return Response("{'status':'ok','message':'database seems fine'}",
                        mimetype='application/json')
    else:
        return Response(
            "{'status':500,'message':'can't connect to ""database'}",
            mimetype='application/json',
            status=500)


@app.route('/<bucket>/', methods=['POST'])
def post_to_bucket(bucket):
    if not request_is_valid(request, bucket):
        abort(400)

    incoming_data = prep_data(request.json)

    if any(invalid_data_object(obj) for obj in incoming_data):
        abort(400)
    else:
        store_objects(bucket, incoming_data)
        return Response("{'status':'ok'}", mimetype='application/json')


def request_is_valid(request, bucket_name):
    if request.json and bucket_is_valid(bucket_name):
        return True
    else:
        return False


def prep_data(incoming_json):
    if isinstance(incoming_json, list):
        return incoming_json
    else:
        return [incoming_json]


def invalid_data_object(obj):
    for key, value in obj.items():
        if key_is_valid(key) and value_is_valid(value):
            return False
        else:
            return True


def bucket_is_valid(bucket_name):
    if VALID_BUCKET_NAME.match(bucket_name):
        return True
    return False


def key_is_valid(key):
    key = key.lower()
    if key[0] == '_':
        if key in RESERVED_KEYWORDS:
            return True
    else:
        if VALID_KEYWORD.match(key):
            return True
    return False


def value_is_valid(value):
    if type(value) == int:
        return True
    if type(value) == unicode:
        return True
    return False


def store_objects(bucket_name, objects_to_store):
    bucket = mongo[DATABASE_NAME][bucket_name]
    bucket.insert(objects_to_store)


def value_is_a_date_time_string(value):
    time_pattern = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}"
                              "T[0-9]{2}:[0-9]{2}:[0-9]{2}"
                              "[+-][0-9]{2}:[0-9]{2}")
    return time_pattern.match(value)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')