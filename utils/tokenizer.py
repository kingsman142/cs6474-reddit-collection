from praw.models import MoreComments
import nltk

def tokenize(posts):
    tokens = []

    for submission in posts:
        # extract posts' selftext if extant
        if submission.selftext:
            selftext_token = nltk.word_tokenize(submission.selftext)
            tokens.append(selftext_token)

        if submission.comments:
            # retrieve top level comments
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()

            # tokenize top level comments
            for top_level_comment in comments:
                body_token = nltk.word_tokenize(top_level_comment.body)
                tokens.append(body_token)
    
    return tokens
        
