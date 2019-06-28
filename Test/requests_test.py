import requests
from requests import Request
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from googlesearch import search
import urllib
from urllib.request import urlopen
import lxml
from lxml import html
import re
from requests_html import HTMLSession

URL = "http://www.google.com"
URL_GIT= 'https://github.com'

def test_GIT():
    r = requests.get(URL_GIT)
    print("Status Code: ", r.status_code)
    print(r.headers)


def test_google():
    r = requests.get(URL, params=None)
    print("Status Code: ", r.status_code)
    print(r.headers)


# failed connect server xxxxxxxx
def test_google_search():
    num_page = 3
    search_results = search("This is my query", num_page)
    for result in search_results:
        print(result.description)


# test_GIT()
# test_google()
# test_google_search()


"""
    r = urlopen(q)
    soup = BeautifulSoup(r, features="lxml")
    for link in soup.findAll('a'):
        print(link.get('href'))

    print('\n\n')
"""

def google_query(query):
    url = "https://www.google.com"
    url_search = url + "/search?q="
    q = url_search + query.replace(" ", "+")
    r = requests.get(url = q, params=None)
    print(r.status_code)
    print(r.text)

    soup = BeautifulSoup(r.text, features="lxml")
    for link in soup.findAll('a'):
        str_link = str(link)
        if "https:" in str_link and \
           "/url?q=" in str_link and \
           "https://www.youtube.com" not in str_link and \
           "https://accounts.google.com" not in str_link:

            url_wo_q = str_link.split("/url?q=")[1]
            clean_url = url_wo_q.split("&amp")[0]
            print(clean_url)

    print('\n\n')

def google_query1(query):

    url = {}
    counter = 0

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

            url[counter] = clean_url
            counter += 1
    return url

def google_query2(query):
    url = {}
    counter = 0

    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    # to search
    for link in search(query, tld="com", num=100, start=0, stop=10, pause=1):
        str_link = str(link)
        if "https://www.youtube.com" not in str_link and \
           "https://accounts.google.com" not in str_link:
            url[counter] = str_link
            counter += 1

    return url



# url = google_query1("dummy python")
url = google_query2("dummy python")


for k, v in url.items():
    print(k, ": ", v)

