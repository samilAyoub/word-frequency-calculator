import logging
import operator
import os
import re
from collections import Counter
import exceptions
import nltk
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

from models import db

app = Flask(__name__)

# Make sure we use the right environment
app.config.from_object(os.environ["APP_SETTINGS"])

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def init_db():
    db.init_app(app)
    db.create_all()


def request_handler(url):
    try:
        r = requests.get(url)
        # r.raise_for_status()
    except requests.exceptions.RequestException as e:
        msg = str(e)
        raise exceptions.GetRequestException(url, msg)
    return r


@app.route("/", methods=['POST', 'GET'])
def hello():
    errors = []
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        # Get URL that user has entred
        url = request.form['url']
        logger.debug('URL entred: %s', url)
        try:
            r = request_handler(url)
            logger.debug('Response: %s', len(r.text))
        except exceptions.GetRequestException as e:
            msg = str(e)
            errors.append(msg)
    return render_template('index.html')


if __name__ == "__main__":
    init_db()
    app.run()
