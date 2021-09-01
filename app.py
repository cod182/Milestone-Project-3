import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import requests
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get("MONGO_DEBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    return render_template("index.html", latest_games=latest_games)


@app.route("/profile")
def profile():
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    return render_template("profile.html", latest_games=latest_games)


@app.route("/latest_reviews")
def latest_reviews():
    return render_template("latest-reviews.html")


@app.route("/games")
def games():
    return render_template("games.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
