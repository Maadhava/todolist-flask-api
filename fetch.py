from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,Blueprint,request,jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()
fetch_blueprint = Blueprint("fetch",__name__,static_folder="static",template_folder="templates")
mongo_uri=os.environ.get("mongo_db_uri")

cluster = MongoClient(mongo_uri)
db = cluster["user"]
collection = db["userdetails"]
api_key = os.environ.get("FLASK_APP_FETCH_API_KEY")

@fetch_blueprint.route('/fetch')
@cross_origin(supports_credentials=True)
def fetch():
    if request.headers["api_key"]==api_key:
        db_name = "user"
        doc_name = "userdetails"
        mydb = cluster[db_name][doc_name]
        result = list(mydb.find())
        for data in result:
            data["_id"] = str(ObjectId())  #json seriliazable error
        return jsonify(
        type="FETCH",
        status={
            "action": "FETCH_SUCCESS!",
            "serverMessage": "GET method handled successfully for /fetch",
            "httpStatusCode": 200,
            },
            data=result,
        )
    else:
        return {"type": "FETCH", "status": {"action": "SERVER_ERROR!", "serverMessage": "FETCH method failed for FETCH", "httpStatusCode": 400}, "data": {"_id": None}}