from flask import Flask, Blueprint, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import os
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
load_dotenv()
add_blueprint = Blueprint("add", __name__, static_folder="static",
                template_folder="templates")
mongo_uri = os.environ.get("mongo_db_uri")
cluster = MongoClient(mongo_uri)
db = cluster["user"]
collection = db["userdetails"]
api_key = os.environ.get("FLASK_APP_ADD_API_KEY")

 

@add_blueprint.route('/add', methods=['POST'])
@cross_origin(supports_credentials=True)
def create():
    if request.headers["api_key"] == api_key:
        details = request.json["payload"]
        if  details.get("isCompleted") != None and details.get("isImportant") != None and details.get("isDeleted") != None and details.get("taskTitle") != None:
            if isinstance(details["taskTitle"],str) and isinstance(details["isCompleted"],bool) and isinstance(details["isDeleted"],bool) and isinstance(details["isImportant"],bool) and request.json["action"] == "CREATE":
                _id = collection.insert_one(details)
                return {"type": "CREATE", "status": {"action": "POST_SUCCESS!", "serverMessage": "POST method handled successfully for CREATE", "httpStatusCode": 201}, "data": {"_id": str(_id.inserted_id)}}
            else:
                return {"type": "CREATE", "status": {"action": "SERVER_ERROR!", "serverMessage": "CREATE method failed for CREATE", "httpStatusCode": 500}, "data": {"_id": None}}
        else:
            return {"type": "CREATE", "status": {"action": "unprocessable entity!", "serverMessage": "CREATE method failed for CREATE", "httpStatusCode": 422}, "data": {"_id": None}}
    else:
         return {"type": "CREATE", "status": {"action": "SERVER_ERROR!", "serverMessage": "CREATE method failed for CREATE", "httpStatusCode": 400}, "data": {"_id": None}}