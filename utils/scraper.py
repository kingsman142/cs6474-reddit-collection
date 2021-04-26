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

        print('Collecting information from r/{}'.format(self.sub))
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
                posts_across_all_searches += self.reddit.subreddit(self.sub).search(query = self.name_searched, limit = self.actor_character_search_limit)
            else:
                for keyword in self.seeds_set:
                    curr_search_posts = self.reddit.subreddit(self.sub).search(query = keyword, limit = self.search_limit)
                    #print("curr keyword: {}".format(keyword)) TODO: remove
                    posts_across_all_searches += curr_search_posts
            print("Number of posts returned: {}".format(len(posts_across_all_searches)))

            # (2) remove duplicate posts (dedup)
            print("Performing dedup of posts...")
            num_deduped_posts = 0
            posts_across_all_searches_deduped = []
            for post in posts_across_all_searches[:100]:
                if post.id not in unique_post_ids:
                    if iter == 0:
                        # filter some of the posts down so the only ones remaining are the ones with keywords from the initial seeding list
                        for word in nltk.word_tokenize(post.selftext):
                            if word in self.seeds_set and post.id not in unique_post_ids:
                                unique_post_ids.add(post.id)
                                initial_subreddit_posts.append(post)
                    else:
                        unique_post_ids.add(post.id)
                        posts_across_all_searches_deduped.append(post)
                else:
                    num_deduped_posts += 1
            #print("len of posts_across_all_searches_deduped: {}".format(len(posts_across_all_searches_deduped)))
            subreddit_posts += initial_subreddit_posts if iter == 0 else posts_across_all_searches_deduped

            # clean and tokenize post bodies (refer to comment above for variable definitions to see the difference between these two variables)
            print("Cleaning posts...")
            posts_tokens = tokenize(initial_subreddit_posts) if iter == 0 else tokenize(posts_across_all_searches_deduped)
            #print("Example list of post tokens: {}".format(posts_tokens[0])) #TODO: remove
            print("Number of posts after deduping: {}".format(len(posts_tokens)))

            # log some data that we can analyze later on
            analysis_dict["subreddit"].append(self.sub)
            analysis_dict["iteration"].append(iter)
            analysis_dict["num_posts"].append(len(posts_tokens))
            analysis_dict["num_deduped_posts"].append(num_deduped_posts)

            # (3) add all new possible keywords to our new seeding set for next round
            if len(posts_tokens) > 0:
                print("Calculating tf-idf scores for tokens...")
                new_keyword_list, new_keyword_scores = calc_tfidf(posts_tokens)
                self.seeds_set = new_keyword_list

                analysis_dict["keywords"].append(new_keyword_list)
                analysis_dict["keyword_scores"].append(new_keyword_scores)
            else:
                analysis_dict["keywords"].append([])
                analysis_dict["keyword_scores"].append([])

        #print("len of subreddit posts: {}".format(len(subreddit_posts)))
        # extract info from our final list of posts
        for post in subreddit_posts:
            # Save any unique posts to sub_dict.
            # base data format off of: https://raw.githubusercontent.com/camille2019/cs6474_twitter_data_collection/main/character_tweets.csv
            sub_dict['tweet_id'].append(post.id) # actually reddit id but we need to make sure it conforms to the twitter data format above
            sub_dict['author_id'].append(post.author.name)
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
