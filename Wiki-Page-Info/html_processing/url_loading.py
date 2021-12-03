import urllib
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from collections import Counter
import json
import string


def data_to_json(data_dict: dict):
    with open(
        "Wiki-Page-Info/html_processing/json_loader/Wiki-Page-Info.json", "w"
    ) as json_file:
        json.dump(data_dict, json_file)
    print("JSON File created in ~Wiki-Page-Info/html_processing/json_loader~")


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


def remove_symbols(text: str):
    # iteration through text words
    for char in string.punctuation:
        text = s.replace(char, " ")
    return text


def get_most_frequent_word(text: str):
    most_occur = Counter(text).most_common(1)[0]
    return most_occur[0]


def get_least_frequent_word(text: str):
    least_occur = Counter(text).most_common()[-1]
    return least_occur[0]


def get_longest_word(text: str):
    return max(text, key=len)


def get_shortest_word(text: str):
    return min(text, key=len)


def get_data_from_html(html_text: str):
    data_dict = {
        "Title": "",
        "Most frequent word": "",
        "Least frequent word": "",
        "Longest word": "",
        "Shortest word": "",
        "Images": [],
    }

    title_index = html_text.find("<title>")
    start_index = title_index + len("<title>")
    end_index = html_text.find("</title>")
    title = html_text[start_index:end_index]

    soup = BeautifulSoup(html_text, "html.parser")
    # print(soup.get_text().split())
    text = remove_symbols(soup.get_text().split())

    data_dict["Title"] = title
    data_dict["Most frequent word"] = get_most_frequent_word(text)
    data_dict["Least frequent word"] = get_least_frequent_word(text)
    data_dict["Longest word"] = get_longest_word(text)
    data_dict["Shortest word"] = get_shortest_word(text)

    images = soup.find_all("img")
    images_list = []
    for img in images:
        images_list.append(img["src"])
    data_dict["Images"] = images_list
    # save_images(images)

    data_to_json(data_dict)
    # print(data_dict)


def load(url: str):
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        get_data_from_html(html)
    except urllib.error.URLError as e:
        print(e.reason)
