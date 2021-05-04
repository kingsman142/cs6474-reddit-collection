import os

import praw
import pandas as pd

from utils import scraper

# intialize reddit and scraper objects
# automatically retrieves credentials from DEFAULT section of praw.ini file in this directory
reddit = praw.Reddit()

# seed keywords
seeds_set = ['racebend', 'black', 'white', 'color', 'divers', 'politic', 'rac', 'annoy', 'remove', 'hate', 'never', 'not', 'dislike', 'disturb', 'threat', 'scrutiniz', 'humiliat', 'angry', 'rage', 'pander', 'nostalg',
             'scare', 'trauma', 'ignor', 'monkey', 'gorilla', 'persecut', 'discriminat', 'prejudice', 'obscen', 'unwelcome', 'no', 'hassle', 'torment', 'irritat', 'aggravat', 'victim', 'aggress', 'crime', 'troll', 'dominat']

# namesets
dc_names = ('iris west', 'diggle', 'black canary', 'starfire', 'deadshot', 'candace patton', 'will smith', 'david ramsey',
            'anna diop', 'jurnee smollett', 'harley', 'margot robbie', 'stephen mmell', 'oliver queen', 'green arrow', 'danielle panabaker', 'killer frost', 'jared leto', 'joker', 'mary elizabeth winstead', 'huntress')
dis_names = ('ariel', 'little mermaid', 'halle bailey',
             'emma watson', 'belle', 'cinderella', 'sleeping beauty', 'lily james', 'maleficent', 'angelina jolie', 'grace van dien')
dw_names = ('bill potts', 'pearl mackie', 'clara oswald', 'jenna coleman', 'rose tyler',
            'billie piper', 'freema agyeman', 'martha jones', 'jo martin', 'jodie whittaker', '13th doctor', '14th doctor')
jb_names = ('bond', 'nomi', 'moneypenny', 'daniel craig',
            'idris elba', 'lashana lynch', 'naomie harris', 'M', 'vesper lynd', 'madeleine swann', 'judi dench', 'eva green', 'lea seydoux', 'pierce brosnan')
marvel_names = ('sam wilson', 'domino', 'valkyrie', 'nick fury', 'heimdall', 'anthony mackie', 'zazie beetz', 'tessa thompson', 'samuel l. jackson',
                'idris elba', 'bucky', 'sebastian stan', 'miles morales', 'donald glover', 'peter parker', 'tom holland', 'mj', 'zendaya', 'black widow', 'scarlett johansson', 'jane foster', 'natalie portman', 'jeremy renner', 'hawkeye', 'brianna hildebrand', 'negasonic teenage warhead')
merlin_names = ('merlin', 'arthur', 'guinevere',
                'colin morgan', 'bradley james', 'angel coulby')
sw_names = ('john boyega', 'kylo ren', 'rey',
            'daisey ridley', 'jannah', 'naomie ackie')
sh_names = ('abbie', 'crane', 'nicole beharie', 'tom mison')

# NOTE: removed 'finn' from sw_names temporarily

# map subreddits to be searched for associated characters
names_to_subreddits = {
    sw_names: ['StarWars', 'StarWarsSpeculation', 'StarWarsCanon', 'Movies', 'SciFi', 'television'],
    marvel_names: ['MarvelStudios', 'MarvelStudiosSpoilers', 'Movies', 'SciFi', 'television'],
    dc_names: ['DCTV', 'theflash'],#, 'titanstv', 'Arrowverse'],#, 'Movies', 'SciFi', 'television'],
    dis_names: ['Movies', 'Disney'],
    merlin_names: ['merlinbbc', 'Movies'],#, 'SciFi', 'television'],
    sh_names: ['SleepyHollow', 'SleepyHollowTV'],#, 'Movies', 'SciFi'],#, 'television'],
    dw_names: ['DoctorWho', 'gallifrey'],#, 'Movies', 'SciFi'],#, 'television'],
    jb_names: ['JamesBond', 'Movies'],#, 'SciFi', 'television']
}

for (names, subreddits) in names_to_subreddits.items():
    for name in names:
        print("= Collecting data for {}...".format(name))
        final_posts_df = pd.DataFrame({'tweet_id': [], 'author_id': [], 'date': [], 'text': [], 'name_searched': [],
            'title': [], 'num_comments': [], 'score': [], 'ups': [], 'downs': [], 'subreddit': []})
        final_analytics_df = pd.DataFrame({"subreddit": [], "iteration": [], "keywords": [],
            "keyword_scores": [], "num_posts": [], "num_deduped_posts": []})
        for subreddit in subreddits:
            print("== Collecting data on the {} subreddit...".format(subreddit))
            # collect data for this character/actor in this specific subreddit
            # sedding_iters = 5, search_limit = 50 for all names before miles morales
            # in tokenizer.py, changed comments limit from 5 to 2 and search_limit = 25 was reduced to 15 for all names that were peter parker or after that
            # starting with margot abbie in the dc names, I capped all subreddit lists to the first 4 subreddits + included initial_subreddit_posts in total subreddit_posts list
            posts_scraper = scraper.SubredditScraper(
                reddit_object=reddit, sub=subreddit, name_searched=name, seeds_set=seeds_set, seeding_iters=2, search_limit=15)
            subreddit_posts_df, subreddit_analytics_df = posts_scraper.get_posts()

            #print("len of subreddt_posts_df")
            #print(len(subreddit_posts_df))

            # attach this subreddit's data to an ongoing dataframe we're constructing containing all this character/actor's data
            final_posts_df = pd.concat([final_posts_df, subreddit_posts_df])
            final_analytics_df = pd.concat(
                [final_analytics_df, subreddit_analytics_df])

        posts_csv = '{}_posts.csv'.format(name)
        analytics_csv_name = "{}_analytics.csv".format(name)

        # save both CSVs to file
        if not os.path.exists("reddit-data"):
            os.mkdir("reddit-data")
        if not os.path.exists("reddit-analytics"):
            os.mkdir("reddit-analytics")

        print(final_posts_df)

        final_posts_df.to_csv(os.path.join("reddit-data", posts_csv), index=False)
        final_analytics_df.to_csv(os.path.join("reddit-analytics", analytics_csv_name), index=False)
        print('{} posts collected and saved to {}'.format(
            len(final_posts_df), posts_csv))
        print('{} events logged (for analytics) and saved to {}'.format(
            len(final_analytics_df), analytics_csv_name))
