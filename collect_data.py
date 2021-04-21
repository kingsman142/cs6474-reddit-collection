import praw
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
             'scare', 'trauma', 'ignor monkey', 'gorilla', 'persecut', 'discriminat', 'prejudice', 'obscen', 'unwelcome', 'no', 'hassle', 'torment', 'irritat', 'aggravat', 'victim', 'aggress', 'crime', 'troll', 'dominat']

# namesets
dc_names = []
dw_names = []
jb_names = []
marvel_names = []
merlin_names = []
sw_names = ['Finn', 'John Boyega']
sh_names = []

# map subreddits to be searched for associated characters
subreddits_to_names = {
    ('/r/StarWars', 'r/StarWarsSpeculation', 'r/StarWarsCanon'): sw_names,
    ('/r/MarvelStudios', '/r/MarvelStudiosSpoilers'): marvel_names,
    ('/r/DCTV', 'r/theflash', 'r/titanstv', 'r/Arrowverse'): dc_names,
    ('/r/merlinbbc'): merlin_names,
    ('/r/SleepyHollow', 'r/SleepyHollowTV'): sh_names,
    ('/r/DoctorWho', '/r/gallifrey'): dw_names,
    ('/r/JamesBond'): jb_names,
    ('/r/Movies', '/r/SciFi', '/r/television'): dc_names + dw_names + jb_names + marvel_names + merlin_names + sw_names + sh_names
}

for (subreddits, names) in subreddits_to_names.items():

    for sr in subreddits:
        for nm in names:
            scraper = scraper.SubredditScraper(reddit_object = reddit, sub = sr, name_searched = nm, seeds_set = seeds_set, seeding_iters = 5, search_limit = 50)
            scraper.get_posts()

