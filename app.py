import os
from flask import (Flask, url_for, render_template)
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


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
