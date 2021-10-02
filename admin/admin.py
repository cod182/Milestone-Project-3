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
    """[Shows the admin controls]

    Returns:
        [html]: [if user is logged in, not admin redirects to ther profile]
        [html]: [if user is not logged in, redirects to login]
        [html]: [if user is logged in adn admin, returns admin page]
    """
    if session.get('user'):
        latest_games = helpers.get_latest_games()

        user = mongo.db.gc_users.find_one({"username": session["user"]})
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
    """[Renders a page to search the DB for a user]

    Returns:
        [html]: [if user is logged in, not admin redirects to ther profile]
        [html]: [if user is not logged in, redirects to login]
        [html]: [if user is logged in and admin, returns admin page]
        [html]: [if searched user exists, returns look p page]
        [html]: [if searched user does not exists, redirects to search page]
    """
    if session.get('user'):
        user = mongo.db.gc_users.find_one({"username": session["user"]})
        latest_games = helpers.get_latest_games()

        allUsers = list(mongo.db.gc_users.find())
        
        if user['userType'] == 'admin':
            if request.method == "POST":
                searchedUser = request.form.get("username").lower()
                searchedUsers = list(mongo.db.gc_users.find(
                    {"username": searchedUser}))

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
    """[A button to delete a specific user and all of their reviews]

    Args:
        user_id ([Object_id]): [Object Id of specific user]

    Returns:
        [html]: [if user is logged in, not admin redirects to ther profile]
        [html]: [if user is not logged in, redirects to login]
        [html]: [if user is logged in and admin, rredirects to user search after deleting]
    """
    if session.get('user'):
        user = mongo.db.gc_users.find_one({"_id": ObjectId(user_id)})
        
        if user['userType'] == 'admin':
            mongo.db.reviews.remove({'review_by': user['username']})

            helpers.remove_user_by_object_id(user_id)

            flash("User & Reviews Deleted")
            return redirect(url_for("admin.user_search"))

        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route('/admin/edit-user/<user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    """[Allows selected users' name and userType to be updated.
    Will also update name aon all their reviews]

    Args:
        user_id ([Object_id]): [Object Id of user to be edited]

    Returns:
        [html]: [if user is logged in, not admin redirects to ther profile]
        [html]: [if user is not logged in, redirects to login]
        [html]: [if user is logged in and admin, returns edit user page]
        [html]: [if POST user details are updated in to DB]
    """
    if session.get('user'):
        user = mongo.db.gc_users.find_one({"username": session["user"]})
        userToEdit = mongo.db.gc_users.find_one({"_id": ObjectId(user_id)})
 
        if user['userType'] == 'admin':
            if request.method == 'POST':
                update = {
                    'username': request.form.get('username').lower(),
                    'userType': request.form.get('user-type').lower()
                }
                mongo.db.gc_users.update(
                    {"_id": ObjectId(user_id)}, {"$set": update})

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
    """[A page allowing look up of all games in the database]

    Returns:
        [html]: [if user is logged in, not admin redirects to ther profile]
        [html]: [if user is not logged in, redirects to login]
        [html]: [if user is logged in and admin, returns game search page]
        [html]: [if POST and game exists, returns game slookup page with game]
        [html]: [if POST and game does notexists, returns games lookup page with message]
    """
    if session.get('user'):
        latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
        gamesList = helpers.get_all_games()

        user = mongo.db.gc_users.find_one(
            {"username": session["user"]})

        if user['userType'] == 'admin':

            if request.method == "POST":
                searchedGame = request.form.get("game-name")
                games = list(mongo.db.games.find({"title": searchedGame}))

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
    """[Delets a specific game and all of it's reviews]

    Args:
        game_id ([Object_id]): [Object id of a specific game]

    Returns:
        [html]: [if user is logged in, not admin redirects to ther profile]
        [html]: [if user is not logged in, redirects to login]
        [html]: [if user is logged in and admin, returns to
        manage games page with message]
    """
    if session.get('user'):
        user = mongo.db.gc_users.find_one({"username": session["user"]})
        game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

        if user['userType'] == 'admin':
            mongo.db.reviews.remove({'game_title': game['title']})
            mongo.db.games.remove({"_id": ObjectId(game_id)})

            flash("Game & Reviews Deleted")
            return redirect(url_for('admin.manage_games'))
        return redirect(url_for("users.profile", username=session.get('user')))
    return redirect(url_for("users.login"))


@admin.route('/admin/manage-reviews', methods=["GET", "POST"])
def manage_reviews():
    """[summary]

    Returns:
        [html]: [if user is logged in, not admin redirects to ther profile]
        [html]: [if user is not logged in, redirects to login]
        [html]: [if user is logged in and admin, returns review lookup page]
        [html]: [if POST game not found, redirects to manage reviews page 
        with a message]
        [html]: [if POST reviews are returned to lookup page]
    """
    if session.get('user'):
        session['url'] = url_for("admin.manage_reviews")
        user = mongo.db.gc_users.find_one({"username": session["user"]})
        reviewList = list(mongo.db.reviews.find())

        latest_games = helpers.get_latest_games()
        gamesList = helpers.get_all_games()

        if user['userType'] == 'admin':
            if request.method == "POST":
                searchedGame = request.form.get("game-name")
                game = mongo.db.games.find_one({"title": searchedGame})

                if game:
                    reviews = list(mongo.db.reviews.find(
                        {"game_title": game['title']}))

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
