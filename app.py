import os
from flask import (Flask, url_for, render_template)
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


@app.route("/")
@app.route("/base")
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
