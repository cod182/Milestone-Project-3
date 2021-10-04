import os
from database import mongo
import helpers
from bson import ObjectId
from flask_paginate import Pagination, get_page_args
from flask import (
    flash, render_template, redirect,
    request, session, url_for, Blueprint)
if os.path.exists("env.py"):
    import env

games = Blueprint("games", __name__, template_folder='templates',
                  static_folder='static',
                  static_url_path='/games/static')


RAWG_API_KEY = os.environ.get("RAWG_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


@games.route("/user/game-search", methods=["GET", "POST"])
def game_lookup():
    """[Searches for a game by a name, using the RAWG
    API, restuning a JSON of the results]

    Returns:
        [html]: [Page for look initial, then game selection after
        POST]
    """
    if request.method == "POST":
        search = request.form.get("game-name")

        game_data = helpers.call_rawg_api_for_games(
            RAWG_API_KEY,
            '?search=',
            search + '&')

        return render_template('select-game.html', game_data=game_data)

    return render_template('lookup-game.html')


@games.route('/user/add-game', methods=["GET", "POST"])
def add_game():
    """[Adds a game to the games DB after a check if it alraedy exists
    Inserts predefined data from JSON results]

    Returns:
        [html]: [retuns page to add game initial, then redirects to
        the game's page after POST]
    """
    if request.method == "POST":

        existing_game = mongo.db.games.find_one(
            {"game_id": int(request.form.get('selected-game'))})

        if existing_game:
            flash('Game Already Exists')
            return redirect(url_for('games.game_lookup'))

        game_id = request.form.get('selected-game')
        data = helpers.call_rawg_api_for_games(
            RAWG_API_KEY, '/', game_id + '?')
        helpers.insert_game_into_game_db(data)
        game = helpers.mongo.db.games.find_one({"game_id": data['id']})

        return redirect(url_for('games.game', game_id=game['_id']))

    return render_template('add-game.html')


@games.route("/game/<game_id>", methods=["GET", "POST"])
def game(game_id):
    """[Goes to a the game page of the game with
    the the game_id. Gets all the reviews and all the users.
    Calls teh Youtube API to get gameplay videso from IGN]

    Args:
        game_id (_id): [The _id of a specific game]

    Returns:
        [render_template]: [renders the game's page.
        If the game no longer exosts, returns index]
    """
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    all_users = list(mongo.db.gc_users.find())

    if game:

        reviews = list(mongo.db.reviews.find({"game_title": game['title']}))
        total = len(reviews)
        page, per_page, offset = get_page_args(
            page_parameter='page', per_page_parameter='per_page')
        pagination_reviews = helpers.get_pag_list(offset=offset,
                                                  per_page=per_page,
                                                  list=reviews)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')

        videos = helpers.call_youtube_api_for_game(
            game['title'], YOUTUBE_API_KEY)

        if session.get('user'):
            user = mongo.db.gc_users.find_one({"username": session["user"]})
            user_reviews = list(mongo.db.reviews.find(
                {'review_by': session['user']}))
            user_game_review = helpers.get_user_reviews_for_game_by_title(
                user_reviews, game)
        else:
            user_game_review = None
            user = None
        all_reviews = list(mongo.db.reviews.find())
        game_rating = helpers.get_game_rating_from_reviews(all_reviews, game)
        if game_rating:
            usersRating = int(sum(game_rating) / len(game_rating))
        else:
            usersRating = 'N/A'

        return render_template("game.html", game=game,
                               pagination_reviews=pagination_reviews,
                               pagination=pagination,
                               user_game_review=user_game_review, user=user,
                               usersRating=usersRating,
                               game_rating=game_rating,
                               all_users=all_users, videos=videos)

    return redirect(url_for('index'))


@games.route("/user/edit-game-details/<game_id>", methods=["GET", "POST"])
def edit_game_details(game_id):
    """[Allos a user to edit some details of the selected game.
    User who edited game is also logged]

    Args:
        game_id ([Object_id]): [THe object_id of the game
        to be edited]

    Returns:
        [html]: [retuns the edit page html first. After POST redirects
        to the game's page]
    """
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})

    if request.method == "POST":
        current_time = helpers.get_date()
        update = {
            "year": request.form.get("game_year"),
            "description": request.form.get("game_description"),
            "largeImage": request.form.get("game_large_image"),
            "background": request.form.get("game_background"),
        }
        mongo.db.games.update({"_id": ObjectId(game_id)}, {"$set": update})
        mongo.db.games.update_one(
            {"_id": ObjectId(game_id)},
            {"$push": {
                'updated_by': {
                    'username': session['user'],
                    'time': current_time
                }
            }}
        )
        flash("Game Updated")

        return redirect(url_for('games.game', game_id=game_id))

    updated = list(game['updated_by'])
    for i in range(0, len(updated)):
        if i == (len(updated)-1):
            updated_by = updated[i]

    return render_template("edit-game.html", game=game, updated_by=updated_by)


@games.route("/latest-reviews")
def get_latest_reviews():
    """[Page with the latet 9 reviews over all games]

    Returns:
        [html]: [page of latest 9 reviews]
    """
    if session.get('user'):
        user = mongo.db.gc_users.find_one({"username": session["user"]})
    else:
        user = None

    latest_reviews = list(mongo.db.reviews.find().sort("_id", -1).limit(9))
    games = list(mongo.db.games.find())
    all_users = list(mongo.db.gc_users.find())

    return render_template("latest-reviews.html",
                           latest_reviews=latest_reviews,
                           games=games, user=user,
                           all_users=all_users
                           )


@games.route("/games", methods=["GET", "POST"])
def get_all_games():
    """[Show all game sorted by their titles.
    Page is paginated for 10 games per page]

    Returns:
        [html]: [Page container all games]
    """

    games_list = list(mongo.db.games.find().sort("title", 1))

    total = len(games_list)
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    pagination_games = helpers.get_pag_list(offset=offset,
                                            per_page=per_page, list=games_list)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    if request.method == "POST":
        if request.form.get('name_of_game'):
            filtered_games = list(mongo.db.games.find(
                {"$text": {
                    "$search": request.form.get(
                        'name_of_game')}}).sort(
                            "title", 1))
            return render_template(
                "games.html",
                pagination_games=filtered_games,
                pagination=None
            )
        flash('No Game Found')
        return redirect(url_for('games.get_all_games'))

    return render_template("games.html", pagination_games=pagination_games,
                           pagination=pagination, page=page, per_page=per_page)
