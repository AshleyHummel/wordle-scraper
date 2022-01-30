# Python program that uses PRAW to scrape the r/wordle subreddit's "Daily Wordle" post to collect
# users' scores in order to analyze them.

# setup from https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

# used to import environment variables
import os
from dotenv import load_dotenv

import praw
import pandas as pd

load_dotenv(".env") # private environment variables are located in a local .env file

# Read-only reddit instance
reddit = praw.Reddit(client_id=os.environ.get('CLIENT_ID'),         # your client id
                               client_secret=os.environ.get('CLIENT_SECRET'),      # your client secret
                               user_agent="wordle-scraper")        # your user agent

# subreddit instance
subreddit = reddit.subreddit("wordle")

url = "https://www.reddit.com/r/wordle/comments/seu7nx/daily_wordle_224_saturday_29_january_2022/"
submission = reddit.submission(url=url) # create submission instance from url of "Daily Wordle"

# comment instance
for top_level_comment in submission.comments:
    indexOfScore = top_level_comment.body.find("/6") # look for "/6", which indicates a score
    score = top_level_comment.body[indexOfScore-1:indexOfScore+2] # take substring of entire score ("#/6")
    print(score)

# TODO - put scores in a list, find average... DISPLAY SOMETHING