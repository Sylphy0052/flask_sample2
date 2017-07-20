# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request
import peewee as pe
import random
import json

def random_string(length, seq = '0123456789abcdefghijklmnopqrstuvwxyz'):
    sr = random.SystemRandom()
    return ''.join([sr.choice(seq) for i in range(length)])

db = pe.SqliteDatabase("datas.db")

class User(pe.Model):
    userId = pe.TextField()
    name = pe.TextField()
    caption = pe.TextField()
    old = pe.IntegerField()

    class Meta:
        database = db

api = Flask(__name__)

@api.route('/user/<string:userId>', methods=['GET'])
def get_user(userId):
    try:
        user = User.get(User.userId == userId)
    except User.DowsNotExist:
        abort(404)

    result = {
        "result":True,
        "data":{
            "userId":user.userId,
            "name":user.name,
            "caption":user.caption,
            "old":int(user.old)
        }
    }
    return make_response(jsonify(result))

@api.route('/usr', methods=['POST'])
def post_user():
    userId = 'us_' + random_string(6)
    dataDict = json.loads(request.data)
    try:
        q = User.insert(userId = userId, name = dataDict["name"], caption = dataDict["caption"], old = dataDict['old'])
        q.execute()
        user = User.get(User.userId == userId)
    except User.DowsNotExist:
        abort(404)

    result = {
        "result":True,
        "data":{
            "userId":user.userId,
            "name":user.name,
            "caption":user.caption,
            "old":int(user.old)
        }
    }
    return make_response(jsonify(result))

@api.route('/user/<string:userId>', methods=['PUT'])
def put_user(userId):
    dataDict = json.loads(request.data)
    try:
        q = User.update(name=dataDict["name"], caption=dataDict["caption"], old=dataDict["old"]).where(User.userId == userId)
        q.execute()
    except User.DowsNotExist:
        abort(404)

    result = {
        "result":True,
    }
    return make_response(jsonify(result))

@api.route('/user/<string:userId>', methods=['DELETE'])
def del_user(userId):
    try:
        q = User.delete().where(User.userId == userId)
        q.execute()
    except User.DowsNotExist:
        abort(404)

    result = {
        "result":True,
    }
    return make_response(jsonify(result))

@api.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.select()
    except User.DowsNotExist:
        abort(404)

    arr = []
    for user in users:
        arr.append({
            "userId":user.userId,
            "name":user.name,
            "caption":user.caption,
            "old":int(user.old)
        })

    result = {
        "result":True,
        "data":arr
    }
    return make_response(jsonify(result))

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)
