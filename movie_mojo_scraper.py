import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_movie_list():
    """
    :return: List of all movies on the Beautiful Soup website
    """


def get_movie_data(movie_list):
    """
    Takes a list of movies and returns all pertinant data in the form of a Pandas Dataframe


    :param movie_list: List of movie titles
    :return: Pandas Dataframe of
    """
    cleaned_data = pd.DataFrame()

    for movie in movie_list:
        url = "http://www.boxofficemojo.com/movies/?page=weekly&id=" + movie + ".htm"
        parsed_movie = parse_movie(url)
        cleaned_data = cleaned_data.append(parsed_movie)

    return cleaned_data


def parse_movie(url):
    """
    Given a single url, gives us all the important data from a single list.
    :param url:
    :return: list of important attributes.
    """
    movie_attributes = []
    request = requests.get(url)

    soup = BeautifulSoup(request.text)

    ## find the attributes