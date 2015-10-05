"""
Bias Reduction:
    - The wikipedia list has 1400 movies rather than 1000 - 200 = 800. I may want to end up
    using that ne instead
Strategy:
1.
"""
import pandas as pd

def load_sequel_titles():
    """

    :return:
    """
    df = pd.read_csv('movies_with_sequels.csv')
    del df['position']

