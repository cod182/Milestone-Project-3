from dotenv import load_dotenv
import os
from flask import (
    Flask,  render_template)
from admin.admin import admin
from games.games import games
from users.users import users
from database import mongo, cache
import helpers

load_dotenv()



app = Flask(__name__)
app.register_blueprint(admin, url_prefix='')
app.register_blueprint(users, url_prefix='')
app.register_blueprint(games, url_prefix='')

app.config['CACHE_TYPE'] = 'simple'
app.config['MONGO_DBNAME'] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo.init_app(app)
cache.init_app(app)


@app.route("/")
@app.route("/index")
def index():
    """[Give the home page]

    Returns:
        [html]: [home page of site]
    """
    latest_games = helpers.get_latest_games()
    return render_template("index.html", latest_games=latest_games)


@app.errorhandler(404)
def page_not_found(e):
    """[If a 404 error page]

    Args:
        e ([error]): [error type]

    Returns:
        [html]: [404 error page]
    """
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
