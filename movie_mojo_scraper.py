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
import pickle

pickle_everything = True


def get_movie_urls():
    """
    Collects the URL of every movie listed on box office mojo

    :return: List of all movie ids on the Beautiful Soup website
    """

    letter_urls = iterate_letters()
    category_urls = iterate_letter_category(letter_urls)
    movie_urls = []
    for url in category_urls:
        text = requests.get(url).text
        soup = BeautifulSoup(text)
        soup = soup.find_all('table')[3]

        for link in soup.find_all('a'):
            if 'schedule' in link.attrs['href']:
                continue # Removes the date hrefs

            movie_urls.append('http://www.boxofficemojo.com' + link.get('href'))
        print("Finished the following Category ", url)


    return movie_urls


def iterate_letters():
    """
    Helper function for get_movie_urls. Returns the url for each letter.

    :param letter:
    :return: List of the URLs for each letter

    Examples
    ---
    >>> iterate_letters()[:2]
     ['http://www.boxofficemojo.com/movies/alphabetical.htm?letter=a',
        'http://www.boxofficemojo.com/movies/alphabetical.htm?letter=b']
    """

    letter_urls = ['http://www.boxofficemojo.com/movies/alphabetical.htm?letter=' + i for
                   i in string.ascii_lowercase]

    letter_urls.append('http://www.boxofficemojo.com/movies/alphabetical.htm?letter=NUM')

    assert len(letter_urls) == 27

    return letter_urls


def iterate_letter_category(letter_urls):
    """
    Helper function for  get_movie_urls. Returns a list of all the letter category URLs.

    :param letter:
    :return: List of the URL of letter categories

    Examples
    ---
    >>> iterate_letter_category(iterate_letters())[:4]
    ['http://www.boxofficemojo.com/movies/alphabetical.htm?letter=a',
    'http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&page=2&p=.htm',
    'http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&page=3&p=.htm',
    'http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&page=4&p=.htm']

    """
    letter_category_urls = []
    for url in letter_urls:
        letter_category_urls.append(url) # The first item is selected automatically
        text = requests.get(url).text
        soup = BeautifulSoup(text)
        soup = soup.find("div", class_="alpha-nav-holder")
        for link in soup.find_all('a'):
            letter_category_urls.append('http://www.boxofficemojo.com' + link.get('href'))

    return letter_category_urls


def parse_movies(movie_list):
    """
    Takes a list of movies and returns all pertinant data in the form of a Pandas Dataframe

    Extracts the following Data:
    1. Domestic Total Gross
    2. Genres
    3. MPAA ratings
    4. Runtime
    5. Production Budget
    6. Distributor
    7. Release Date
    8. Actors


    :param movie_list: List of movie titles
    :return: Pandas Dataframe of
    """
    cleaned_data = pd.DataFrame()

    for url in movie_list:
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
    movie_list = get_movie_urls()
    if pickle_everything:
        pickle.dump(movie_list, 'movie_list.pkl')
    movie_data = parse_movies(movie_list)
    movie_data.to_csv('/Data/films/mojo.csv')