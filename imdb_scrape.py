"""
Bias Reduction:
    - The wikipedia list has 1400 movies rather than 1000 - 200 = 800. I may want to end up
    using that ne instead
Process:
    1. Find all of the necessary data for the training model.
    2. Make my predictions for the test models
    3. Go back to scraping all the films
    4. Find the films that have the most related thing

Strategy for scraping data:
    1. Load a list of sequel titles
    2. Construct a list of all the URLs of interest.
"""
import sys
import pandas as pd


def load_sequel_df():
    """

    :return:
    """
    df = pd.read_csv('movies_with_sequels.csv')
    del df['position']
    return df


def get_sequel_urls(df):
    """
    Returns a list of the urls of all the Sequels in the dataset.
    """
    id = list(df.const.values)
    base_url = 'http://www.imdb.com/title/'
    complete_url = [base + end for base, end in zip(id, base_url)]
    assert len(complete_url) > 500

    return complete_url





def main():
    """

    :return:
    """

if __name__ == 'main':
    main()