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
    """[A page for users to register on the DB]

    Returns:
        [html]: [returns a page to register]
        [html]: [If the username already exists, the page is redirected]
        [html]: [If post sucsessful, the user's porfile page is returned]
    """
    profile_images = helpers.get_profile_images()

    if request.method == "POST":
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

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("users.profile", username=session["user"]))

    return render_template("register.html", profile_images=profile_images)


@users.route("/login", methods=["GET", "POST"])
def login():
    """[Page to login to the database]

    Returns:
        [html]: [Returns a login page]
        [html]: [On POST, if username doesn't exist,
                redirects to login with message]
        [html]: [On POST, if password is wrong,
                redirects to login with message]
        [html]: [On POST, sucsess, retuns Profile page]
    """
    if request.method == "POST":
        existing_user = mongo.db.gc_users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("users.profile",
                                        username=session["user"]))
            flash("Wrong Username / Password")
            return redirect(url_for("users.login"))

        flash("Wrong Username / Password")
        return redirect(url_for("users.login"))

    return render_template("login.html")


@users.route("/logout")
def logout():
    """[Removes the user from the session]

    Returns:
        [html]: [Returns login page]
    """
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("users.login"))


@users.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """[Current users profile page]

    Args:
        username ([username]): [CUrrent users username]

    Returns:
        [html]: [If session user exits, returns their profile page]]
        [html]: [If session user doesn't exist, returns login]
    """
    if session.get("user"):
        latest_games = helpers.get_latest_games()

        user = mongo.db.gc_users.find_one({"username": session["user"]})

        return render_template(
            "profile.html",
            latest_games=latest_games,
            user=user,
        )

    return redirect(url_for("users.login"))


@users.route("/profile/change-password", methods=["GET", "POST"])
def change_password():
    """[Changes the current users password]

    Returns:
        [html]: [If no session user, returns login page]
        [html]: [OnPOST, if passwords match, return change password page
        with message]
    """
    if session.get("user"):
        latest_games = helpers.get_latest_games()
        user = mongo.db.gc_users.find_one({"username": session["user"]})

        if request.method == "POST":
            if check_password_hash(mongo.db.gc_users.find_one(
                                {"username": session["user"]})["password"],
                                request.form.get("originalPassword")):
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
    """[A page showing all the reviews linked to the current user]

    Returns:
        [html]: [If no user logged in, returns logi page]
        [html]: [If user logged in, retunrs the your review page]
    """
    if session.get("user"):
        latest_games = helpers.get_latest_games()
        user = mongo.db.gc_users.find_one(
            {"username": session["user"]})

        your_reviews = list(mongo.db.reviews.find(
            {'review_by': session['user']}))

        total = len(your_reviews)
        page, per_page, offset = get_page_args(
            page_parameter='page', per_page_parameter='per_page')
        pagination_reviews = helpers.get_pag_list(offset=offset,
                                                  per_page=per_page,
                                                  list=your_reviews)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')

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
    """[Allows the current review to be edited]

    Args:
        review_id ([Object_ID]): [CUrrent review Object ID]

    Returns:
        [html]: [If no user logged in, returns logi page]
        [html]: [If user logged in, retunrs the your review page]
        [html]: [On POST, updated review in DB]
    """
    if session.get("user"):
        user = mongo.db.gc_users.find_one({"username": session["user"]})

        if request.method == "POST":
            update = {
                "review_message": request.form.get("review_message"),
                "review_rating": request.form.get("review_rating"),
                "review_title": request.form.get("review_title")
            }
            mongo.db.reviews.update(
                {"_id": ObjectId(review_id)}, {"$set": update})

            game_id = mongo.db.games.find_one(
                {"title": request.form.get("game_title")})

            flash("Review Updated")
            return redirect(url_for('games.game', game_id=game_id['_id']))

        review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
        return render_template("edit-review.html", review=review, user=user, session_url=session['url'])
    return redirect(url_for("users.login"))


@users.route("/delete-review/<review_id>")
def delete_review(review_id):
    """[Delets a review form the DB]

    Args:
        review_id ([Objec_id]): [Object ID of specific review]

    Returns:
        [html]: [if no session user, returns login]
        [html]: [delets review and returns to session url]
    """
    if session.get('user'):
        mongo.db.reviews.remove({"_id": ObjectId(review_id)})

        flash("Review Deleted")
        return redirect(session['url'])
    return redirect(url_for("users.login"))


@users.route("/profile/game-search", methods=["GET", "POST"])
def search_for_game():
    """[Look up a game in the databse]

    Returns:
        [html]: [If no session user, returns login]
        [html]: [if session user, returns game look up]
        [html]: [On POST, if game found, rredirect to game look up with
                returns to game seearch with game json]
        [html]: [on POST, if game not found, returns game look up with
                message]
    """
    if session.get('user'):
        user = mongo.db.gc_users.find_one({"username": session["user"]})

        latest_games = helpers.get_latest_games()
        all_games = helpers.get_all_games()
        session['url'] = url_for("users.search_for_game")

        if request.method == "POST":
            game = mongo.db.games.find_one(
                {"title": request.form.get("search")})

            if game:
                userReviews = list(mongo.db.reviews.find(
                    {'review_by': session['user']}))
                review = helpers.get_user_reviews_for_game_by_title(
                    userReviews, game)

                return render_template(
                    "review-game-search.html",
                    user=user,
                    latest_games=latest_games,
                    game=game,
                    all_games=all_games,
                    review=review
                )
            flash('Game Not Found')
            return redirect(url_for('users.search_for_game'))

        return render_template(
            "review-game-search.html",
            user=user,
            latest_games=latest_games,
            all_games=all_games
        )
    return redirect(url_for("users.login"))


@users.route('/profile/add-review/<game_id>', methods=["GET", "POST"])
def add_review(game_id):
    """[Adds a review to a specific game]

    Args:
        game_id ([Object_id]): [Object Id of specific game]

    Returns:
        [html]: [If no session user, returns login]
        [html]: [on POST, inserts review into DB]
    """
    if session.get('user'):
        game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

        if request.method == "POST":
            new_review = {
                "review_message": request.form.get("review_message"),
                "review_rating": request.form.get("review_rating"),
                "review_by": session['user'],
                "game_title": game['title'],
                "review_title": request.form.get("review_title")
            }
            mongo.db.reviews.insert(new_review)

            game = mongo.db.games.find_one({"title": game['title']})

            return redirect(url_for('games.game', game_id=game['_id']))

        return render_template("add-review.html", game=game)
    return redirect(url_for("users.login"))
