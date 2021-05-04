import os
import math
import pandas as pd

from collections import Counter

# load our data
all_reddit_filenames = [os.path.join("reddit-analytics", reddit_filename) for reddit_filename in os.listdir("reddit-analytics")] # return all filenames in the reddit-data/ directory and put them in this list as reddit-data/filename

black_white_characters = pd.read_csv("black_white_characters.csv")
black_chars = list(black_white_characters["black"])
white_chars = list(black_white_characters["white"])

white_keyword_counter = Counter()
black_keyword_counter = Counter()

avg_num_black_posts_per_iteration = 0
black_seeding_iterations = 0
avg_num_white_posts_per_iteration = 0
white_seeding_iterations = 0
avg_num_deduped_posts_per_iteration = 0

for filename_index, filename in enumerate(all_reddit_filenames):
    reddit_data = pd.read_csv(filename)
    name = filename.split("_")[0].replace("\\", "/").split("/")[1].lower().strip()

    for index, row in reddit_data.iterrows():
        keywords = row["keywords"].replace(")", "").replace("(", "").replace("'", "").replace(" ", "").split(",")
        if len(keywords) == 1: # this means keywords = ['[]'] instead of ['describe', 'knot', 'appear', 'menu', 'ride', 'city', 'cartoon', 'joint', 'masterpiece', 'thus'] because of no posts returned in that iteration
            continue

        if name in black_chars:
            black_keyword_counter.update(keywords)
            avg_num_black_posts_per_iteration += row["num_posts"]
            black_seeding_iterations += 1
        elif name in white_chars:
            white_keyword_counter.update(keywords)
            avg_num_white_posts_per_iteration += row["num_posts"]
            white_seeding_iterations += 1
        else:
            print("Name not found: {}".format(name))

        avg_num_deduped_posts_per_iteration += row["num_deduped_posts"]

avg_num_deduped_posts_per_iteration /= (black_seeding_iterations + white_seeding_iterations)
avg_num_posts_per_iteration = (avg_num_black_posts_per_iteration + avg_num_white_posts_per_iteration) / (black_seeding_iterations + white_seeding_iterations)

print("Avg # of posts per iteration: {}".format(avg_num_posts_per_iteration))
print("Avg # of deduped posts per iteration: {} ({}%)".format(avg_num_deduped_posts_per_iteration, round(avg_num_deduped_posts_per_iteration / avg_num_posts_per_iteration * 100, 2)))

avg_num_black_posts_per_iteration /= black_seeding_iterations
avg_num_white_posts_per_iteration /= white_seeding_iterations

print("Avg # of black posts per iteration: {}".format(avg_num_black_posts_per_iteration))
print("Avg # of white posts per iteration: {}".format(avg_num_white_posts_per_iteration))

print("\nMost common black keywords: {}".format(black_keyword_counter.most_common(10)))
print("Most common white keywords: {}".format(white_keyword_counter.most_common(10)))
