import praw
import pdb
import re
import os
import json
import datetime
from time import gmtime, strftime
from GoogleSpreadsheetHandler import GoogleSpreadsheetHandler
from SQLHandler import SQLHandler

class RedditBot(object):

	def __init__(self, subreddit_name):
		self.totalComments = 0
		self.modsWhoDeleted = []
		self.myOwnComment = None
		self.deletedCommentsList = []
		self.sheetHandler= GoogleSpreadsheetHandler();
		self.SQLHandler = SQLHandler();
		self.subredditName = subreddit_name;

    # Return ceddit link to show comment in ceddit.com 
	def getCedditCommentURL(self, comment):
		return "https://www.ceddit.com/r/" + self.subredditName + "/comments/" + comment.submission.id + "/_/" + comment.id;

	def getCedditSubmissionURL(self, submission):
		return "https://www.ceddit.com/r/" + self.subredditName + "/comments/" + submission.id;


    # Check to see if the submission has been removed by lack of author name or submission was banned
	def submission_is_removed(self, submission):
		try:
			author = str(submission.author.name)
		except:
			author = '[Deleted]'
		if not submission.banned_by is None or author is '[Deleted]':
			if not submission.banned_by in modsWhoDeleted:
				self.modsWhoDeleted.append(submission.banned_by)
			return True
		elif submission.author is None or submission.selftext  is '[Deleted]':
			return True
		else:
			return False


	def submission_is_removed2(self, submission):
		if not submission.banned_by is None:
			return True
		try:
			author = str(submission.author.name)
			return
		except:
			try:
				submission.remove()
				submission.approve()
				return
			except:
				return True


    # Check to see if the comment has been removed by lack of author name or comment was banned
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



    # Return date when submission was submitted
	def get__submission_date(self,submission):
		time = submission.created
		return datetime.datetime.time

    # Return date when comment was submitted
	def get_comment_date(self,comment):
		time = comment.created
		return str(datetime.datetime.time)


    # Check submission to handle removed submission and logging them into the database
	def checkSubmission(self,submission):
		if(self.submission_is_removed2(submission)):
			if(self.SQLHandler.checkSubmissionID(submission.id)):
			    return False
			else:
			    print("submission WAS deleted");
			    authorName = "[Deleted]" if submission.author is None else submission.author.name
			    bannedBy = "" if submission.banned_by is None else submission.banned_by
			    self.SQLHandler.insertRow(submission.id, None, self.getCedditSubmissionURL(submission), authorName, submission.selftext , bannedBy);
			    return True;
			return False;


    # Loops through Comments object to handle removed comments and logging them into the database
	def checkComments(self,comments):
		for comment in comments:
			self.checkIfItsMyComment(comment)
			self.totalComments += 1
			if(self.SQLHandler.checkCommentID(comment.submission.id, comment.id)):
			    continue;			
			if self.comment_is_removed(comment):
				self.deletedCommentsList.append(comment)
				authorName = "[Deleted]" if comment.author is None else comment.author.name
				bannedBy = "" if comment.banned_by is None else comment.banned_by
				self.SQLHandler.insertRow(comment.submission.id, comment.id, self.getCedditCommentURL(comment), authorName, comment.body, bannedBy);
			self.checkComments(comment.replies)

    # Return comma separated string of mods
	def printModsWhoBanned(self):
		return  (','.join([str(x) for x in self.modsWhoDeleted]))

    # Returns true if this comment was ours
	def checkIfItsMyComment(self,comment):
		if comment.author == "gackhammer3":
			self.myOwnComment = comment
			return True
		return False

    # Re-initialize class variables
	def refresh(self):
		self.totalComments = 0
		self.modsWhoDeleted = []
		self.myOwnComment = None
		self.deletedCommentsList = []

    # Returns string to post as comment to submission that we're checking
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

    # Submits a reply to a submission
	def submitReply(self,reply, submission):
		try:
			if self.myOwnComment is None:
				submission.reply(reply)
			else:
				self.myOwnComment.edit(reply)
		except: 
			print("archived post")	

	def writeCommentRowsToSpreadsheet(self):
		rows = self.SQLHandler.getAllCommentsFromThisIteration();
		self.sheetHandler.writeToSheet(rows, True);


	def writeSubmissionRowsToSpreadsheet(self):
		rows = self.SQLHandler.getAllSubmissionsFromThisIteration();
		self.sheetHandler.writeToSheet(rows, False);

	
