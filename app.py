import logging
import operator
import os
import re
from collections import Counter

import nltk
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

from exceptions import GetRequestException, StoreResultException
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
    :type url: str
    :returns: response of get request
    :rtype: Response
    :raises GetRequestException: if get request failed
    """
    try:
        r = requests.get(url)
        # r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise GetRequestException(url, str(e))
    return r


def k_most_commons(html_text, url, k=10, store=True):
    """
    Return k most common words in a given HTML text.

    :param html_text: HTML text
    :param url: URL of the web page, where HTML text is scraped
    :param k: Number of most common words to return
    :param store: An option to store or not the result in database
    :type html_text: str
    :type k: int
    :type store: boolean
    :returns: List of tuples, each tuple have tow elements. First one is the 
    word, and the second one is its number of occurrences.
    :rtype: List
    :raises StoreResultException: If storing the result in database is failed
    """

    logger.debug('Text length: %s', len(html_text))
    # Clean text by removing HTML tags.
    raw = BeautifulSoup(html_text, 'html.parser').get_text()
    logger.debug('Text length after deleting HTML tags: %s', len(raw))
    # Set ntlk path.
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
        logger.info("Downloading punkt ...")
    tokens = nltk.word_tokenize(raw)
    logger.debug('Tokens length: %s', len(tokens))
    nltk_text = nltk.Text(tokens)
    # Remove punctuation.
    no_punct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in nltk_text if no_punct.match(w)]
    # Eliminate stop words.
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    result = Counter(no_stop_words).most_common(k)
    if store:
        try:
            store_results(url, result)
            logger.info("Result stored in database")
        except StoreResultException as e:
            logger.exception(str(e))
            raise e
    return result


def store_results(url, result):
    """
    Store a given result in database.

    :param url: URL of the web page, where the result come from
    :type url: str
    :param result: the result we want to store
    :type result: dict
    """
    try:
        result = Result(url=url, result=result)
        db.session.add(result)
        db.session.commit()
    except Exception as e:
        raise StoreResultException(result.result, str(e))


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
            # Get 10 most common words.
            result = k_most_commons(r.text, url)
            logger.debug("10 most common words: %s", result)
        except GetRequestException as e:
            logger.exception(str(e))
            errors.append("Request Failed.")
        except StoreResultException:
            errors.append("Error while storing the result.")

    return render_template('index.html', errors=errors, result=result)
