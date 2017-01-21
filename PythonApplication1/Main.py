import praw
import pdb
import re
import os
import json
import datetime
from time import gmtime, strftime
from RedditBot import RedditBot

#Sheet = https://docs.google.com/spreadsheets/d/1YuAjfZ04yUnb0zZH-v784D0a2Xo3M5-QBRNEkFM210U/edit#gid=0

r = praw.Reddit("bot1")
subreddit_name = "socialism"
subreddit = r.subreddit(subreddit_name)

redditBot = RedditBot(subreddit_name);

#Set to true if we want to have this bot write some stats on the submission
bWriteComments = False;


#Begin main loop for the bot to check all submissions
for submission in subreddit.hot():
	submission.comments.replace_more(limit=None)	
	redditBot.checkComments(submission.comments)
	print(redditBot.printModsWhoBanned())
	print("Finished Submission: " + submission.id + " \n\n\n");
	if(bWriteComments):
		reply = redditBot.createReply();
		redditBot.submitReply(reply, submission);
	redditBot.refresh();



