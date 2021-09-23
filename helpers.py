from database import mongo, cache
from flask import (session)
from bson.objectid import ObjectId
from datetime import datetime
import time
import requests


def get_user_from_session_user(user):
    # Gets a user in the DB from the session user's name
    return mongo.db.gc_users.find_one({"username": session["user"]})


def get_one_user_by_username(name):
    # gets one user by username
    return mongo.db.gc_users.find_one({"username": name})


def get_user_by_id(id):
    # gets a user by a object id
    return mongo.db.gc_users.find_one({"_id": ObjectId(id)})


def get_user_list_by_username(name):
    return list(mongo.db.gc_users.find({"username": name}))


def get_all_users():
    # Gets all the users in the DB
    return list(mongo.db.gc_users.find())


def remove_user_by_object_id(id):
    """Removes a games from the database

    Args:
        id (-id): [Object id for a game]
    """
    mongo.db.gc_users.remove({"_id": ObjectId(id)})


def get_all_games():
    """Returns a list of all games in db

    Returns:
        [list]: [Games in databse]
    """
    return list(mongo.db.games.find())


def get_all_genres_of_games():
    """Gets all the individual genres in
    the databse from games

    Returns:
        [list]: [unique game genres]
    """
    genres = []

    games = get_all_games()
    for game in games:
        x = game['genres']
        for genre in x:
            if genre['name'] not in genres:
                genres.append(genre['name'])
    return genres


def get_game_by_game_name(title):
    return mongo.db.games.find_one({"title": title})


def get_game_by_object_id(id):
    # gets the game by it's _id
    return mongo.db.games.find_one({"_id": ObjectId(id)})


def get_game_by_game_id(id):
    # Gets the game by it's game_id
    return mongo.db.games.find_one({"game_id": id})


def remove_game_by_objectId(id):
    # removes a game by it's object id
    mongo.db.games.remove({"_id": ObjectId(id)})


def list_of_games_by_title_indexed(title):
    # gets a list fo games by title using an index
    return list(mongo.db.games.find({"$text": {"$search": title}}))


@cache.cached(timeout=21600)
def get_latest_games():
    print('getting latest games')
    return list(mongo.db.games.find().sort("_id", -1).limit(5))


def call_rawg_api_for_games(key, param, search):
    # Calls the RAWG API with a search term
    try:
        response = requests.get(
            "https://api.rawg.io/api/games"
            + param
            + search
            + "key="
            + key
        )
    except Exception as e:
        print(e, response.status)

    return response.json()


def insert_game_into_game_db(data):
    """[summary]

    Args:
        data ([dict]): [dict of new game information]
    Desc:
        Adds new game into database
    """
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
            "metacritic": data['metacritic'],
            "updated_by": [{
                'username': session['user'],
                'time': get_date()
                }]
        }
    # Game inserted into database
    mongo.db.games.insert(newGame)


def remove_game_reviews_by_title(title):
    # Removes a games review by the game's title
    mongo.db.reviews.remove({'game_title': title})


def get_date():
    # Gets the current date/time
    uk_date_time = datetime.now()
    # dd/mm/YY H:M:S
    return uk_date_time.strftime("%d/%m/%Y %H:%M:%S")


def get_user_reviews_for_game_by_title(reviews, game):
    """
    Goes through reviews matching to game title
    returns matches
    """
    for review in reviews:
        if review["game_title"] == game["title"]:
            return review


def get_review_by_object_id(id):
    # gets the review with the object id
    return mongo.db.reviews.find_one({"_id": ObjectId(id)})


def get_all_user_reviews():
    # Gets all the user reviews in the DB
    return list(mongo.db.reviews.find())


def get_user_reviews(user):
    # Gets all of the current users reviews
    return list(mongo.db.reviews.find({'review_by': user}))


def remove_reviews_by_user(name):
    # gets reviews by the user name of reviewer
    mongo.db.reviews.remove({'review_by': name})


def remove_review_by_object_id(id):
    # Removes a review with matching object ID
    mongo.db.reviews.remove({"_id": ObjectId(id)})


def get_game_reviews_by_title(game):
    # gets review matching the game_title
    return list(mongo.db.reviews.find({"game_title": game}))


def get_game_rating_from_reviews(reviews, game):
    # List for all ratings of game
    gameRating = []
    # get the rating from each review and push to gameRating
    for review in reviews:
        if review["game_title"] == game["title"]:
            gameRating.append(int(review["review_rating"]))
    return gameRating


def get_profile_images():
    # gets all the progile imaeges in db
    return list(mongo.db.profile_images.find())


def check_for_existing_user_by_name(name):
    # Checks if a user exists in db
    return mongo.db.gc_users.find_one({"username": name})
