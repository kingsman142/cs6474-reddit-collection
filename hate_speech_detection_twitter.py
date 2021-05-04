import os
import math
import pandas as pd

from happytransformer import HappyTextClassification

# load our data
twitter_data_filename = "clean_tweets.csv"

# load the hate speech detection model with 3 classes ("normal", "hate speech", "toxic")
happy_tc = HappyTextClassification("BERT", "Hate-speech-CNERG/bert-base-uncased-hatexplain", 3) # https://github.com/hate-alert/HateXplain

# classify tweets
twitter_data = pd.read_csv(twitter_data_filename)
predictions_data = {"tweet_id": twitter_data["tweet_id"], "name_searched": [], "classification": [], "classification_score": []}
for post_index, post in twitter_data.iterrows():
    if post_index == 0 or (post_index+1) % 5 == 0:
        print("\tWorking on post {}/{}...".format(post_index+1, len(twitter_data["text"])))

    post_text = post["text_lower"]
    pred = happy_tc.classify_text(post_text)
    
    predictions_data["name_searched"].append(post["name_searched"])
    predictions_data["classification"].append(pred.label) # hate speech, toxic, or normal?
    predictions_data["classification_score"].append(pred.score) # how confident are we? score between 0-1

# write predictions to a file
predictions_df = pd.DataFrame(predictions_data)
predictions_filename = "clean_tweets_pred.csv"
predictions_df.to_csv(predictions_filename, index=False)
