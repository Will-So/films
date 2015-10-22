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


Notes
~~~~~

"""


import requests
import pandas as pd
from bs4 import BeautifulSoup
import string
import pickle
from html.parser import HTMLParseError
import warnings
from urllib.error import HTTPError
import time

PICKLE_MOVIE_URLS = True
PICKLE_ARRAYS = True
TABLE_XPATH =  ('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]'
                '/table/tbody/tr/td/center/table/tbody')


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


    :param movie_list: List of movie titles
    :return: A list of Numpy arrays with all relevant stats and name

    Example
    ---

    """
    # all_dfs is a list of dataframes of len `movie_list`.

    all_dfs = []
    failed_urls = []
    names = []
    count = 0
    for url in movie_list:
        try:
            df = pd.read_html(url)[5] # The 5th table on BJ is of interest
            all_dfs.append(df)
            names.append(re.search('(\w+?).htm', url).group(1))
            count += 1
            if count % 5 == 0:
                time.sleep(0.5)
                print("Finished {} frames. {} Failed".format(count, len(failed_urls)))
        except (UnicodeEncodeError, HTMLParseError, HTTPError) as err:
            failed_urls.append((url, err))
            continue

    if len(failed_urls) > 250:
        warnings.warn("{} URLs failed to Parse.".format(len(failed_urls)))

    if PICKLE_ARRAYS:
        with open('arrays.pkl', 'wb') as picklefile:
            pickle.dump(arrays, picklefile)

    arrays = [np.append(name, df) for name, df in zip(names, all_dfs)]
    return arrays


def generate_df(movie_dfs):
    """
    Takes list of dataframes generated from `parse_movies` and returns a clean
    dataframe from everything

    :param movie_dfs:
    :return: list of important attributes.
    """
    columns = ['name', 'gross', 'genres', 'mpaa', 'runtime', 'pg', 'distributor', 'release_date']


    cleaned_df = pd.DataFrame(arrays)
    cleaned_df = cleaned_df.drop([2], axis=1) # Extraneous Column

    cleaned_df.columns = columns


    return cleaned_df


    ## find the attributes


def main():
    movie_list = get_movie_urls()
    if PICKLE_MOVIE_URLS:
        pickle.dump(movie_list, 'movie_list.pkl')
    movie_data = parse_movies(movie_list)
    df = generate_df(movie_data)
    df.to_csv('/Data/films/mojo.csv')