from database import mongo, cache
from flask import (session, flash)
from bson.objectid import ObjectId
from datetime import datetime
import requests
from requests.exceptions import HTTPError
import os
if os.path.exists("env.py"):
    import env


def remove_user_by_object_id(id):
    """Removes a games from the database

    Args:
        id (-id): [Object id for a game]
    """
    mongo.db.gc_users.remove({"_id": ObjectId(id)})


@cache.cached(timeout=1300, key_prefix='all_games')
def get_all_games():
    """Returns a list of all games in db

    Returns:
        [list]: [Games in databse]
    """
    return list(mongo.db.games.find())


def get_pag_list(offset=0, per_page=10, list=None):
    return list[offset: offset + per_page]


@cache.cached(timeout=1300, key_prefix='all_genres')
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


@cache.cached(timeout=21600, key_prefix='latest_games')
def get_latest_games():
    return list(mongo.db.games.find().sort("_id", -1).limit(5))


def call_rawg_api_for_games(key, param, search):
    """[calls rawg api for information on searched game]

    Args:
        key ([API Key]): [The api key for RAWG]
        param ([string]): [search parameter]
        search ([string]): [game / id to search]

    Returns:
        [json list]: [details of searched game]
    """
    try:
        response = requests.get(
            "https://api.rawg.io/api/games"
            + param
            + search
            + "key="
            + key
        )
        response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        flash(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        flash(f'Error occurred: {err}')
        return None
    return response.json()


def call_youtube_api_for_game(game, key):
    """[Calls youtube for IGN's videos relating to
    the given game]

    Args:
        game ([string]): [game title to search]

    Returns:
        [json list]: [list of 2 videos]
    """
    try:
        search_url = "https://www.googleapis.com/youtube/v3/search"

        search_params = {
            'key': key,
            'part': "snippet",
            'channelId': "UCKy1dAqELo0zrOtPkf0eTMw",
            'maxResults': 2,
            'q': game
        }

        response = requests.get(search_url, params=search_params)

        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None
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


def get_game_rating_from_reviews(reviews, game):
    # List for all ratings of game
    gameRating = []
    # get the rating from each review and push to gameRating
    for review in reviews:
        if review["game_title"] == game["title"]:
            gameRating.append(int(review["review_rating"]))
    return gameRating


@cache.cached(timeout=86400, key_prefix='profile_images')
def get_profile_images():
    # gets all the progile imaeges in db
    return list(mongo.db.profile_images.find())
