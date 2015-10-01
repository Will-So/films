"""
Strategy

1. Get a list of the movie names
    - Figure out how to navigate through all of the different letters
        Implemented through iterate_letters
    - Figure out how to navigate through all of the sub-directories for the letter
    if they exist
    - Scrape all of the ids for the movies
2. Parse all of the relevant movie information
    - Retrieve the soup object for each entry
    - Put all of the relevant entries into a list
    - Return each list as a single row of a Pandas df
"""


import requests
import pandas as pd
from bs4 import BeautifulSoup
import string


def get_movie_id_list():
    """
    :return: List of all movie ids on the Beautiful Soup website
    """

    letter_urls = iterate_letters()
    category_urls = iterate_letter_category(letter_urls)
    movie_ids = []
    for url in category_urls:
        pass
        # Adds the movie ids to all the lists in the thing

    return movie_ids


def iterate_letters():
    """

    :param letter:
    :return: List of the URLs for each letter
    """

    letter_urls = ['http://www.boxofficemojo.com/movies/alphabetical.htm?letter=' + i for
                   i in string.ascii_lowercase]

    letter_urls.append('http://www.boxofficemojo.com/movies/alphabetical.htm?letter=NUM')

    assert len(letter_urls) == 27

    return letter_urls


def iterate_letter_category(letter_urls):
    """

    :param letter:
    :return: List of the URL of letter categories
    """
    letter_category_urls = []
    for url in letter_urls:
        letter_category_urls.append(url) # The first item is selected automatically
        text = requests.get(url).text
        soup = BeautifulSoup(text)





    return letter_category_urls



def parse_movies(movie_list):
    """
    Takes a list of movies and returns all pertinant data in the form of a Pandas Dataframe


    :param movie_list: List of movie titles
    :return: Pandas Dataframe of
    """
    cleaned_data = pd.DataFrame()

    for movie in movie_list:
        url = "http://www.boxofficemojo.com/movies/?page=weekly&id=" + movie + ".htm"

        request = requests.get(url)
        soup = BeautifulSoup(request.text)
        cleaned_data.append(retrieve_attributes(soup))

    return cleaned_data


def retrieve_attributes(soup):
    """
    Helper function for `parse_movies`. Retrieves individual points of data for each movie
    :param soup:
    :return: list of important attributes.
    """
    movie_attributes = []


    return movie_attributes


    ## find the attributes


def main():
    movie_list = get_movie_id_list()
    movie_data = parse_movies(movie_list)
    movie_data.to_csv('/Data/films/mojo.csv')