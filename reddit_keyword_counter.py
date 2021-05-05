import os
import math
import pandas as pd

import matplotlib.pyplot as plt

from collections import Counter

# load our data
all_reddit_filenames = [os.path.join("reddit-data", reddit_filename) for reddit_filename in os.listdir("reddit-data")] # return all filenames in the reddit-data/ directory and put them in this list as reddit-data/filename
seeds_set = ['racebend', 'black', 'white', 'color', 'divers', 'politic', 'rac', 'annoy', 'remove', 'hate', 'never', 'not', 'dislike', 'disturb', 'threat', 'scrutiniz', 'humiliat', 'angry', 'rage', 'pander', 'nostalg',
             'scare', 'trauma', 'ignor', 'monkey', 'gorilla', 'persecut', 'discriminat', 'prejudice', 'obscen', 'unwelcome', 'no', 'hassle', 'torment', 'irritat', 'aggravat', 'victim', 'aggress', 'crime', 'troll', 'dominat']

black_white_characters = pd.read_csv("black_white_characters.csv")
black_chars = list(black_white_characters["black"])
white_chars = list(black_white_characters["white"])

black_seeds_counter = Counter()
white_seeds_counter = Counter()
for filename_index, filename in enumerate(all_reddit_filenames):
    reddit_data = pd.read_csv(filename)
    name = filename.split("_")[0].replace("\\", "/").split("/")[1].lower().strip()

    for index, post in reddit_data.iterrows():
        post_text = post["text"] if type(post["text"]) is not float else post["title"]
        for seed in seeds_set:
            if seed in post_text:
                if name in black_chars:
                    black_seeds_counter[seed] += 1
                elif name in white_chars:
                    white_seeds_counter[seed] += 1

# make some graphs
most_common_black_keywords = black_seeds_counter.most_common(10)
black_keyword_names = [x[0] for x in most_common_black_keywords]
black_keyword_counts = [x[1] for x in most_common_black_keywords]
most_common_white_keywords = white_seeds_counter.most_common(10)
white_keyword_names = [x[0] for x in most_common_white_keywords]
white_keyword_counts = [x[1] for x in most_common_white_keywords]
plt.bar(x = black_keyword_names, height = black_keyword_counts)
plt.title("Keyword Counts Across Black Reddit Posts")
plt.axis("auto")
plt.figure()
plt.bar(x = white_keyword_names, height = white_keyword_counts)
plt.title("Keyword Counts Across White Reddit Posts")
plt.axis("auto")
plt.show()
