from flask import Flask,Blueprint,request
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import os
from dotenv import load_dotenv
from flask_cors import CORS,cross_origin
load_dotenv()
update_blueprint = Blueprint("update",__name__,static_folder="static",template_folder="templates")
mongo_uri=os.environ.get("mongo_db_uri")

cluster = MongoClient(mongo_uri)
db = cluster["user"]
collection = db["userdetails"]
api_key = os.environ.get("FLASK_APP_UPDATE_API_KEY")

@update_blueprint.route('/update', methods=['PATCH'])
@cross_origin(supports_credentials=True)
def update():
    try:
        if request.headers["api_key"] == api_key:
            payload = request.json["payload"]
            i = payload["_id"]
            details = payload["data"]
            if details.get("isDeleted") != None:
                res = collection.update_one({"_id": ObjectId(i)}, {
                    "$set": {"isDeleted": details["isDeleted"]}}, upsert=True)
            if details.get("isImportant") != None:
                res = collection.update_one({"_id": ObjectId(i)}, {
                    "$set": {"isImportant": details["isImportant"]}}, upsert=True)
            if details.get("isCompleted") != None:
                res = collection.update_one({"_id": ObjectId(i)}, {
                    "$set": {"isCompleted": details["isCompleted"]}}, upsert=True)
            return {"type": "UPDATE", "status": {"action": "PATCH_SUCCESS!", "serverMessage": "PATCH method handled successfully for UPDATE", "httpStatusCode": 200}, "data": {"_id": str(i)}}
        else:
            return {"type": "UPDATE", "status": {"action": "SERVER_ERROR!", "serverMessage": "UPDATE method failed for UPDATE", "httpStatusCode": 400}, "data": {"_id": None}}   
    except Exception:
        return{"type": "UPDATE", "status": {"action": "SERVER_ERROR!", "serverMessage": "UPDATE method failed for UPDATE", "httpStatusCode": 500}, "data": {"_id": None}}

