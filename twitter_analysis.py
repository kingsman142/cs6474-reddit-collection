import os
import math
import pandas as pd

# load our data
twitter_data_filename = "clean_tweets_pred.csv"
twitter_data = pd.read_csv(twitter_data_filename)

black_white_characters = pd.read_csv("black_white_characters.csv")
black_chars = list(black_white_characters["black"])
white_chars = list(black_white_characters["white"])

# simple analysis (can use simple dataframe features)
num_offensive_tweets = len(twitter_data[twitter_data["classification"] == "offensive"])
num_hatespeech_tweets = len(twitter_data[twitter_data["classification"] == "hate speech"])
print("# offensive tweets: {} ({}%)".format(num_offensive_tweets, round(num_offensive_tweets / len(twitter_data) * 100, 5)))
print("# hate speech tweets: {} ({}%)".format(num_hatespeech_tweets, round(num_hatespeech_tweets / len(twitter_data) * 100, 5)))

# complex analysis (have to iterate over all rows)
num_black_offensive_tweets = 0
num_white_offensive_tweets = 0
num_black_hatespeech_tweets = 0
num_white_hatespeech_tweets = 0
num_black_tweets = 0
num_white_tweets = 0
for post_index, post in twitter_data.iterrows():
    prediction = post["classification"]
    name = post["name_searched"].lower().strip()
    if name in black_chars:
        num_black_offensive_tweets += 1 if prediction == "offensive" else 0
        num_black_hatespeech_tweets += 1 if prediction == "hate speech" else 0
        num_black_tweets += 1
    elif name in white_chars:
        num_white_offensive_tweets += 1 if prediction == "offensive" else 0
        num_white_hatespeech_tweets += 1 if prediction == "hate speech" else 0
        num_white_tweets += 1
    else:
        print("Name not found: {}".format(name))

print("\nP(offensive | black) = {}".format(round(num_black_offensive_tweets / num_black_tweets, 8)))
print("P(hate speech | black) = {}".format(round(num_black_hatespeech_tweets / num_black_tweets, 8)))
print("P(offensive | white) = {}".format(round(num_white_offensive_tweets / num_white_tweets, 8)))
print("P(hate speech | white) = {}".format(round(num_white_hatespeech_tweets / num_white_tweets, 8)))

print("\nP(black | offensive) = {}".format(round(num_black_offensive_tweets / (num_black_offensive_tweets + num_white_offensive_tweets), 8)))
print("P(black | hate speech) = {}".format(round(num_black_hatespeech_tweets / (num_black_hatespeech_tweets + num_white_hatespeech_tweets), 8)))
print("P(white | offensive) = {}".format(round(num_white_offensive_tweets / (num_black_offensive_tweets + num_white_offensive_tweets), 8)))
print("P(white | hate speech) = {}".format(round(num_white_hatespeech_tweets / (num_black_hatespeech_tweets + num_white_hatespeech_tweets), 8)))
