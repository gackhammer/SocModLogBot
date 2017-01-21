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

bWriteComments = False;

for submission in subreddit.hot():
	submission.comments.replace_more(limit=None)	
	redditBot.checkComments(submission.comments)
	print(redditBot.printModsWhoBanned())
	print("Finished Submission: " + submission.id + " \n\n\n");
	if(bWriteComments):
		reply = redditBot.createReply();
		redditBot.submitReply(reply, submission);
	redditBot.refresh();

'''
if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []

else:
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

'''




'''
if re.search("i love python", comment.body.lower(), re.IGNORECASE):
	comment.reply("Botty bot says: Me too!!")
	print("Bot replying to : ", submission.title)
	posts_replied_to.append(submission.id)
'''

'''
with open("posts_replied_to.txt", "w") as f:
	for post_id in posts_replied_to:
		f.write(post_id + "\n")

'''






'''
for submission in subreddit.hot(limit=2):
    print("Title: ", submission.title)
    print("Text: ", submission.selftext)
    print("Score: ", submission.score)
    print("---------------------------------\n")
'''

    