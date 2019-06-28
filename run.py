from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from googlesearch import search
import requests
import json
import lxml
from lxml import html
from bs4 import BeautifulSoup
import re
from urllib3.exceptions import HTTPError as BaseHTTPError
from nltk.corpus import stopwords

app = Flask(__name__)

# Default delimiter to delineate primary key fields in string.
key_delimiter = "_"

# Google Search URL
URL = "http://www.google.com"

# Get stopwords
stop_words = set(stopwords.words('english'))


# Search by using requests
def google_query1(query):

    url = []

    # Form a url
    url_search = URL + "/search?q="
    q = url_search + query.replace(" ", "+")

    # Search on google
    r = requests.get(url=q, params=None)

    # extract all the URL we fin
    soup = BeautifulSoup(r.text, features="lxml")
    for link in soup.findAll('a'):
        str_link = str(link)
        if "https:" in str_link and \
           "/url?q=" in str_link and \
           "https://www.youtube.com" not in str_link and \
           "https://accounts.google.com" not in str_link:

            url_wo_q = str_link.split("/url?q=")[1]
            clean_url = url_wo_q.split("&amp")[0]

            url.append(clean_url)

    return url

# Search by using google api
def google_query2(query):

    url = []

    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    # to search
    for link in search(query, tld="com", num=100, start=0, stop=10, pause=1):
        str_link = str(link)
        if "https://www.youtube.com" not in str_link and \
            "https://accounts.google.com" not in str_link:
            url.append(str_link)

    return url

# Get Clean Text
def clean_text(url):
    one_page_text = ""

    for query in url:
        # Search on google
        res = requests.get(url=query, params=None)

        # extract all the URL we fin
        soup = BeautifulSoup(res.text, features="lxml")

        for node in soup.findAll('p'):
            one_page_text += ' '.join(node.findAll(text=True))

        print(one_page_text)


@app.route('/search',  methods = ['POST', 'GET'])
def handle_search():
    try:
        search_content = request.form['search_content']

    except ValueError:
        return render_template('index.html')

    try:
        url = google_query2()

        # Get list of relevant words

        # From a image

    except requests.HTTPError:

        url = google_query1()


    except:
        return render_template("error.html", ERROR_CODE=1)

    return "hello"





@app.route('/', methods = ['POST', 'GET'])
@app.route('/home', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
def handle_home():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run()