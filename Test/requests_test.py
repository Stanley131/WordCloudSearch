import requests
from bs4 import BeautifulSoup, SoupStrainer
from googlesearch import search
import re
from nltk.corpus import stopwords
import operator
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import random
from datetime import datetime


# image size 1920 x 1080\
# Default delimiter to delineate primary key fields in string.
key_delimiter = "_"
temp_images_path = "../static/temp_images/"
URL = "http://www.google.com"
URL_GIT= 'https://github.com'
stop_words = set(stopwords.words('english'))
pronouns = ['I', 'ME', 'HIS', 'HE', 'HIM', 'HER', 'SHE', 'YOU', 'IT', 'THEY', 'THEM']
other = ['', ' ', '"', '\r', '\r\n', '(', ')']



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

def clean_text(url):

    pages = []
    for query in url:
        # Search on google
        res = requests.get(url=query, params=None)

        # extract all the URL we fin
        soup = BeautifulSoup(res.text, features="lxml")

        one_page_text = ""

        for node in soup.findAll('p'):
            one_page_text += ' '.join(node.findAll(text=True))
            # print(one_page_text)

        pages.append(one_page_text)

    return pages

def parse_text(page_text):

    page_words = []
    for page in page_text:
        raw_words = re.split(r"\s|,|\.|:|\'|\"", page)
        words = [w.capitalize() for w in raw_words if w not in stop_words and
                 w not in other and w not in pronouns]
        page_words.append(words)

    return page_words

def count_words(clean_text):
    word_count= {}

    for page in clean_text:
        for word in page:
            if word in word_count.keys():
                word_count[word] += 1
            else:
                word_count[word] = 1
    sorted_word = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
    word_dic = dict(sorted_word)

    # print(word_dic)
    return word_dic

def back_to_text(word_count):
    text= ""
    unique_words = ""
    counter = 0
    for k, v in word_count.items():
        for i in range(v):
            text += k
            text += " "
        counter += 1
        unique_words += k
        unique_words += " "
        if counter == 110:
            break

    return (text, unique_words)

def transform_format(val):
    if val == 0:
        return 255
    else:
        return val

def create_mask(image):

    mask = np.array(Image.open(image))
    # print(mask.shape)

    # transformed_mask = np.ndarray((mask.shape[0], mask.shape[1]), np.int32)

    # for i in range(len(mask)):
    # transformed_mask[i] = list(map(transform_format, mask[i]))

    # print(transformed_mask)
    return mask

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    d1 = random.randint(0, 360)
    d2 = random.randint(0, 100)
    d3 = random.randint(0, 100)
    return "hsl(" + str(d1) + "," + str(d2) + "% ," + str(d3) + "%)"

def get_google_text(search_content):

    url = google_query1(search_content)

    page_text = clean_text(url)

    cleanText = parse_text(page_text)

    word_count = count_words(cleanText)

    text, unique_words = back_to_text(word_count)

    return (text, unique_words)

def get_image_name(seach_content):

    image_name = seach_content.replace(" ", key_delimiter)
    now = datetime.now()
    time = now.strftime("_%m_%d_%Y_%H_%M_%S")

    return image_name + time + ".jpg"

def create_word_cloud(text,  image_name, mask_image=None):

    transformed_mask = create_mask("luffy2.jpg")


    wordcloud = WordCloud(background_color="white", collocations=False, max_words=1000,
                      mask=transformed_mask, contour_width=3, color_func=color_func,
                      width=1920, height=1080, contour_color='black').generate(text)

    saved_image = temp_images_path + image_name
    wordcloud.to_file(saved_image)

search_text = "Game of Thrones"

text, unique_words = get_google_text(search_text)

image_name = get_image_name(search_text)

create_word_cloud(text, image_name, mask_image=None)

print(unique_words)