from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
from flask import Flask, request, jsonify,json
from flask_cors import CORS, cross_origin
from add import add_blueprint
from update import update_blueprint
from bson.json_util import dumps
from delete import delete_blueprint
from fetch import fetch_blueprint
import os
from flask import Flask, render_template
mongo_uri = os.environ.get("mongo_db_uri")

cluster = MongoClient(mongo_uri)
db = cluster["user"]
collection = db["userdetails"]
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})



app.register_blueprint(add_blueprint, url_prefix="/")
app.register_blueprint(update_blueprint, url_prefix="/")
app.register_blueprint(delete_blueprint, url_prefix="/")
app.register_blueprint(fetch_blueprint, url_prefix="/")



@app.route("/")
def welcome_api():
  return "API is working, deployed on Heroku!"

@app.errorhandler(400)
def error(e):
    return {"message": "bad request"}


@app.errorhandler(404)
def error(e):
    return {"message": "page not found!", "httpscode": 404}


@app.errorhandler(405)
def error(e):
    return {"message": "method not allowed!"}


if __name__ == "__main__":
    app.run(debug=True)
