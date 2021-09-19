import os
import requests
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config['MONGO_DBNAME'] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
RAWG_API = os.environ.get("RAWG_API_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """
    Go to a page to display the home screen
    """
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    return render_template("index.html", latest_games=latest_games)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Go to a page to register to database
    """
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
            "password": generate_password_hash(request.form.get("password")),
            "userType": "standard"
        }
        mongo.db.gc_users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
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
                return redirect(url_for("profile",
                                        username=session["user"]))
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
    """
    Go to a page to display users profile page
    """
    if session["user"]:
        latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
        # grab the session user's username from db
        user = mongo.db.gc_users.find_one(
            {"username": session["user"]})
        username = user['username'].capitalize()
        return render_template("profile.html", latest_games=latest_games,
                                username=username, user=user)

    return redirect(url_for("login"))


@app.route('/adminpanel', methods=["GET", "POST"])
def adminPanel():
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()
    if session["user"]:
        if user['userType'] == 'admin':
            return render_template("admin-base.html", username=username, user=user, latest_games=latest_games)

    return redirect(url_for("login"))


@app.route('/adminUserLookUp', methods=["GET", "POST"])
def adminUserLookUp():

    """
    Go to a page to search all user
    """
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    allUsers = list(mongo.db.gc_users.find())

    return render_template("admin-user-lookup.html", user=user, username=username,
                            latest_games=latest_games, allUsers=allUsers)


@app.route('/adminUserSearch', methods=["GET", "POST"])
def adminUserSearch():
    # gets the session user and then current user username
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()

    # gets the latest games
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))

    # gets all of the users
    allUsers = list(mongo.db.gc_users.find())

    if request.method == "POST":
        searchedUser = request.form.get("username")

        # returns the users found from serch
        searchedUsers = list(mongo.db.gc_users.find({"username": searchedUser}))
        # if user exists
        if searchedUsers:
            return render_template("admin-user-lookup.html", user=user, username=username,
                                latest_games=latest_games, allUsers=allUsers, searchedUsers=searchedUsers)
        else:
            flash('User Not Found!')
            return redirect(url_for('adminUserLookUp'))


@app.route('/adminDeleteUser/<user_id>', methods=["GET", "POST"])
def adminDeleteUser(user_id):
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

    return redirect(url_for("adminUserLookUp"))


@app.route('/adminEditUser/<user_id>', methods=["GET", "POST"])
def adminEditUser(user_id):

    # gets the session user and then current user username
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()

    # finds the user matching the id
    userToEdit = mongo.db.gc_users.find_one({"_id": ObjectId(user_id)})

    if request.method == 'POST':
        # Update details from form
        update = {
            'username': request.form.get('username'),
            'userType': request.form.get('user-type')
        }
        # updates the user from update dict
        mongo.db.gc_users.update({"_id": ObjectId(user_id)}, {"$set": update})
        flash('User Updated')
        return redirect(url_for("adminUserLookUp"))

    return render_template('edit-user.html', user=user, userToEdit=userToEdit, username=username)


@app.route("/manageGames", methods=["GET", "POST"])
def manageGames():
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
            return render_template("admin-games-lookup.html", user=user, username=username, gamesList=gamesList, games=games, latest_games=latest_games)
        else:
            flash('User Not Found!')
            return redirect(url_for('manageGames'))

    return render_template("admin-games-lookup.html", user=user, username=username, gamesList=gamesList, latest_games=latest_games)


@app.route("/adminDeleteGame/<game_id>", methods=["GET", "POST"])
def adminDeleteGame(game_id):
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

    return redirect(url_for('manageGames'))


@app.route('/manageReviews', methods=["GET", "POST"])
def manageReviews():
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
        searchedGame = request.form.get("game-name")

        # returns the game found from search
        game = mongo.db.games.find_one({"title": searchedGame})
        print(game)

        reviews = list(mongo.db.reviews.find({"game_title": game['title'] }))

        # if reviews exists
        if reviews:
            return render_template("admin-review-lookup.html", user=user, username=username, gamesList=gamesList, reviews=reviews, latest_games=latest_games)
        else:
            flash('No Reviews found for that game')
            return redirect(url_for('manageReviews'))

    return render_template("admin-review-lookup.html", user=user, username=username, reviewList=reviewList, latest_games=latest_games, gamesList=gamesList)


@app.route("/gameLookUp", methods=["GET", "POST"])
def game_lookup():
    if request.method == "POST":
        search = request.form.get("game-name")
        try:
            response = requests.get("https://api.rawg.io/api/games" + "?key=" + RAWG_API + '&search=' + search)
            gameData = response.json()

            return render_template('select-game.html', gameData=gameData)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
            flash('No Results Found')
            return redirect(url_for('game_lookup'))

    return render_template('lookup-game.html')


@app.route('/addGame', methods=["GET", "POST"])
def add_game():
    """
    Added a new game to the database
    """
    if request.method == "POST":
        # Checks if game already exists in database
        existing_game = mongo.db.games.find_one(
            {"game_id": int(request.form.get('selected-game'))})

        if existing_game:
            flash('Game Already Exists')
            return redirect(url_for('game_lookup'))

        # Gets the game id from page then makes and API call in order to get details
        gameId = request.form.get('selected-game')
        apiCall = requests.get("https://api.rawg.io/api/games/" + gameId + "?key=" + RAWG_API)
        data = apiCall.json()

        # Fields to be inseted into db
        newGame = {
            "title": data['name'],
            "year": data['released'],
            "genres": data['genres'],
            "game_id": data['id'],
            "description": data['description'],
            "largeImage": data['background_image'],
            "platforms": data['platforms'],
            "rating": data['esrb_rating'],
            "background": data['background_image_additional'],
            "metacritic": data['metacritic']
        }

        # Game inserted into database
        mongo.db.games.insert(newGame)
        game = mongo.db.games.find_one(
            {"game_id": data['id']})

        now = datetime.now()
        # dd/mm/YY H:M:S
        currenttime = now.strftime("%d/%m/%Y %H:%M:%S")

        # Adds the user who added the game and the time/date
        mongo.db.games.update_one({"_id": ObjectId(game['_id'])}, {"$push":{ 'updated_by': {
            'username': session['user'],
            'time': currenttime
            }}})

        # redirected to game page
        return redirect(url_for('game', game_id=game['_id']))

    return render_template('add-game.html')


@app.route("/profileGameSearch", methods=["GET", "POST"])
def profileGameSearch():
    """
    Go to a page to search all games in order to add a review
    OR add a new game to Database
    """
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    allgames = list(mongo.db.games.find())

    return render_template("review-game-search.html", user=user, username=username,
                            latest_games=latest_games, allgames=allgames)


@app.route("/gameSearch", methods=["GET", "POST"])
def gameSearch():
    """
    Takes a POST to load a page containing the results of a game search
    reloads the review-game-search page
    """
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))

    allgames = list(mongo.db.games.find())

    gameName = request.form.get("search")
    games = list(mongo.db.games.find({"$text": {"$search": gameName}}))

    reviews = list(mongo.db.reviews.find({'review_by': session['user']}))
    return render_template("review-game-search.html", user=user, username=username,
                            latest_games=latest_games, games=games, allgames=allgames, reviews=reviews)


@app.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    """
    Go to a page displaying a game based off the game_id provided
    """
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    reviews = list(mongo.db.reviews.find())

    def getReviewforGame(reviews):
        for review in reviews:
            if review["game_title"] == game["title"]:
                return review
    if session.get('user'):
        userReviews = list(mongo.db.reviews.find({'review_by': session['user']}))
        userGameReview = getReviewforGame(userReviews)
    else:
        userGameReview = None

    return render_template("game.html", game=game, reviews=reviews, 
                            userGameReview=userGameReview)


@app.route("/editGame/<game_id>", methods=["GET", "POST"])
def editGame(game_id):

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    if request.method == "POST":
        # gets the current date.time
        now = datetime.now()
        # dd/mm/YY H:M:S
        currenttime = now.strftime("%d/%m/%Y %H:%M:%S")

        update = {
            "year": request.form.get("game_year"),
            "description": request.form.get("game_description"),
            "largeImage": request.form.get("game_large_image"),
            "background": request.form.get("game_background"),
        }
        # Pushes the update to the db
        mongo.db.games.update({"_id": ObjectId(game_id)}, {"$set": update})

        # Adds the user who updated the game and the time/date
        mongo.db.games.update_one({"_id": ObjectId(game_id)}, {"$push": { 'updated_by': {
            'username': session['user'],
            'time': currenttime
            }}})
        flash("Game Updated")

        return redirect(url_for('game', game_id=game_id))

    # gets the last peson to have updated the game
    updated = list(game['updated_by'])
    for i in range(0, len(updated)):
        if i == (len(updated)-1):
            updated_by = updated[i]

    return render_template("edit-game.html", game=game, updated_by=updated_by)


@app.route("/changePass", methods=["GET", "POST"])
def changePass():
    """
    Go to a page to change password of account. TAkes a POST
    """
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()
    userPass = mongo.db.gc_users.find_one(
        {"username": session["user"]})["password"]

    if request.method == "POST":
        if check_password_hash(userPass, request.form.get("originalPassword")):
            mongo.db.gc_users.update_one({"username": username}, {"$set": {"password": generate_password_hash(request.form.get("password"))}})
            flash("Password Updated")
        else:
            flash('Password Incorrect')
    return render_template("changepass.html", user=user, username=username.capitalize(), latest_games=latest_games)


@app.route('/addReview/<game_id>', methods=["GET", "POST"])
def add_review(game_id):
    """
    Go to a page to add a review to a game based on game_id
    """
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
        game = mongo.db.games.find_one(
            {"title": game['title']})

        # redirected to game page
        return redirect(url_for('game', game_id=game['_id']))

    return render_template("add-review.html", game=game)


@app.route("/yourReviews")
def yourReviews():
    """
    Go to a page displaying all reviews linked to the session.user
    extends the profile page
    """
    # gets the latest games in revers order. Max of 5
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))

    # gets the user matching the session user
    user = mongo.db.gc_users.find_one(
        {"username": session["user"]})
    username = user['username'].capitalize()

    # gets all review by the user
    your_reviews = list(mongo.db.reviews.find({'review_by': session['user']}))

    return render_template("your-reviews.html", your_reviews=your_reviews,
                            latest_games=latest_games, username=username, user=user)


@app.route("/review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    """
    Go to a page to edit a review based on it's review_id
    """
    if request.method == "POST":
        """
        Gets values from form and update the relevant
        review with them
        """
        # Update key value pairs from form
        update = {
            "review_message": request.form.get("review_message"),
            "review_rating": request.form.get("review_rating"),
            "review_by": session['user'],
            "game_title": request.form.get("game_title"),
            "review_title": request.form.get("review_title")
        }
        # Updates the review with matching _id with update dict
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, update)
        flash("Review Updated")

        # gets the game id with the matching title
        game_id = mongo.db.games.find_one({"title": request.form.get("game_title")})['_id']

        return redirect(url_for('game', game_id=game_id))
    
    # finds a review with matching _id
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    return render_template("edit-review.html", review=review)


@app.route("/deleteReview/<review_id>")
def delete_review(review_id):
    """
    From a button to delete the selected review based on review_id
    """
    # Removes the review with atching _id
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Deleted")

    return redirect(url_for("yourReviews"))


@app.route("/logout")
def logout():
    """
    From a button removes the sessions cookie
    """
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/latest_reviews")
def latest_reviews():
    """
    Goes to page container all reviews
    with newest first
    """
    # gets all reviews, newest first
    latest_reviews = list(mongo.db.reviews.find().sort("_id", -1))
    # gets all games
    games = list(mongo.db.games.find())

    return render_template("latest-reviews.html", latest_reviews=latest_reviews, games=games)


@app.route("/games", methods=["GET", "POST"])
def games():

    genres = []

    games = list(mongo.db.games.find())
    for game in games:
        x = game['genres']
        for genre in x:
            if genre['name'] not in genres:
                genres.append(genre['name'])
    print(genres)

    if request.method == "POST":
        # Gets all games containing the search term
        filteredGames = list(mongo.db.games.find({"$text": {"$search": request.form.get('name_of_game')}}).sort("title", 1))
        return render_template("games.html", allGames=filteredGames, genres=genres)

    # Gets all games sorted by title
    allGames = list(mongo.db.games.find().sort("title", 1))

    return render_template("games.html", allGames=allGames, genres=genres)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
