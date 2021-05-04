import os
import math
import pandas as pd

from happytransformer import HappyTextClassification

# load our data
all_reddit_filenames = [os.path.join("reddit-data", reddit_filename) for reddit_filename in os.listdir("reddit-data")] # return all filenames in the reddit-data/ directory and put them in this list as reddit-data/filename

# create an output directory where we store classification results
if not os.path.exists("reddit-predictions"):
    os.mkdir("reddit-predictions")

# load the hate speech detection model with 3 classes ("normal", "hate speech", "toxic")
happy_tc = HappyTextClassification("BERT", "Hate-speech-CNERG/bert-base-uncased-hatexplain", 3) # https://github.com/hate-alert/HateXplain

# iterate over all the reddit posts collected for each character
for filename_index, filename in enumerate(all_reddit_filenames):
    print("Working on file {}/{} ({})...".format(filename_index+1, len(all_reddit_filenames), filename))

    # classify posts for this character
    reddit_data = pd.read_csv(filename)
    predictions_data = {"tweet_id": reddit_data["tweet_id"], "classification": [], "classification_score": []}
    for post_index, post in reddit_data.iterrows():
        if post_index == 0 or (post_index+1) % 5 == 0:
            print("\tWorking on post {}/{}...".format(post_index+1, len(reddit_data["text"])))

        post_text = post["text"] if type(post["text"]) is not float else post["title"]
        post_length = len(post_text)
        pred = None
        while True:
            try:
                pred = happy_tc.classify_text(post_text[:post_length])
                break
            except RuntimeError: # will get this exception if the post is more than 500 tokens and can't be fed into the model
                print("\t\tString too long; shortening from {} to {} characters".format(post_length, int(post_length/2)))
                post_length = post_length - 300
        predictions_data["classification"].append(pred.label) # hate speech, toxic, or normal?
        predictions_data["classification_score"].append(pred.score) # how confident are we? score between 0-1

    # write predictions to a file in reddit-predictions/
    predictions_df = pd.DataFrame(predictions_data)
    predictions_filename = "{}_pred.csv".format(filename.split("_")[0].replace("\\", "/").split("/")[1]) # filename.split("_")[0].replace("\\", "/").split("/")[1] extracts the actor/character name from "reddit-data\actorname_posts.csv"
    predictions_df.to_csv(os.path.join("reddit-predictions", predictions_filename), index=False)
