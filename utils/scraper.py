import os
from time import sleep

import pandas as pd

from utils.calculations import calc_tfidf
from utils.tokenizer import tokenize

class SubredditScraper:
    def __init__(self, reddit_object, sub, seeds_set, seeding_iters, lim=900, mode='w'):
        self.sub = sub
        self.lim = lim
        self.mode = mode
        self.seeds_set = seeds_set
        self.seeds_iters = seeding_iters
        self.reddit = reddit_object
        print('SubredditScraper instance created with values: sub = {}, lim = {}, mode = {}'.format(sub, lim, mode))

    def get_posts(self):
        """Get unique posts from a specified subreddit."""
        sub_dict = {
            'selftext': [], 'title': [], 'id': [], 'num_comments': [],
            'score': [], 'ups': [], 'downs': [], 'dates': []}
        csv = '{}_posts.csv'.format(self.sub)

        # Set csv_loaded to True if csv exists since you can't
        # evaluate the truth value of a DataFrame.
        df, csv_loaded = (pd.read_csv(csv), True) if os.path.isfile(csv) else ('', False)

        print('csv = {}'.format(csv))
        print('csv_loaded = {}'.format(csv_loaded))

        print('Collecting information from r/{}.'.format(self.sub))
        initial_subreddit_posts = []
        subreddit_posts = []
        unique_post_ids = set()
        for iter in range(self.seeds_iters):
            # (1) find all posts that contain keywords in the seeding list
            all_search_posts = []
            for keyword in self.seeds_set:
                curr_search_posts = self.reddit.subreddit(self.sub).search(query = keyword)
                all_search_posts += curr_search_posts

            # (2) remove duplicate posts (dedup)
            for post in all_search_posts:
                if post.id not in unique_post_ids:
                    unique_post_ids.add(post.id)
                    if iter == 0:
                        initial_subreddit_posts.append(post)
                    else:
                        subreddit_posts.append(post)
                        
            # clean and tokenize post bodies
            posts_tokens = tokenize(subreddit_posts)

            # (3) add all new possible keywords to our new seeding set for next round
            new_keyword_list, _ = calc_tfidf(posts_tokens)

            self.seeds_set = new_keyword_list

        # extract info from our final list of posts
        for post in subreddit_posts:
            # Check if post.id is in df and set to True if df is empty.
            # This way new posts are still added to dictionary when df = ''
            unique_id = post.id not in tuple(df.id) if csv_loaded else True

            # Save any unique posts to sub_dict.
            if unique_id:
                sub_dict['selftext'].append(post.selftext)
                sub_dict['title'].append(post.title)
                sub_dict['id'].append(post.id)
                sub_dict['num_comments'].append(post.num_comments)
                sub_dict['score'].append(post.score)
                sub_dict['ups'].append(post.ups)
                sub_dict['downs'].append(post.downs)
                sub_dict['dates'].append(post.created_utc)
            sleep(0.1)

        new_df = pd.DataFrame(sub_dict)

        # Add new_df to df if df exists then save it to a csv.
        if 'DataFrame' in str(type(df)) and self.mode == 'w':
            pd.concat([df, new_df], axis=0, sort=0).to_csv(csv, index=False)
            print('{} new posts collected and added to {}'.format(len(new_df), csv))
        elif self.mode == 'w':
            new_df.to_csv(csv, index=False)
            print('{} posts collected and saved to {}'.format(len(new_df), csv))
        else:
            print('{} posts were collected but they were not added to {} because mode was set to "{}"'.format(len(new_df), csv, self.mode))
