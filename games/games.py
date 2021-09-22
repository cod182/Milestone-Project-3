import os
from database import mongo
import requests
import helpers
from flask import (
    flash, render_template, redirect,
    request, session, url_for, Blueprint)
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

games = Blueprint(
    "games",
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/games/static')


RAWG_API = os.environ.get("RAWG_API_KEY")


@games.route("/user/game-search", methods=["GET", "POST"])
def game_lookup():
    if request.method == "POST":
        search = request.form.get("game-name")
        try:
            response = requests.get(
                "https://api.rawg.io/api/games"
                + "?key="
                + RAWG_API
                + '&search='
                + search
            )
            gameData = response.json()

            return render_template('select-game.html', gameData=gameData)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    return render_template('lookup-game.html')


@games.route('/user/add-game', methods=["GET", "POST"])
def add_game():
    """
    Added a new game to the database
    """
    if request.method == "POST":
        # Checks if game already exists in database
        existing_game = getGameByGameId(int(request.form.get('selected-game')))

        if existing_game:
            flash('Game Already Exists')
            return redirect(url_for('games.game_lookup'))

        # Gets game id from page, makes and API call to get details
        gameId = request.form.get('selected-game')
        apiCall = requests.get(
            "https://api.rawg.io/api/games/"
            + gameId
            + "?key="
            + RAWG_API
        )
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
        game = getGameByGameId(data['id'])

        currenttime = getDate()

        # Adds the user who added the game and the time/date
        mongo.db.games.update_one(
            {"_id": ObjectId(game['_id'])},
            {"$push": {'updated_by': {
                'username': session['user'],
                'time': currenttime
                }
            }})

        # redirected to game page
        return redirect(url_for('games.game', game_id=game['_id']))

    return render_template('add-game.html')


@games.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    """
    Go to a page displaying a game based off the game_id provided
    """
    # Gets the game by the id
    game = helpers.getGameByObjectId(game_id)
    # gets all reviews
    reviews = helpers.getAllUserReviews()
    # gets all users
    allUsers = helpers.getAllUsers()

    # If a user is logged in
    if session.get('user'):
        # Gets the session user
        user = helpers.getUserFromSessionUser(session['user'])

        userReviews = helpers.getUserReviews(session['user'])
        # Gets reviews for the game
        userGameReview = helpers.getReviewforGame(userReviews, game)
    else:
        userGameReview = None
        user = None

    gameRating = helpers.getGameRatingFromReviews(reviews, game)
    # Add all ints in gameRating and divide by length
    # getting average
    if gameRating:
        usersRating = int(sum(gameRating) / len(gameRating))
    else:
        usersRating = 'N/A'

    return render_template(
        "game.html",
        game=game,
        reviews=reviews,
        userGameReview=userGameReview,
        user=user,
        usersRating=usersRating,
        gameRating=gameRating,
        allUsers=allUsers
    )


@games.route("/user/edit-game-details/<game_id>", methods=["GET", "POST"])
def edit_game_details(game_id):
    # Finds the game by it's _id
    game = helpers.getGameByObjectId(game_id)

    if request.method == "POST":
        # gets the current date.time
        currenttime = getDate()

        update = {
            "year": request.form.get("game_year"),
            "description": request.form.get("game_description"),
            "largeImage": request.form.get("game_large_image"),
            "background": request.form.get("game_background"),
        }
        # Pushes the update to the db
        mongo.db.games.update({"_id": ObjectId(game_id)}, {"$set": update})

        # Adds the user who updated the game and the time/date
        mongo.db.games.update_one(
            {"_id": ObjectId(game_id)},
            {"$push": {
                'updated_by': {
                    'username': session['user'],
                    'time': currenttime
                }
            }}
        )
        flash("Game Updated")

        return redirect(url_for('games.game', game_id=game_id))

    # gets the last peson to have updated the game
    updated = list(game['updated_by'])
    for i in range(0, len(updated)):
        if i == (len(updated)-1):
            updated_by = updated[i]

    return render_template("edit-game.html", game=game, updated_by=updated_by)


@games.route("/latest-reviews")
def get_latest_reviews():
    """
    Goes to page container all reviews
    with newest first
    """
    if session.get('user'):
        # Gets the session user
        user = mongo.db.gc_users.find_one(
            {"username": session["user"]})
    else:
        user = None

    # gets all reviews, newest first
    latest_reviews = list(mongo.db.reviews.find().sort("_id", -1))
    # gets all games
    games = list(mongo.db.games.find())
    # gets all the db users
    allUsers = list(mongo.db.gc_users.find())

    return render_template(
        "latest-reviews.html",
        latest_reviews=latest_reviews,
        games=games,
        user=user,
        allUsers=allUsers
    )


@games.route("/games", methods=["GET", "POST"])
def get_all_games():

    # Gets all games sorted by title
    allGames = list(mongo.db.games.find().sort("title", 1))

    genres = []

    games = list(mongo.db.games.find())
    for game in games:
        x = game['genres']
        for genre in x:
            if genre['name'] not in genres:
                genres.append(genre['name'])

    if request.method == "POST":
        if request.form.get('name_of_game'):
            # Gets all games containing the search term
            filteredGames = list(mongo.db.games.find(
                {"$text": {
                    "$search": request.form.get(
                        'name_of_game')}}).sort(
                            "title", 1))
            return render_template(
                "games.html",
                allGames=filteredGames,
                genres=genres
            )
        flash('No Game Found')
        return render_template(
            "games.html",
            allGames=allGames,
            genres=genres
        )

    return render_template("games.html", allGames=allGames, genres=genres)
