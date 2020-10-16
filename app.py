import os

from flask import Flask, render_template

from models import db

app = Flask(__name__)

# Make sure we use the right environment
app.config.from_object(os.environ["APP_SETTINGS"])

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def init_db():
    db.init_app(app)
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    init_db()
    app.run()
