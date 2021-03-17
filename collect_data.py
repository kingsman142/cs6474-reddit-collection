import praw
from utils import scraper

# intialize reddit and scraper objects
reddit = praw.Reddit() # automatically retrieves credentials from DEFAULT section of praw.ini file in this directory

# test for finn from star wars on r/starwars
seeds_set = ['racebend', 'black']#, 'white', 'color', 'divers', 'politic', 'rac', 'annoy', 'remove', 'hate', 'never', 'not', 'dislike', 'disturb', 'threat', 'scrutiniz', 'humiliat', 'angry', 'rage', 'pander', 'nostalg', 'scare', 'trauma', 'ignor monkey', 'gorilla', 'persecut', 'discriminat', 'prejudice', 'obscen', 'unwelcome', 'no', 'hassle', 'torment', 'irritat', 'aggravat', 'victim', 'aggress', 'crime', 'troll', 'dominat', 'finn', 'john', 'boyega']
scraper = scraper.SubredditScraper(reddit_object = reddit, sub = "starwars", seeds_set = seeds_set, seeding_iters = 5, search_limit = 50)
scraper.get_posts()
