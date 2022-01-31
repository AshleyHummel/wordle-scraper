# Python program that uses PRAW to scrape the r/wordle subreddit's "Daily Wordle" post to collect
# users' scores in order to analyze them.

# RESOURCES
# PRAW setup from https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
# plotly setup from https://plotly.com/python/basic-charts/
# menu --> https://computinglearner.com/how-to-create-a-menu-for-a-python-console-application/ 


# used to import environment variables
import os
from dotenv import load_dotenv

import praw
import pandas as pd

# plotly
import plotly.express as px
import plotly.graph_objects as go

load_dotenv(".env") # private environment variables are located in a local .env file

# Print program info and collect initial reddit info from user
print('------------------------------------------------------------------------------------'
    + '\n\t\t\tWelcome to Wordle Scraper!'
    + '\n\tA program that scrapes subreddit r/wordle\'s daily thread' 
    + '\n\t\t  to provide today\'s Wordle statistics!'
    + '\n------------------------------------------------------------------------------------')
url = input('To begin, visit https://www.reddit.com/r/wordle/'
          + '\nand enter the URL for today\'s \"Daily Wordle\" thread: ')

print('\nCollecting Redditors\' Wordle scores...')

# Read-only reddit instance
reddit = praw.Reddit(client_id=os.environ.get('CLIENT_ID'),                        # your client id
                              client_secret=os.environ.get('CLIENT_SECRET'),      # your client secret
                              user_agent="wordle-scraper")                        # your user agent

# subreddit instance
subreddit = reddit.subreddit("wordle")

# url = "https://www.reddit.com/r/wordle/comments/seu7nx/daily_wordle_224_saturday_29_january_2022/"
submission = reddit.submission(url=url) # create submission instance from url of "Daily Wordle"

postTitle = submission.title

scoresList = [0,0,0,0,0,0]; # each index+1 represents number of scores found for that score (1/6 - 6/6)
count = 0 # total number of scores analyzed
sum = 0 # sum of all scores

# comment instance
for top_level_comment in submission.comments:
  # look for "/6", which indicates a score
  indexOfScore = top_level_comment.body.index("/6") if "/6" in top_level_comment.body else -1
  
  if indexOfScore != -1:
    fullScore = top_level_comment.body[indexOfScore-1:indexOfScore+2]
    score = int(fullScore[0]) # just the number part of the score
    # print(fullScore)
    # print(score)
    scoresList[score - 1] += 1 # increased index of score to keep track of individual scores found
    count += 1
    sum += score
    # print(scoresList)  

print('Done!')

# ---------- MENU ----------
menu_options = {
    1: 'View today\'s stats',
    2: 'View pie chart',
    3: 'View bar graph',
    4: 'Exit',
}

def print_menu():
    print('\n------------------------------------------')
    for key in menu_options.keys():
        print(key, '--', menu_options[key])
    print('------------------------------------------')

while(True):
  print_menu()
  option = ''
  try:
    option = int(input('Enter your choice: '))
  except:
    print('Wrong input. Please enter a number ...')
  # 1) Today's stats
  if option == 1:
      # calculate average
      average = sum / count

      # calculate mode
      max = 0 # keeps track of largest number of occurrences of a score
      mode = 0
      index = 0
      for val in scoresList:
        if val > max:
          max = val
          mode = index + 1
        index += 1

      print('\nAverage score: ' + str(round(average)) + ' (' + str('{0:.3g}'.format(average)) + ')'
          + '\nMode (most frequent score): ' + str(mode) + "/6")
  # 2) Pie chart
  elif option == 2:
      print('Opening pie chart in a window...')
      labels = ['1/6', '2/6', '3/6', '4/6', '5/6', '6/6']
      values = [scoresList[0], scoresList[1], scoresList[2], scoresList[3], scoresList[4], scoresList[5]]

      colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

      pieChart = go.Figure(data=[go.Pie(labels=labels, values=values)])
      pieChart.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
      pieChart.update_layout(title_text=postTitle)
  
      pieChart.show()
  # 3) Bar graph
  elif option == 3:
      print('Opening bar graph in a window...')
      
      scores = ['1/6', '2/6', '3/6', '4/6', '5/6', '6/6']

      barGraph = go.Figure()
      barGraph.add_trace(go.Bar(
          x = scores,
          y = [scoresList[0], scoresList[1], scoresList[2], scoresList[3], scoresList[4], scoresList[5]],
          name='Primary Product',
          marker_color='indianred'
      ))

      barGraph.update_layout(
        title_text=postTitle,
        xaxis=dict(title='Scores'),
        yaxis=dict(title='Occurrences')
      )

      barGraph.show()
  # 4) Exit
  elif option == 4:
      print('Exiting Wordle Scraper... goodbye!\n')
      exit()
  else:
      print('Invalid option. Please enter a number between 1 and 4.')