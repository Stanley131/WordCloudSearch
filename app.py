from flask import Flask
from aeneid.dbservices import dataservice as ds
from flask import Flask
from flask import request
import os
import json
import copy
from aeneid.utils import utils as utils
import re
from aeneid.utils import webutils as wu
from aeneid.dbservices.DataExceptions import DataException
from flask import Response
from urllib.parse import urlencode

# Default delimiter to delineate primary key fields in string.
key_delimiter = "_"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search(search_content):
    content = search_content.split(" ")
    length = len(content)

    # Check empty input
    if length == 0:
        return
    # Check single words
    if length == 1:

    # Check two words
    if length == 2:

    # Check three words
