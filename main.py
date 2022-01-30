# Python program that uses PRAW to scrape the r/wordle subreddit's "Daily Wordle" post to collect
# users' scores in order to analyze them.

# setup from https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

# used to import environment variables
import os
from dotenv import load_dotenv

import praw
import pandas as pd

# plotly
import plotly.express as px
import plotly.graph_objects as go

load_dotenv(".env") # private environment variables are located in a local .env file

# Read-only reddit instance
reddit = praw.Reddit(client_id=os.environ.get('CLIENT_ID'),                        # your client id
                              client_secret=os.environ.get('CLIENT_SECRET'),      # your client secret
                              user_agent="wordle-scraper")                        # your user agent

# subreddit instance
subreddit = reddit.subreddit("wordle")

url = "https://www.reddit.com/r/wordle/comments/seu7nx/daily_wordle_224_saturday_29_january_2022/"
submission = reddit.submission(url=url) # create submission instance from url of "Daily Wordle"

postTitle = submission.title

scoresList = [0,0,0,0,0,0]; # each index+1 represents number of scores found for that score (1/6 - 6/6)

# comment instance
for top_level_comment in submission.comments:
  # look for "/6", which indicates a score
  indexOfScore = top_level_comment.body.index("/6") if "/6" in top_level_comment.body else -1
  
  if indexOfScore != -1:
    fullScore = top_level_comment.body[indexOfScore-1:indexOfScore+2]
    score = int(fullScore[0]) # just the number part of the score
    # print(fullScore)
    # print(score)
    scoresList[score - 1] += 1
    # print(scoresList)  

# TODO: MENU
# User inputs URL of daily wordle
# View today's stats (mean and mode)
# Pie chart
# bar graph

# ---------- pie chart ----------
labels = ['1/6', '2/6', '3/6', '4/6', '5/6', '6/6']
values = [scoresList[0], scoresList[1], scoresList[2], scoresList[3], scoresList[4], scoresList[5]]

colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen'] # TODO

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.update_layout(title_text=postTitle)

fig.show()