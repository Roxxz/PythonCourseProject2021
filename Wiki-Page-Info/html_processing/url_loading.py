import urllib
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from collections import Counter
import json


def data_to_json(data_dict: dict):
    with open(
        "Wiki-Page-Info/html_processing/json_loader/Wiki-Page-Info.json", "w"
    ) as json_file:
        json.dump(data_dict, json_file)


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


def get_most_frequent_word(html_text: str):
    # split() returns list of all the words in the string
    split_it = html_text.split()

    # Pass the split_it list to instance of Counter class.
    counter = Counter(split_it)

    # most_common() produces k frequently encountered
    # input values and their respective counts.
    most_occur = counter.most_common(1)

    return most_occur[0][0]


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

    data_dict["Title"] = title
    # print(title)

    soup = BeautifulSoup(html_text, "html.parser")
    # print(soup.get_text())

    data_dict["Most_frequent_word"] = get_most_frequent_word(soup.get_text())

    images = soup.find_all("img")
    images_list = []
    for img in images:
        images_list.append(img["src"])
    data_dict["Images"] = images_list
    # save_images(images)

    # print(data_dict)
    data_to_json(data_dict)


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
