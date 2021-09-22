import os
from database import mongo
from flask import (
    flash, render_template, redirect,
    request, session, url_for)
from bson.objectid import ObjectId
from flask import Blueprint
if os.path.exists("env.py"):
    import env

admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static')


RAWG_API = os.environ.get("RAWG_API_KEY")


@admin.route('/admin', methods=["GET", "POST"])
def get_admin():
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()
    if session["user"]:
        if user['userType'] == 'admin':
            return render_template(
                "admin-base.html",
                username=username,
                user=user,
                latest_games=latest_games
            )

    return redirect(url_for("users.login"))


@admin.route('/admin/user-search', methods=["GET", "POST"])
def user_search():

    """
    Go to a page to search all user
    """
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    # gets all the db users
    allUsers = list(mongo.db.gc_users.find())

    if request.method == "POST":
        searchedUser = request.form.get("username").lower()

        # returns the users found from serch
        searchedUsers = list(mongo.db.gc_users.find(
            {"username": searchedUser}
        ))

        # if user exists
        if searchedUsers:
            return render_template(
                "admin-user-lookup.html",
                user=user,
                username=username,
                latest_games=latest_games,
                allUsers=allUsers,
                searchedUsers=searchedUsers
            )
        flash('User Not Found!')
        return redirect(url_for('admin.user_search'))

    return render_template(
        "admin-user-lookup.html",
        user=user,
        username=username,
        latest_games=latest_games,
        allUsers=allUsers
    )


@admin.route('/admin/delete-user/<user_id>', methods=["GET", "POST"])
def delete_user(user_id):
    """
    From a button to delete the selected user review_id
    """
    # finds the account name of user_id
    user = mongo.db.gc_users.find_one({"_id": ObjectId(user_id)})

    # Removes the reviews by user_id username
    mongo.db.reviews.remove({'review_by': user['username']})

    # Removes the user with matching id
    mongo.db.gc_users.remove({"_id": ObjectId(user_id)})

    flash("User & Reviews Deleted")

    return redirect(url_for("admin.user_search"))


@admin.route('/admin/edit-user/<user_id>', methods=["GET", "POST"])
def edit_user(user_id):

    # gets the session user and then current user username
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()

    # finds the user matching the id
    userToEdit = mongo.db.gc_users.find_one({"_id": ObjectId(user_id)})

    if request.method == 'POST':
        # Update details from form
        update = {
            'username': request.form.get('username').lower(),
            'userType': request.form.get('user-type').lower()
        }
        # updates the user from update dict
        mongo.db.gc_users.update({"_id": ObjectId(user_id)}, {"$set": update})

        # Update the name on all review by user
        mongo.db.reviews.update_many(
            {"review_by": userToEdit['username'].lower()},
            {"$set": {"review_by": request.form.get('username').lower()}})

        flash('User Updated')
        return redirect(url_for("admin.user_search"))

    return render_template(
        'edit-user.html',
        user=user,
        userToEdit=userToEdit,
        username=username
    )


@admin.route("/admin/manage-games", methods=["GET", "POST"])
def manage_games():
    # gets the latest games
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))

    # gets the session user and then current user username
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()

    # gets all games
    gamesList = list(mongo.db.games.find())

    if request.method == "POST":
        searchedGame = request.form.get("game-name")

        # returns the games found from serch
        games = list(mongo.db.games.find({"title": searchedGame}))

        # if game exists
        if searchedGame:
            return render_template(
                "admin-games-lookup.html",
                user=user,
                username=username,
                gamesList=gamesList,
                games=games,
                latest_games=latest_games
            )

        flash('User Not Found!')
        return redirect(url_for('admin.manage_games'))

    return render_template(
        "admin-games-lookup.html",
        user=user,
        username=username,
        gamesList=gamesList,
        latest_games=latest_games
    )


@admin.route("/admin/delete-game/<game_id>", methods=["GET", "POST"])
def delete_game_and_reviews(game_id):
    """
    From a button to delete the selected game
    and reviews from game_id
    """
    # finds the account name of game_id
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    # Removes the reviews by game_id username
    mongo.db.reviews.remove({'game_title': game['title']})

    # Removes the game with matching id
    mongo.db.games.remove({"_id": ObjectId(game_id)})

    flash("Game & Reviews Deleted")

    return redirect(url_for('admin.manage_games'))


@admin.route('/admin/manage-reviews', methods=["GET", "POST"])
def manage_reviews():

    # sets the sessions url to yourReviews Page
    session['url'] = url_for("admin.manage_reviews")

    # gets the latest games
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))

    # gets the session user and then current user username
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()

    # gets all reviews
    reviewList = list(mongo.db.reviews.find())

    # gets all games
    gamesList = list(mongo.db.games.find())

    if request.method == "POST":
        # Gets the searched term
        searchedGame = request.form.get("game-name")

        # returns the game found from search
        game = mongo.db.games.find_one({"title": searchedGame})
        print(game)

        # if game exists
        if game:
            reviews = list(mongo.db.reviews.find(
                {"game_title": game['title']}
            ))

            return render_template(
                "admin-review-lookup.html",
                user=user,
                username=username,
                gamesList=gamesList,
                reviews=reviews,
                latest_games=latest_games
            )
        flash('Game Not Found!')
        return redirect(url_for('admin.manage_reviews'))

    return render_template(
        "admin-review-lookup.html",
        user=user,
        username=username,
        reviewList=reviewList,
        latest_games=latest_games,
        gamesList=gamesList
    )
