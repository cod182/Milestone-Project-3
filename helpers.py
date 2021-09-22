from database import mongo
from flask import (session)
from bson.objectid import ObjectId
from datetime import datetime


def getUserFromSessionUser(user):
    # Gets a user in the DB from the session user's name
    return mongo.db.gc_users.find_one({"username": session["user"]})


def getAllUsers():
    # Gets all the users in the DB
    return list(mongo.db.gc_users.find())


def getAllUserReviews():
    # Gets all the user reviews in the DB
    return list(mongo.db.reviews.find())


def getUserReviews(user):
    # Gets all of the current users reviews
    return list(mongo.db.reviews.find({'review_by': session['user']}))


def getGameByObjectId(id):
    # gets the game by it's _id
    return mongo.db.games.find_one({"_id": ObjectId(id)})


def getGameByGameId(id):
    # Gets the game by it's game_id
    return mongo.db.games.find_one({"game_id": id})


def getDate():
    # Gets the current date/time
    now = datetime.now()
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")


def getReviewforGame(reviews, game):
    """
    Goes through reviews matching to game title
    returns matches
    """
    for review in reviews:
        if review["game_title"] == game["title"]:
            return review


def getGameRatingFromReviews(reviews, game):
    # List for all ratings of game
    gameRating = []
    # get the rating from each review and push to gameRating
    for review in reviews:
        if review["game_title"] == game["title"]:
            gameRating.append(int(review["review_rating"]))
    return gameRating
