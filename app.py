from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)


# Default delimiter to delineate primary key fields in string.
key_delimiter = "_"


@app.route('/')
def search():

    return "Hello"
    content = search_content.split(" ")
    length = len(content)

    # Check empty input
    if length == 0:
        return "Beef Kanye VS Drake"
    # Check single words
    if length == 1:
        return "Beef Eminem VS MGK"
    # Check two words
    if length == 2:
        return "Beef 21 Sava"
    # Check three words
