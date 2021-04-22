import os
import nltk
from time import sleep

import pandas as pd

from utils.calculations import calc_tfidf
from utils.tokenizer import tokenize

class SubredditScraper:
    def __init__(self, reddit_object, name_searched, sub, seeds_set, seeding_iters = 5, search_limit = 100, actor_character_search_limit = 400, mode='w'):
        self.sub = sub # the subreddit we're searching through
        self.mode = mode # search mode (e.g. 'relevant', 'hot', 'new')
        self.seeds_set = seeds_set
        self.seeds_iters = seeding_iters # the number of iterations for seeding
        self.reddit = reddit_object
        self.search_limit = search_limit

        self.name_searched = name_searched # name of actor or character we're searching for
        self.actor_character_search_limit = actor_character_search_limit
        print('SubredditScraper instance created with values: sub = {}, mode = {}'.format(sub, mode))

    def get_posts(self):
        """Get unique posts from a specified subreddit."""
        sub_dict = {
            'tweet_id': [], 'author_id': [], 'date': [], 'text': [], 'name_searched': [],
            'title': [], 'num_comments': [], 'score': [], 'ups': [], 'downs': [], 'subreddit': []}

        # Set csv_loaded to True if csv exists since you can't
        # evaluate the truth value of a DataFrame.
        df, csv_loaded = (pd.read_csv(csv), True) if os.path.isfile(csv) else ('', False)

        print('csv = {}'.format(csv))
        print('csv_loaded = {}'.format(csv_loaded))

        print('Collecting information from r/{}.'.format(self.sub))
        # NOTE: initial_subreddit_posts and subreddit_posts are separated so we can later analyze the quality of posts returned from our initial search vs. later searches.
        #       besides that purpose, if we don't want to analyze their differences later, we can just drop initial_subreddit_posts and store everything in subreddit_posts.
        initial_subreddit_posts = []
        subreddit_posts = []
        analysis_dict = {"subreddit": [], "iteration": [], "keywords": [], "keyword_scores": [], "num_posts": [], "num_deduped_posts": []} # only used for logging purposes so we can analyze them later in the term

        # seeding iterations
        unique_post_ids = set()
        for iter in range(self.seeds_iters):
            print("=== Beginning iteration {}/{} of seeding ===".format(iter+1, self.seeds_iters))
            # (1) find all posts that contain keywords in the seeding list
            posts_across_all_searches = []
            if iter == 0: # in the first iteration, discover posts related to the actor and character's names
                # find posts with actor/character names
                posts_across_all_searches += self.reddit.subreddit(self.sub).search(query = self.actor, limit = self.actor_character_search_limit)
            else:
                for keyword in self.seeds_set:
                    curr_search_posts = self.reddit.subreddit(self.sub).search(query = keyword, limit = self.search_limit)
                    print("curr keyword: {}".format(keyword))
                    posts_across_all_searches += curr_search_posts
            print("Number of posts returned: {}".format(len(posts_across_all_searches)))

            # (2) remove duplicate posts (dedup)
            print("Performing dedup of posts...")
            num_deduped_posts = 0
            for post in posts_across_all_searches:
                if post.id not in unique_post_ids:
                    if iter == 0:
                        # filter some of the posts down so the only ones remaining are the ones with keywords from the initial seeding list
                        for word in nltk.word_tokenize(post.selftext):
                            if word in self.seeds_set and post.id not in unique_post_ids:
                                unique_post_ids.add(post.id)
                                initial_subreddit_posts.append(post)
                    else:
                        unique_post_ids.add(post.id)
                        subreddit_posts.append(post)
                else:
                    num_deduped_posts += 1

            # clean and tokenize post bodies (refer to comment above for variable definitions to see the difference between these two variables)
            print("Cleaning posts...")
            posts_tokens = tokenize(initial_subreddit_posts) if iter == 0 else tokenize(subreddit_posts)
            print("Example list of post tokens: {}".format(posts_tokens[0]))
            print(len(posts_tokens))

            # (3) add all new possible keywords to our new seeding set for next round
            print("Calculating tf-idf scores for tokens...")
            new_keyword_list, new_keyword_scores = calc_tfidf(posts_tokens)

            # log some data that we can analyze later on
            analysis_dict["subreddit"].append(self.sub)
            analysis_dict["iteration"].append(iter)
            analysis_dict["keywords"].append(new_keyword_list)
            analysis_dict["keyword_scores"].append(new_keyword_scores)
            analysis_dict["num_posts"].append(len(unique_post_ids))
            analysis_dict["num_deduped_posts"].append(num_deduped_posts)

            self.seeds_set = new_keyword_list

        # extract info from our final list of posts
        for post in subreddit_posts:
            # Check if post.id is in df and set to True if df is empty.
            # This way new posts are still added to dictionary when df = ''
            unique_id = post.id not in tuple(df.id) if csv_loaded else True

            # Save any unique posts to sub_dict.
            # base data format off of: https://raw.githubusercontent.com/camille2019/cs6474_twitter_data_collection/main/character_tweets.csv
            if unique_id:
                sub_dict['tweet_id'].append(post.id) # actually reddit id but we need to make sure it conforms to the twitter data format above
                sub_dict['author_id'].append(post.author.id)
                sub_dict['date'].append(post.created_utc)
                sub_dict['text'].append(post.selftext)
                sub_dict['name_searched'].append(self.name_searched)
                sub_dict['title'].append(post.title)
                sub_dict['num_comments'].append(post.num_comments)
                sub_dict['score'].append(post.score)
                sub_dict['ups'].append(post.ups)
                sub_dict['downs'].append(post.downs)
                sub_dict['subreddit'].append(self.sub)
            sleep(0.1)

        new_df = pd.DataFrame(sub_dict)
        analytics_df = pd.DataFrame(analysis_dict)

        return new_df, analytics_df
