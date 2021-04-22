import os

import praw
import pandas as pd

from utils import scraper

# intialize reddit and scraper objects
# automatically retrieves credentials from DEFAULT section of praw.ini file in this directory
reddit = praw.Reddit()

# test for finn from star wars on r/starwars
# seeds_set = ['racebend', 'black']
# scraper = scraper.SubredditScraper(reddit_object = reddit, sub = "starwars", name_searched = "boyega", seeds_set = seeds_set, seeding_iters = 5, search_limit = 50)
# scraper.get_posts()

# seed keywords
seeds_set = ['racebend', 'black', 'white', 'color', 'divers', 'politic', 'rac', 'annoy', 'remove', 'hate', 'never', 'not', 'dislike', 'disturb', 'threat', 'scrutiniz', 'humiliat', 'angry', 'rage', 'pander', 'nostalg',
             'scare', 'trauma', 'ignor', 'monkey', 'gorilla', 'persecut', 'discriminat', 'prejudice', 'obscen', 'unwelcome', 'no', 'hassle', 'torment', 'irritat', 'aggravat', 'victim', 'aggress', 'crime', 'troll', 'dominat']

# namesets
dc_names = []
dw_names = []
jb_names = []
marvel_names = []
merlin_names = []
sw_names = ['Finn', 'John Boyega']
sh_names = []

# map subreddits to be searched for associated characters
'''subreddits_to_names = {
    ('/r/StarWars', 'r/StarWarsSpeculation', 'r/StarWarsCanon'): sw_names,
    ('/r/MarvelStudios', '/r/MarvelStudiosSpoilers'): marvel_names,
    ('/r/DCTV', 'r/theflash', 'r/titanstv', 'r/Arrowverse'): dc_names,
    ('/r/merlinbbc'): merlin_names,
    ('/r/SleepyHollow', 'r/SleepyHollowTV'): sh_names,
    ('/r/DoctorWho', '/r/gallifrey'): dw_names,
    ('/r/JamesBond'): jb_names,
    ('/r/Movies', '/r/SciFi', '/r/television'): dc_names + dw_names + jb_names + marvel_names + merlin_names + sw_names + sh_names
}'''

names_to_subreddits = {
    sw_names: ['/r/StarWars', 'r/StarWarsSpeculation', 'r/StarWarsCanon', '/r/Movies', '/r/SciFi', '/r/television'],
    marvel_names: ['/r/MarvelStudios', '/r/MarvelStudiosSpoilers', '/r/Movies', '/r/SciFi', '/r/television'],
    dc_names: ['/r/DCTV', 'r/theflash', 'r/titanstv', 'r/Arrowverse', '/r/Movies', '/r/SciFi', '/r/television'],
    merlin_names: ['/r/merlinbbc', '/r/Movies', '/r/SciFi', '/r/television'],
    sh_names: ['/r/SleepyHollow', 'r/SleepyHollowTV', '/r/Movies', '/r/SciFi', '/r/television'],
    dw_names: ['/r/DoctorWho', '/r/gallifrey', '/r/Movies', '/r/SciFi', '/r/television'],
    jb_names: ['/r/JamesBond', '/r/Movies', '/r/SciFi', '/r/television']
}

for (names, subreddits) in names_to_subreddits.items():
    for name in names:
        final_posts_df = pd.DataFrame({'tweet_id': [], 'author_id': [], 'date': [], 'text': [], 'name_searched': [], 'title': [], 'num_comments': [], 'score': [], 'ups': [], 'downs': [], 'subreddit': []})
        final_analytics_df = pd.DataFrame({"subreddit": [], "iteration": [], "keywords": [], "keyword_scores": [], "num_posts": [], "num_deduped_posts": []})
        for subreddit in subreddits:
            # collect data for this character/actor in this specific subreddit
            scraper = scraper.SubredditScraper(reddit_object = reddit, sub = sr, name_searched = nm, seeds_set = seeds_set, seeding_iters = 5, search_limit = 50)
            subreddit_posts_df, subreddit_analytics_df = scraper.get_posts()

            # attach this subreddit's data to an ongoing dataframe we're constructing containing all this character/actor's data
            final_posts_df = pd.concat([final_posts_df, subreddit_posts_df])
            final_analytics_df = pdf.concat([final_analytics_df, subreddit_analytics_df])

        posts_csv = '{}_posts.csv'.format(name)
        analytics_csv_name = "{}_analytics.csv".format(name)

        # save both CSVs to file
        final_posts_df.to_csv(posts_csv, index=False)
        final_analytics_df.to_csv(analytics_csv_name, index=False)
        print('{} posts collected and saved to {}'.format(len(final_posts_df), posts_csv))
        print('{} events logged (for analytics) and saved to {}'.format(len(final_analytics_df), analytics_csv_name))
