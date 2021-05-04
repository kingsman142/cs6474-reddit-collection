import os
import math
import pandas as pd

import matplotlib.pyplot as plt

# load our data
all_reddit_filenames = [os.path.join("reddit-predictions", reddit_filename) for reddit_filename in os.listdir("reddit-predictions")] # return all filenames in the reddit-data/ directory and put them in this list as reddit-data/filename

black_white_characters = pd.read_csv("black_white_characters.csv")
black_chars = list(black_white_characters["black"])
white_chars = list(black_white_characters["white"])

num_black_offensive_tweets = 0
num_white_offensive_tweets = 0
num_black_hatespeech_tweets = 0
num_white_hatespeech_tweets = 0
num_black_tweets = 0
num_white_tweets = 0

most_hated_names = {}
most_hated_black_names = {}
most_hated_white_names = {}

for filename_index, filename in enumerate(all_reddit_filenames):
    reddit_data = pd.read_csv(filename)
    name = filename.split("_")[0].replace("\\", "/").split("/")[1].lower().strip()

    # simple analysis
    num_offensive_tweets = len(reddit_data[reddit_data["classification"] == "offensive"])
    num_hatespeech_tweets = len(reddit_data[reddit_data["classification"] == "hate speech"])
    print("{} : {} ({}%) offensive, {} ({}%) hate speech".format(name, num_offensive_tweets, round(num_offensive_tweets / len(reddit_data) * 100, 5), num_hatespeech_tweets, round(num_hatespeech_tweets / len(reddit_data) * 100, 5)))
    most_hated_names[name] = round((num_offensive_tweets + num_hatespeech_tweets) / len(reddit_data), 4)

    # complex analysis
    if name in black_chars:
        most_hated_black_names[name] = round((num_offensive_tweets + num_hatespeech_tweets) / len(reddit_data), 4)

        num_black_offensive_tweets += num_offensive_tweets
        num_black_hatespeech_tweets += num_hatespeech_tweets
        num_black_tweets += len(reddit_data)
    elif name in white_chars:
        most_hated_white_names[name] = round((num_offensive_tweets + num_hatespeech_tweets) / len(reddit_data), 4)

        num_white_offensive_tweets += num_offensive_tweets
        num_white_hatespeech_tweets += num_hatespeech_tweets
        num_white_tweets += len(reddit_data)
    else:
        print("Name not found: {}".format(name))

print("\nmost hated characters\n=====")
for name, percent in sorted(most_hated_names.items(), key = lambda x : x[1], reverse = True)[:10]:
    print("{} ({}%)".format(name, round(percent * 100, 2)))
print("\nmost hated black characters\n=====")
for name, percent in sorted(most_hated_black_names.items(), key = lambda x : x[1], reverse = True)[:10]:
    print("{} ({}%)".format(name, round(percent * 100, 2)))
print("\nmost white hated characters\n=====")
for name, percent in sorted(most_hated_white_names.items(), key = lambda x : x[1], reverse = True)[:10]:
    print("{} ({}%)".format(name, round(percent * 100, 2)))

print("\n# offensive reddit posts: {}".format(num_black_offensive_tweets + num_white_offensive_tweets))
print("# hate speech reddit posts: {}".format(num_black_hatespeech_tweets + num_white_hatespeech_tweets))

print("\nP(offensive | black) = {}".format(round(num_black_offensive_tweets / num_black_tweets, 8)))
print("P(hate speech | black) = {}".format(round(num_black_hatespeech_tweets / num_black_tweets, 8)))
print("P(offensive | white) = {}".format(round(num_white_offensive_tweets / num_white_tweets, 8)))
print("P(hate speech | white) = {}".format(round(num_white_hatespeech_tweets / num_white_tweets, 8)))

p_black_offensive = round(num_black_offensive_tweets / (num_black_offensive_tweets + num_white_offensive_tweets), 8)
p_black_hatespeech = round(num_black_hatespeech_tweets / (num_black_hatespeech_tweets + num_white_hatespeech_tweets), 8)
p_white_offensive = round(num_white_offensive_tweets / (num_black_offensive_tweets + num_white_offensive_tweets), 8)
p_white_hatespeech = round(num_white_hatespeech_tweets / (num_black_hatespeech_tweets + num_white_hatespeech_tweets), 8)

print("\nP(black | offensive) = {}".format(p_black_offensive))
print("P(black | hate speech) = {}".format(p_black_hatespeech))
print("P(white | offensive) = {}".format(p_white_offensive))
print("P(white | hate speech) = {}".format(p_white_hatespeech))

# make some graphs
labels = ["Black", "White"]
offensive_sizes = [p_black_offensive * 100, p_white_offensive * 100]
hatespeech_sizes = [p_black_offensive * 100, p_white_offensive * 100]
plt.pie(x = offensive_sizes, labels = labels, autopct=lambda p : '{:.2f}%'.format(p))
plt.title("% of Offensive Reddit Posts Targeting Each Race")
plt.axis("auto")
plt.figure()
plt.pie(x = hatespeech_sizes, labels = labels, autopct=lambda p : '{:.2f}%'.format(p))
plt.title("% of Hate Speech Reddit Posts Targeting Each Race")
plt.axis("auto")
plt.show()
