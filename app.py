import os

from flask import Flask

app = Flask(__name__)

# Make sure we use the right environment
app.config.from_object(os.environ["APP_SETTINGS"])


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
