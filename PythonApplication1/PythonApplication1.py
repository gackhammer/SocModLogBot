import praw
import pdb
import re
import os

r = praw.Reddit("bot1")


subreddit = r.subreddit("RiseOfNationsScens")

if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []

else:
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

print('its doing something')

for submission in subreddit.hot(limit=5):
	for comment in submission.comments:
		if re.search("i love python", comment.body.lower(), re.IGNORECASE):
			comment.reply("Botty bot says: Me too!!")
			print("Bot replying to : ", submission.title)
			posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
	for post_id in posts_replied_to:
		f.write(post_id + "\n")






def submission_is_removed(sub_id):
    s = r.get_submission(submission_id=sub_id)
    try:
        author = str(s.author.name)
    except:
        author = '[Deleted]'
    if not s.banned_by is None or author is '[Deleted]':
        return True
    else:
        return False

def comment_is_removed(comment):
    try:
        author = str(comment.author.name)
    except:
        author = '[Deleted]'
    if not comment.banned_by is None or author is '[Deleted]':
        return True
    else:
        return False


def get__submission_date(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)

def get_comment_date(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)


'''
for submission in subreddit.hot(limit=2):
    print("Title: ", submission.title)
    print("Text: ", submission.selftext)
    print("Score: ", submission.score)
    print("---------------------------------\n")
'''

    