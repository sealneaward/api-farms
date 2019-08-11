import json
import os
import traceback
from flask import Flask, make_response, request
import pymongo

import farm.config as CONFIG

app = Flask(__name__)

# check if db exists
# create if names is not in databases list
client = pymongo.MongoClient("mongodb://localhost:27017/")
names_db = client["names_db"]
names = names_db["names"]


@app.route('/hello')
def report():
    try:
        name = request.args.get('name')
        if name == '' or name is None:
            name = 'stranger'
    except BaseException as e:
        resp = make_response('{"status": "fail", "msg": %s}' % traceback.print_exc(e))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp
    # create object to insert into collection
    obj = {"name": name}
    if names.find(obj).count() == 0:
        names.insert_one(obj)

    # return message
    res = 'Hello %s!' % name
    resp = make_response(res)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000, debug=True)
