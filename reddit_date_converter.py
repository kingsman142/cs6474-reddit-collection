import os
import math
import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime

# load our data
all_reddit_filenames = [os.path.join("reddit-data", reddit_filename) for reddit_filename in os.listdir("reddit-data")] # return all filenames in the reddit-data/ directory and put them in this list as reddit-data/filename

earliest_date = float('inf')
latest_date = float('-inf')

for filename_index, filename in enumerate(all_reddit_filenames):
    reddit_data = pd.read_csv(filename)
    name = filename.split("_")[0].replace("\\", "/").split("/")[1].lower().strip()

    earliest_date = min(earliest_date, int(min(reddit_data['date'])))
    latest_date = max(latest_date, int(max(reddit_data['date'])))

print(datetime.fromtimestamp(earliest_date).strftime('%Y-%m-%d %H:%M:%S'))
print(datetime.fromtimestamp(latest_date).strftime('%Y-%m-%d %H:%M:%S'))
