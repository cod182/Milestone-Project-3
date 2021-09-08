import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    return render_template("index.html", latest_games=latest_games)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.gc_users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.gc_users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.gc_users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Wrong Username / Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Wrong Username / Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    # grab the session user's username from db
    username = mongo.db.gc_users.find_one(
        {"username": session["user"]})["username"].capitalize()

    if session["user"]:
        return render_template("profile.html", latest_games=latest_games,
                                username=username)

    return redirect(url_for("login"))


@app.route("/profileGameSearch", methods=["GET", "POST"])
def profileGameSearch():
    username = mongo.db.gc_users.find_one(
        {"username": session["user"]})["username"].capitalize()
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    allgames = list(mongo.db.games.find())

    return render_template("review-game-search.html", username=username, latest_games=latest_games, allgames=allgames)


@app.route("/gameSearch", methods=["GET", "POST"])
def gameSearch():
    username = mongo.db.gc_users.find_one(
        {"username": session["user"]})["username"].capitalize()
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    gameName = request.form.get("search")
    games = list(mongo.db.games.find({"$text": {"$search": gameName}}))
    allgames = list(mongo.db.games.find())
    reviews = list(mongo.db.reviews.find())

    return render_template("review-game-search.html", username=username,
                            latest_games=latest_games, games=games, allgames=allgames, reviews=reviews)


@app.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    return render_template("game.html", game=game)


@app.route("/changePass", methods=["GET", "POST"])
def changePass():
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    username = mongo.db.gc_users.find_one(
        {"username": session["user"]})["username"]
    userPass = mongo.db.gc_users.find_one(
        {"username": session["user"]})["password"]

    if request.method == "POST":
        if check_password_hash(userPass, request.form.get("originalPassword")):
            mongo.db.gc_users.update_one({"username": username}, {"$set": {"password": generate_password_hash(request.form.get("password"))}})
            flash("Password Updated")
        else:
            flash('Password Incorrect')
    return render_template("changepass.html", username=username.capitalize(), latest_games=latest_games)


@app.route("/yourReviews")
def yourReviews():
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    username = mongo.db.gc_users.find_one(
        {"username": session["user"]})["username"]
    your_reviews = list(mongo.db.reviews.find())
    return render_template("your-reviews.html", your_reviews=your_reviews,
                            latest_games=latest_games, username=username.capitalize())


@app.route("/review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == "POST":
        update = {
            "review_message": request.form.get("review_message"),
            "review_rating": request.form.get("review_rating"),
            "review_by": session['user'],
            "game_title": request.form.get("game_title")
        }
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, update)
        flash("Review Updated")

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    return render_template("edit-review.html", review=review)


@app.route("/deleteReview/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Deleted")
    return redirect(url_for("yourReviews"))

@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/latest_reviews")
def latest_reviews():
    return render_template("latest-reviews.html")


@app.route("/games")
def games():
    return render_template("games.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
