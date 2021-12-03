import urllib
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import json


def data_to_json(data_dict: dict):
    # with open('person.txt', 'w') as json_file:
    #     json.dump(personDict, json_file)
    pass


def save_images(images):
    for i in range(len(images)):
        try:
            urlretrieve(
                "https:" + images[i]["src"],
                "Wiki-Page-Info/html_processing/retrieved_images/retrieved_img_"
                + str(i)
                + ".jpg",
            )
        except FileNotFoundError as err:
            print(err)  # something wrong with local path
        except HTTPError as err:
            print(err)  # something wrong with url


def get_data_from_html(html_text: str):
    data_dict = {
        "Title": "",
        "Most_frequent_word": "",
        "Images": [],
    }

    title_index = html_text.find("<title>")
    start_index = title_index + len("<title>")
    end_index = html_text.find("</title>")
    title = html_text[start_index:end_index]
    # print(title)

    soup = BeautifulSoup(html_text, "html.parser")
    # print(soup.get_text())

    images = soup.find_all("img")
    save_images(images)


def load():
    try:
        url = "https://ro.wikipedia.org/wiki/Regnul_Fungi"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        # print(html)
        get_data_from_html(html)
    except urllib.error.URLError as e:
        print(e.reason)
