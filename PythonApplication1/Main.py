import praw
import pdb
import re
import os
import json
import datetime
from time import gmtime, strftime
from RedditBot import RedditBot


#Sheet = https://docs.google.com/spreadsheets/d/1YuAjfZ04yUnb0zZH-v784D0a2Xo3M5-QBRNEkFM210U/edit#gid=0




r = praw.Reddit("bot")
subreddit_name = "socialism" #That's my test subreddit
subreddit = r.subreddit(subreddit_name)

redditBot = RedditBot(subreddit_name);

#Set to true if we want to have this bot write some stats on the submission
bWriteComments = False;


def iteration(submission):
    redditBot.checkSubmission(submission);
    submission.comments.replace_more(limit=None)	
    redditBot.checkComments(submission.comments)
    print("Finished Submission: " + submission.id + " \n");
    if(bWriteComments):
        reply = redditBot.createReply();
        redditBot.submitReply(reply, submission);
    redditBot.refresh();

def loop(list, num):
    index = 0;
    for submission in list:
        iteration(submission)      
        if(index > num):
            break;
        index = index+1

#Begin main loop for the bot to check all submissions
loop(subreddit.new(), 10)
loop(subreddit.hot(), 10)
loop(subreddit.controversial(), 10)
for _ in range(10):
    iteration(subreddit.random())

redditBot.writeCommentRowsToSpreadsheet();
redditBot.writeSubmissionRowsToSpreadsheet();


