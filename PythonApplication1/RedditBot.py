import praw
import pdb
import re
import os
import json
import datetime
from time import gmtime, strftime
from GoogleSpreadsheetHandler import GoogleSpreadsheetHandler

class RedditBot(object):

	def __init__(self, subreddit_name):
		self.totalComments = 0
		self.modsWhoDeleted = []
		self.myOwnComment = None
		self.deletedCommentsList = []
		self.sheetHandler= GoogleSpreadsheetHandler();
		self.subredditName = subreddit_name;

	def getCedditURL(self, comment):
		return "https://www.ceddit.com/r/" + self.subredditName + "/comments/" + comment.submission.id + "/_/" + comment.id;

	def submission_is_removed(self, sub_id):
		s = r.get_submission(submission_id=sub_id)
		try:
			author = str(s.author.name)
		except:
			author = '[Deleted]'
		if not s.banned_by is None or author is '[Deleted]':
			if not s.banned_by in modsWhoDeleted:
				self.modsWhoDeleted.append(s.banned_by)
			return True
		elif s.author is None or s.body is '[Deleted]':
			return True
		else:
			return False


	def comment_is_removed(self,comment):
		try:
			author = str(comment.author.name)
		except:
			author = '[Deleted]'
		if not comment.banned_by is None or author is '[Deleted]':
			if not comment.banned_by in self.modsWhoDeleted:
				self.modsWhoDeleted.append(comment.banned_by)
			return True
		else:
			return False




	def get__submission_date(self,submission):
		time = submission.created
		return datetime.datetime.time

	def get_comment_date(self,comment):
		time = comment.created
		return str(datetime.datetime.time)

	def checkComments(self,comments):
		for comment in comments:
			self.checkIfItsMyComment(comment)
			self.totalComments += 1
			if self.comment_is_removed(comment):
				self.deletedCommentsList.append(comment)
				authorName = "[Deleted]" if comment.author is None else comment.author.name
				bannedBy = "" if comment.banned_by is None else comment.banned_by
				self.sheetHandler.writeToSheet(comment.submission.id, comment.id, self.getCedditURL(comment), authorName, comment.body, bannedBy );
			self.checkComments(comment.replies)

	def printModsWhoBanned(self):
		return  (','.join([str(x) for x in self.modsWhoDeleted]))

	def checkIfItsMyComment(self,comment):
		if comment.author == "gackhammer3":
			self.myOwnComment = comment
			return True
		return False

	def refresh(self):
		self.totalComments = 0
		self.modsWhoDeleted = []
		self.myOwnComment = None
		self.deletedCommentsList = []

	def createReply(self):
		d = datetime.date.today()
		d = datetime.date.today()
		strBotReply = "*Beep Boop Bleep Blop I'm a bot*. \n\n I'm just testing out some of my code. Here's some info about the mods' activity this in this thread "
		strBotReply += "\n\n**Number of comments and replies removed by mods:** " + str(len(self.deletedCommentsList))
		strBotReply += "\n\n**Total Comments and Replies Counted:**(including mod removed): " + str(self.totalComments + (1 if self.myOwnComment is None else 0))
		if(len(self.printModsWhoBanned()) > 0):
			strBotReply += "\n\n **Names of Mods who removed comments in this thread:** *" + self.printModsWhoBanned() + "*"
		strBotReply += " \n\n --------------------------------------------------------------------- "
		strBotReply += "\n\n I last checked this thread on: **" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT**"
		strBotReply += "\n\n If you want to check the entire mod log that I make, click here: "
		strBotReply += "\n\n If you find any bugs with what I'm doing, send a PM to me (yes, to me... the bot) and I'll have some developers check it out: "
		print(strBotReply)
		return strBotReply

	def submitReply(self,reply, submission):
		try:
			if self.myOwnComment is None:
				submission.reply(reply)
			else:
				self.myOwnComment.edit(reply)
		except: 
			print("archived post")	

	