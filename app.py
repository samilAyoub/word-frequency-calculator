import logging
import operator
import os
import re
from collections import Counter

import nltk
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

import exceptions
from models import db
from stop_words import stops

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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


def html_text_preprocessing(html_text):
    """
    Count words in a HTML text.

    :param html_text: HTML text
    :type html_text: String
    :returns: Count each word in HTML text
    :rtype: Counter
    """

    # Clean text by removing HTML tags.
    raw = BeautifulSoup(html_text, 'html.parser').get_text()
    logger.debug('Text after removing HTML tags from: %s', raw[:100])
    # Set ntlk path.
    nltk.data.path.append('./nltk_data/')
    tokens = nltk.word_tokenize(raw)
    logger.debug('Text tokens: %s', tokens[:100])
    nltk_text = nltk.Text(tokens)
    # Remove punctuation.
    no_punct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in nltk_text if no_punct.match(w)]
    # Eliminate stop words.
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)
    logger.debug('10 most common elements: %s',
                 no_stop_words_count.most_common(10))
    return no_stop_words_count


@app.route("/", methods=['POST', 'GET'])
def hello():
    errors = []
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
        if r:
            html_text_preprocessing(r.text)
    return render_template('index.html')


if __name__ == "__main__":
    init_db()
    app.run()
