# Python program that uses PRAW to scrape the r/wordle subreddit's "Daily Wordle" post to collect
# users' scores in order to analyze them.

# setup from https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

import praw
import pandas as pd

# Read-only reddit instance
reddit_read_only = praw.Reddit(client_id="",         # your client id
                               client_secret="",      # your client secret
                               user_agent="")        # your user agent

# subreddit instance
subreddit = reddit.subreddit("wordle")

url = "https://www.reddit.com/r/wordle/comments/seu7nx/daily_wordle_224_saturday_29_january_2022/"
submission = reddit.submission(url) # create submission instance from url of "Daily Wordle"

# comment instance
# all_comments = submission.comments.list()