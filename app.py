import os
from flask import (
    Flask,  render_template)
from admin.admin import admin
from games.games import games
from users.users import users
if os.path.exists("env.py"):
    import env
from database import mongo

app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(games)


app.config['MONGO_DBNAME'] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
RAWG_API = os.environ.get("RAWG_API_KEY")

mongo.init_app(app)


@app.route("/")
@app.route("/index")
def index():
    """
    Go to a page to display the home screen
    """
    # gets the latest 5 games
    latest_games = list(mongo.db.games.find().sort("_id", -1).limit(5))

    return render_template("index.html", latest_games=latest_games)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
