import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

import constants

def calc_tfidf(posts_tokens):
    # construct the list of unique tokens (i.e. vocabulary)
    vocabulary = set()
    for post_tokens in posts_tokens:
        unique_tokens = set(post_tokens)
        vocabulary.intersection(unique_tokens) # create a superset of the tokens across the posts
    vocabulary = list(vocabulary) # must convert from a set to list for the CountVectorizer below

    # join all the tokens in a post and separate by whitespace (required for the fit function below)
    posts_content = [" ".join(post_tokens) for post_tokens in posts_tokens]

    # compute tfidf scores across the posts' words
    pipe = Pipeline([('count', CountVectorizer(vocabulary = vocabulary)), ('tfidf', TfidfTransformer())]).fit(posts_content)

    # sort vocab and tfidf scores together (sort in descending order of tfidf score)
    vocab_words, vocab_tfidf = zip(*sorted(zip(vocabulary, pipe['tfidf'].idf_), key=itemgetter(1), reverse = True))[:constants.TOP_N_KEYWORDS]
    
    return vocab_words, vocab_tfidf
