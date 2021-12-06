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
        finally:
            continue


def remove_symbols(text: list):
    symbols = [
        "`",
        ".",
        "~",
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "_",
        "+",
        "-",
        "=",
        "[",
        "]",
        "{",
        "}",
        "|",
        ";",
        "'",
        ":",
        "/",
        "<",
        ">",
        "?",
        ",",
    ]
    for symbol in symbols:
        while symbol in text:
            text.remove(symbol)
    return text


def format_text(text: list, option: bool = 0):
    if option:
        prepositions = [
            "with",
            "at",
            "by",
            "to",
            "in",
            "for",
            "from",
            "of",
            "on",
            "at",
            "but",
            "by",
            "this",
            "that",
            "the",
            "and",
            "a",
            "an",
            "With",
            "At",
            "By",
            "To",
            "In",
            "For",
            "From",
            "Of",
            "On",
            "At",
            "But",
            "By",
            "This",
            "That",
            "The",
            "And",
            "A",
            "An",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0",
        ]
        for preposition in prepositions:
            while preposition in text:
                text.remove(preposition)
        return text
    else:
        return text


def get_most_frequent_word(text: list):
    most_occur = Counter(text).most_common(1)[0]
    return most_occur


def get_least_frequent_word(text: list):
    least_occur = Counter(text).most_common()[-1]
    return least_occur


def get_longest_word(text: list):
    word = max(text, key=len)
    while not word.isalpha():
        text.remove(word)
        word = max(text, key=len)
    return word


def get_shortest_word(text: list):
    word = min(text, key=len)
    while len(word) < 4:
        text.remove(word)
        word = min(text, key=len)
    return word


def process_data(html_text: str):
    data_dict = {
        "Title": "",
        "Most frequent word": "",
        "MFW No. of Appearances": "",
        "Least frequent word": "",
        "LFW No. of Appearances": "",
        "Longest word": "",
        "Shortest word": "",
        "Images": [],
    }

    soup = BeautifulSoup(html_text, "html.parser")

    text = remove_symbols(
        soup.find("div", attrs={"class": "mw-parser-output"}).get_text().split()
    )

    option = input(
        "Choose text format option: \n 0: simple format; \n 1: without prepositions and numbers; \n"
    )
    text = format_text(text, option)

    title = soup.title.text
    data_dict["Title"] = title
    (word, no) = get_most_frequent_word(text)
    data_dict["Most frequent word"] = word
    data_dict["MFW No. of Appearances"] = no
    (word, no) = get_least_frequent_word(text)
    data_dict["Least frequent word"] = word
    data_dict["LFW No. of Appearances"] = no
    data_dict["Longest word"] = get_longest_word(text)
    data_dict["Shortest word"] = get_shortest_word(text)

    images = soup.find_all("img")
    images_list = []
    for img in images:
        images_list.append(img["src"])
    data_dict["Images"] = images_list
    save_images(images)

    option = input(
        "Choose method of visualising data: \n 0: Only JSON; \n 1: Terminal and JSON; \n"
    )
    if option == "1":
        print(json.dumps(data_dict, indent=4), "\n")
    data_to_json(data_dict)


def load(url: str):
    try:
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        process_data(html)
    except urllib.error.URLError as e:
        print(e.reason)
