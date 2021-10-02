from database import mongo
import helpers
from flask import (
    flash, render_template, redirect,
    request, session, url_for, Blueprint)
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint(
    'users',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/users/static')


@users.route("/register", methods=["GET", "POST"])
def register():
    """
    Go to a page to register to database
    """
    # Gets all the profile image options
    profileImages = helpers.get_profile_images()

    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.gc_users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("users.register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "userType": "standard",
            "profile_image": request.form.get("profile_image")
        }
        mongo.db.gc_users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("users.profile", username=session["user"]))

    return render_template("register.html", profileImages=profileImages)


@users.route("/login", methods=["GET", "POST"])
def login():
    """
    Go to a page to login
    """
    if request.method == "POST":
        # Check if username exists in db
        existing_user = mongo.db.gc_users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("users.profile",
                                        username=session["user"]))
            # invalid password match
            flash("Wrong Username / Password")
            return redirect(url_for("users.login"))

        # username doesn't exist
        flash("Wrong Username / Password")
        return redirect(url_for("users.login"))

    return render_template("login.html")


@users.route("/logout")
def logout():
    """
    From a button removes the sessions cookie
    """
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("users.login"))


@users.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Go to a page to display users profile page
    """
    if session.get("user"):
        # gets the latest 5 games
        latest_games = helpers.get_latest_games()
        # grab the session user's username from db
        user = mongo.db.gc_users.find_one({"username": session["user"]})
        return render_template(
            "profile.html",
            latest_games=latest_games,
            user=user,
        )

    return redirect(url_for("users.login"))


@users.route("/profile/change-password", methods=["GET", "POST"])
def change_password():
    """
    Go to a page to change password of account. Takes a POST
    """
    if session.get("user"):
        latest_games = helpers.get_latest_games()
        user = mongo.db.gc_users.find_one({"username": session["user"]})
        userPass = mongo.db.gc_users.find_one(
            {"username": session["user"]})["password"]

        if request.method == "POST":
            if check_password_hash(userPass, request.form.get(
                    "originalPassword")):
                mongo.db.gc_users.update_one(
                    {"username": user['username'].lower()},
                    {"$set": {
                        "password": generate_password_hash(request.form.get(
                            "password"
                        ))
                    }}
                )
                flash("Password Updated")
            else:
                flash('Password Incorrect')
        return render_template(
            "changepass.html",
            user=user,
            latest_games=latest_games
        )
    return redirect(url_for("users.login"))


@users.route("/profile/your-reviews")
def get_user_reviews():
    """
    Go to a page displaying all reviews linked to the session.user
    extends the profile page
    """
    if session.get("user"):
        # gets the latest games in revers order. Max of 5
        latest_games = helpers.get_latest_games()
        # gets the user matching the session user
        user = mongo.db.gc_users.find_one(
            {"username": session["user"]})
        # gets all review by the user
        your_reviews = list(mongo.db.reviews.find(
            {'review_by': session['user']}))
        # the length og the your review list
        total = len(your_reviews)

        page, per_page, offset = get_page_args(
            page_parameter='page', per_page_parameter='per_page')
        # pagination for the reviews
        pagination_reviews = helpers.get_pag_list(offset=offset,
                                                  per_page=per_page,
                                                  list=your_reviews)
        # Pagination controsl
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')
        # sets the sessions url to get_user_reviews Page
        session['url'] = url_for("users.get_user_reviews")

        return render_template(
            "your-reviews.html",
            your_reviews=pagination_reviews,
            pagination=pagination,
            latest_games=latest_games,
            user=user
        )
    return redirect(url_for("users.login"))


@users.route("/review/<review_id>", methods=["GET", "POST"])
def edit_user_review(review_id):
    """
    Go to a page to edit a review based on it's review_id
    """
    if session.get("user"):
        # gets user matched with session user
        user = mongo.db.gc_users.find_one({"username": session["user"]})

        if request.method == "POST":
            """
            Gets values from form and update the relevant
            review with them
            """
            # Update key value pairs from form
            update = {
                "review_message": request.form.get("review_message"),
                "review_rating": request.form.get("review_rating"),
                "review_title": request.form.get("review_title")
            }
            # Updates the review with matching _id with update dict
            mongo.db.reviews.update(
                {"_id": ObjectId(review_id)}, {"$set": update})

            flash("Review Updated")

            # gets the game id with the matching title
            game_id = mongo.db.games.find_one(
                {"title": request.form.get("game_title")})

            return redirect(url_for('games.game', game_id=game_id['_id']))

        # finds a review with matching _id
        review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

        return render_template("edit-review.html", review=review, user=user)
    return redirect(url_for("users.login"))


@users.route("/delete-review/<review_id>")
def delete_review(review_id):
    """
    From a button to delete the selected review based on review_id
    """
    if session.get('user'):
        # Removes the review with atching _id
        mongo.db.reviews.remove({"_id": ObjectId(review_id)})
        flash("Review Deleted")

        return redirect(session['url'])
    return redirect(url_for("users.login"))


@users.route("/profile/game-search", methods=["GET", "POST"])
def search_for_game():
    """
    Go to a page to search all games in order to add a review
    OR add a new game to Database
    """
    if session.get('user'):
        user = mongo.db.gc_users.find_one({"username": session["user"]})
        # gets the latest 5 games, newest first
        latest_games = helpers.get_latest_games()
        # gets all the games in db
        allgames = helpers.get_all_games()

        # if a post request
        if request.method == "POST":
            # gets the name from the search box
            gameName = request.form.get("search")
            # searches the game in db
            game = mongo.db.games.find_one({"title": gameName})
            if game:
                # gets reviews by user
                userReviews = list(mongo.db.reviews.find(
                    {'review_by': session['user']}))
                # Get review for game
                review = helpers.get_user_reviews_for_game_by_title(
                    userReviews, game)

                return render_template(
                    "review-game-search.html",
                    user=user,
                    latest_games=latest_games,
                    game=game,
                    allgames=allgames,
                    review=review
                )
            flash('Game Not Found')
            return redirect(url_for('users.search_for_game'))

        return render_template(
            "review-game-search.html",
            user=user,
            latest_games=latest_games,
            allgames=allgames
        )
    return redirect(url_for("users.login"))


@users.route('/profile/addReview/<game_id>', methods=["GET", "POST"])
def add_review(game_id):
    """
    Go to a page to add a review to a game based on game_id
    """
    if session.get('user'):
        # find the game with matching _id
        game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

        if request.method == "POST":
            # newReview key value pairs from form
            newReview = {
                "review_message": request.form.get("review_message"),
                "review_rating": request.form.get("review_rating"),
                "review_by": session['user'],
                "game_title": game['title'],
                "review_title": request.form.get("review_title")
            }
            # Inserts new document from newReview into db
            mongo.db.reviews.insert(newReview)

            # find game with title matches the form title
            game = mongo.db.games.find_one({"title": game['title']})

            # redirected to game page
            return redirect(url_for('games.game', game_id=game['_id']))

        return render_template("add-review.html", game=game)
    return redirect(url_for("users.login"))
