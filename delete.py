from flask import Flask, Blueprint, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin


load_dotenv()
delete_blueprint = Blueprint("delete", __name__, static_folder="static",
                  template_folder="templates")
mongo_uri = os.environ.get("mongo_db_uri")
cluster = MongoClient(mongo_uri)
db = cluster["user"]
collection = db["userdetails"]

api_key = os.environ.get("FLASK_APP_DELETE_API_KEY")


@delete_blueprint.route('/delete', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete():
        if request.headers["api_key"] == api_key:
            details = request.json["payload"]
            if  isinstance(details["_id"],str) and request.json["action"] == "DELETE":
                i = details["_id"]
                myquery = {"_id": ObjectId(i)}
                collection.delete_one(myquery)
                return {"type": "ERASE", "status": {"action": "DELETE_SUCCESS!", "serverMessage": "DELETE method handled successfully for DELETE", "httpStatusCode": 200}, "data": {"_id": str(i)}}
            else:
                return {"type": "ERASE", "status": {"action": "unprocessable entity!", "serverMessage": "ERASE method failed for ERASE", "httpStatusCode": 422}, "data": {"_id": None}}
        else:
            return {"type": "DELETE", "status": {"action": "SERVER_ERROR!", "serverMessage": "DELETE method failed for DELETE", "httpStatusCode": 400}, "data": {"_id": None}}