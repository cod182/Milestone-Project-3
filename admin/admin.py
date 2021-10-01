from database import mongo
import helpers
from flask import (
    flash, render_template, redirect,
    request, session, url_for)
from bson.objectid import ObjectId
from flask import Blueprint

admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static')


@admin.route('/admin', methods=["GET", "POST"])
def get_admin():
    if session.get('user'):
        # Gets the latest 5 games
        latest_games = helpers.get_latest_games()
        # gets the user in db from session user
        user = helpers.get_user_from_session_user(session["user"])
        if user['userType'] == 'admin':
            return render_template(
                "admin-base.html",
                user=user,
                latest_games=latest_games
            )
        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route('/admin/user-search', methods=["GET", "POST"])
def user_search():
    """
    Go to a page to search all users
    """
    if session.get('user'):
        user = helpers.get_user_from_session_user(session["user"])
        latest_games = helpers.get_latest_games()
        # gets all the db users
        allUsers = helpers.get_all_users()
        if user['userType'] == 'admin':
            if request.method == "POST":
                searchedUser = request.form.get("username").lower()

                # returns the users found from serch
                searchedUsers = helpers.get_user_list_by_username(searchedUser)

                # if user exists
                if searchedUsers:
                    return render_template(
                        "admin-user-lookup.html",
                        user=user,
                        latest_games=latest_games,
                        allUsers=allUsers,
                        searchedUsers=searchedUsers
                    )
                flash('User Not Found!')
                return redirect(url_for('admin.user_search'))

            return render_template(
                "admin-user-lookup.html",
                user=user,
                latest_games=latest_games,
                allUsers=allUsers
            )
        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route('/admin/delete-user/<user_id>', methods=["GET", "POST"])
def delete_user(user_id):
    """
    From a button to delete the selected user review_id
    """
    if session.get('user'):
        # finds the account name of user_id
        user = helpers.get_user_by_id(user_id)
        if user['userType'] == 'admin':
            # Removes the reviews by user_id username
            helpers.remove_reviews_by_user(user['username'])

            # Removes the user with matching id
            helpers.remove_user_by_object_id(user_id)

            flash("User & Reviews Deleted")

            return redirect(url_for("admin.user_search"))

        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route('/admin/edit-user/<user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    if session.get('user'):
        # gets the session user
        user = helpers.get_user_from_session_user(session["user"])

        # finds the user matching the id
        userToEdit = mongo.db.gc_users.find_one({"_id": ObjectId(user_id)})
        if user['userType'] == 'admin':
            if request.method == 'POST':
                # Update details from form
                update = {
                    'username': request.form.get('username').lower(),
                    'userType': request.form.get('user-type').lower()
                }
                # updates the user from update dict
                mongo.db.gc_users.update(
                    {"_id": ObjectId(user_id)}, {"$set": update})

                # Update the name on all review by user
                mongo.db.reviews.update_many(
                    {"review_by": userToEdit['username'].lower()},
                    {"$set": {"review_by": request.form.get(
                        'username').lower()}})

                flash('User Updated')
                return redirect(url_for("admin.user_search"))

            return render_template(
                'edit-user.html',
                user=user,
                userToEdit=userToEdit,
            )
        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route("/admin/manage-games", methods=["GET", "POST"])
def manage_games():
    if session.get('user'):
        # gets the latest games
        latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))

        # gets the session user and then current user username
        user = mongo.db.gc_users.find_one(
            {"username": session["user"]})

        # gets all games
        gamesList = helpers.get_all_games()
        if user['userType'] == 'admin':

            if request.method == "POST":
                searchedGame = request.form.get("game-name")

                # returns the games found from serch
                games = list(mongo.db.games.find({"title": searchedGame}))

                # if game exists
                if searchedGame:
                    return render_template(
                        "admin-games-lookup.html",
                        user=user,
                        gamesList=gamesList,
                        games=games,
                        latest_games=latest_games
                    )
                flash('Game Not Found!')
                return redirect(url_for('admin.manage_games'))

            return render_template(
                "admin-games-lookup.html",
                user=user,
                gamesList=gamesList,
                latest_games=latest_games
            )
        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route("/admin/delete-game/<game_id>", methods=["GET", "POST"])
def delete_game_and_reviews(game_id):
    """
    From a button to delete the selected game
    and reviews from game_id
    """
    if session.get('user'):
        # finds the account name of game_id
        # gets the session user and then current user username
        user = helpers.get_user_from_session_user(session["user"])
        game = helpers.get_game_by_object_id(game_id)
        if user['userType'] == 'admin':
            # Removes the reviews by game_id username
            helpers.remove_game_reviews_by_title(game['title'])
            # Removes the game with matching id
            helpers.remove_game_by_objectId(game_id)

            flash("Game & Reviews Deleted")

            return redirect(url_for('admin.manage_games'))
        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route('/admin/manage-reviews', methods=["GET", "POST"])
def manage_reviews():
    if session.get('user'):
        # sets the sessions url to get_user_reviews Page
        session['url'] = url_for("admin.manage_reviews")

        # gets the latest games
        latest_games = helpers.get_latest_games()

        # gets the session user and then current user username
        user = helpers.get_user_from_session_user(session["user"])

        # gets all reviews
        reviewList = helpers.get_all_user_reviews()

        # gets all games
        gamesList = helpers.get_all_games()
        if user['userType'] == 'admin':
            if request.method == "POST":
                # Gets the searched term
                searchedGame = request.form.get("game-name")

                # returns the game found from search
                game = helpers.get_game_by_game_name(searchedGame)

                # if game exists
                if game:
                    reviews = helpers.get_game_reviews_by_title(game['title'])

                    return render_template(
                        "admin-review-lookup.html",
                        user=user,
                        gamesList=gamesList,
                        reviews=reviews,
                        latest_games=latest_games
                    )
                flash('Game Not Found!')
                return redirect(url_for('admin.manage_reviews'))

            return render_template(
                "admin-review-lookup.html",
                user=user,
                reviewList=reviewList,
                latest_games=latest_games,
                gamesList=gamesList
            )
        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))
