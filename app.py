import os

from flask import Flask

from models import db

app = Flask(__name__)

# Make sure we use the right environment
app.config.from_object(os.environ["APP_SETTINGS"])

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def init_db():
    db.init_app(app)
    db.create_all()


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    init_db()
    app.run()
