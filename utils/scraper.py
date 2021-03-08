import pandas as pd

class SubredditScraper:
    def __init__(self, reddit_object, sub, lim=900, mode='w'):
        self.sub = sub
        self.lim = lim
        self.mode = mode
        self.reddit = reddit_object
        print('SubredditScraper instance created with values: sub = {}, lim = {}, mode = {}'.format(sub, lim, mode))

    def get_posts(self):
        """Get unique posts from a specified subreddit."""

        sub_dict = {
            'selftext': [], 'title': [], 'id': [], 'sorted_by': [],
            'num_comments': [], 'score': [], 'ups': [], 'downs': [], 'dates': []}
        csv = '{}_posts.csv'.format(self.sub)

        # Set csv_loaded to True if csv exists since you can't
        # evaluate the truth value of a DataFrame.
        df, csv_loaded = (pd.read_csv(csv), True) if isfile(csv) else ('', False)

        print('csv = {}'.format(csv))
        print('csv_loaded = {}'.format(csv_loaded))

        print('Collecting information from r/{}.'.format(self.sub))
        subreddit_posts = self.reddit.subreddit(self.sub).top(limit=self.lim)

        for post in subreddit_posts:
            # Check if post.id is in df and set to True if df is empty.
            # This way new posts are still added to dictionary when df = ''
            unique_id = post.id not in tuple(df.id) if csv_loaded else True

            # Save any unique posts to sub_dict.
            if unique_id:
                sub_dict['selftext'].append(post.selftext)
                sub_dict['title'].append(post.title)
                sub_dict['id'].append(post.id)
                sub_dict['sorted_by'].append(sort)
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
