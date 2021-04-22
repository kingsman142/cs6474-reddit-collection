import os
import pandas as pd

from happytransformer import HappyTextClassification

# load our data
all_reddit_filenames = [os.path.join("reddit-data", reddit_filename) for reddit_filename in os.listdir("reddit-data")] # return all filenames in the reddit-data/ directory and put them in this list as reddit-data/filename

# create an output directory where we store classification results
if not os.path.exists("reddit-predictions"):
    os.makedir("reddit-predictions")

# load the hate speech detection model with 3 classes ("normal", "hate speech", "toxic")
happy_tc = HappyTextClassification("BERT", "Hate-speech-CNERG/bert-base-uncased-hatexplain", 3) # https://github.com/hate-alert/HateXplain

# iterate over all the reddit posts collected for each character
for filename_index, filename in enumerate(all_reddit_filenames):
    print("Working on file {}/{}...".format(filename_index+1, len(all_reddit_filenames)))

    # classify posts for this character
    reddit_data = pd.read_csv(filename)
    predictions_data = {"tweet_id": reddit_data["tweet_id"], "classification": [], "classification_score": []}
    for post_index, post in enumerate(reddit_data["text"]):
        if post_index == 0 or (post_index+1) % 5 == 0:
            print("\tWorking on post {}/{}...".format(post_index+1, len(reddit_data["text"])))

        pred = happy_tc.classify_text(post)
        predictions_data["classification"].append(pred.label) # hate speech, toxic, or normal?
        predictions_data["classification_score"].append(pred.score) # how confident are we? score between 0-1

    # write predictions to a file in reddit-predictions/
    predictions_df = pd.DataFrame(new_data)
    predictions_filename = "{}_pred.csv".format(filename.split("_")[0]) # filename.split("_")[0] extracts the actor/character name from "actorname_posts.csv"
    predictions_df.to_csv(predictions_filename, index=False)
