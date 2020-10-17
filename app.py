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
from models import db, Result
from stop_words import stops

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Make sure we use the right environment
app.config.from_object(os.environ["APP_SETTINGS"])

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def request_handler(url):
    """
    Handle get requests.

    :param url: URL of a web page
    :type url: String
    :returns: response of get request
    :rtype: Response
    :raises GetRequestException: if get request failed
    """
    try:
        r = requests.get(url)
        # r.raise_for_status()
    except requests.exceptions.RequestException as e:
        msg = str(e)
        raise exceptions.GetRequestException(url, msg)
    return r


def k_most_commons(html_text, k):
    """
    Return k most common words in a given HTML text.

    :param html_text: HTML text
    :param k: Number of most common words to return
    :type html_text: String
    :type k: int
    :returns: List of tuples, each tuple have tow elements. First one is the 
    word, and the second one is its number of occurrences.
    :rtype: List
    """

    # Clean text by removing HTML tags.
    logger.debug('Text length: %s', len(html_text))
    raw = BeautifulSoup(html_text, 'html.parser').get_text()
    logger.debug('Text length after deleting HTML tags: %s', len(raw))
    # Set ntlk path.
    nltk.data.path.append('./nltk_data/')
    tokens = nltk.word_tokenize(raw)
    logger.debug('Tokens length: %s', len(tokens))
    nltk_text = nltk.Text(tokens)
    # Remove punctuation.
    no_punct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in nltk_text if no_punct.match(w)]
    # Eliminate stop words.
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)
    return no_stop_words_count.most_common(k)


def store_results(url, result):
    """
    Store a given result to database.

    :param url: URL of the web page, where the result come from
    :type url: String
    :param result: the result we want to store
    :type result: dict
    """
    try:
        result = Result(url=url, result=result)
        db.session.add(result)
        db.session.commit()
    except Exception as e:
        msg = str(e)
        raise exceptions.StoreResultException(result, msg)


@app.route("/", methods=['POST', 'GET'])
def hello():
    result = []
    errors = []
    if request.method == 'POST':
        # Get URL that user has entred
        url = request.form['url']
        logger.debug('URL entred: %s', url)
        try:
            r = request_handler(url)
        except exceptions.GetRequestException as e:
            msg = str(e)
            errors.append(msg)
        if r:
            # Get 10 most common words.
            result = k_most_commons(r.text, 10)
            logger.debug("10 most common words: %s", result)
            try:
                store_results(url, result)
                logger.debug("Result stored in database")
            except exceptions.StoreResultException as e:
                msg = str(e)
                errors.append(msg)
                logger.debug("Store result error: %s", msg)

    return render_template('index.html', errors=errors, result=result)
