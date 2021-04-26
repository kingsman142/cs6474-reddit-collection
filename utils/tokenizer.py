from praw.models import MoreComments
import nltk

nltk.download('words')

def tokenize(posts):
    tokens = []
    english_vocab = set(word.lower() for word in nltk.corpus.words.words())
    for letter in "abcdefghijklmnopqrstuvwxyz":
        english_vocab.remove(letter)

    for index, submission in enumerate(posts):
        if index == 0 or (index+1) % 10 == 0:
            print("\tcleaned post {}/{}".format(index+1, len(posts)))
        # extract posts' selftext if extant
        if submission.selftext:
            selftext_token = [token.lower() for token in nltk.word_tokenize(submission.selftext) if token in english_vocab]
            tokens.append(selftext_token)

        if submission.comments:
            # retrieve top level comments
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()
            top_n_comments = min(len(comments), 2)

            # tokenize top level comments
            for top_level_comment in comments[:top_n_comments]:
                body_token = nltk.word_tokenize(top_level_comment.body)
                body_token = [token.lower() for token in body_token if token in english_vocab]
                tokens.append(body_token)

    return tokens
