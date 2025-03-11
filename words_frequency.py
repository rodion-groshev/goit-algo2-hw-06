import string
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return None


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def visualize_top_words(values, top_words=None):
    if top_words:
        lst_value = list(values.values())[:top_words]
        lst_keys = list(values.keys())[:top_words]
    else:
        lst_value = list(values.values())
        lst_keys = list(values.keys())

    plt.barh(
        lst_keys,
        lst_value,
    )
    plt.show()


def map_reduce(text, search_words=None):
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word in search_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(sorted(reduced_values, key=lambda x: x[1], reverse=True))


if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        result = map_reduce(text)
        visualize_top_words(result, 20)

        print("The result of the word count:", result)
    else:
        print("Error: Unable to receive input text.")
