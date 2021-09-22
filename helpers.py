from database import mongo
from flask import (session)
from bson.objectid import ObjectId
from datetime import datetime


def get_user_from_session_user(user):
    # Gets a user in the DB from the session user's name
    return mongo.db.gc_users.find_one({"username": session["user"]})


def get_all_users():
    # Gets all the users in the DB
    return list(mongo.db.gc_users.find())


def get_all_user_reviews():
    # Gets all the user reviews in the DB
    return list(mongo.db.reviews.find())


def get_user_reviews(user):
    # Gets all of the current users reviews
    return list(mongo.db.reviews.find({'review_by': session['user']}))


def get_all_games():
    return list(mongo.db.games.find())


def get_game_by_object_id(id):
    # gets the game by it's _id
    return mongo.db.games.find_one({"_id": ObjectId(id)})


def get_game_by_game_id(id):
    # Gets the game by it's game_id
    return mongo.db.games.find_one({"game_id": id})


def get_date():
    # Gets the current date/time
    now = datetime.now()
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")


def get_reviews_for_game(reviews, game):
    """
    Goes through reviews matching to game title
    returns matches
    """
    for review in reviews:
        if review["game_title"] == game["title"]:
            return review


def get_game_rating_from_reviews(reviews, game):
    # List for all ratings of game
    gameRating = []
    # get the rating from each review and push to gameRating
    for review in reviews:
        if review["game_title"] == game["title"]:
            gameRating.append(int(review["review_rating"]))
    return gameRating
