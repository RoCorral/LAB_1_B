"""
@author Rocorral
ID: 80416750
Instructor: David Aguirre
Section: TR 1030-1150
Assignment:Lab 1-B - Recursion
Last Modification: 09/13/2018
Program Purpose: The purpose of this program is to practice recursive algorithm problem
solving andbuilding. by Using methods built in to the provided NLTK and PRAW software we 
can access Reddit submission and break down their comment and reply trees into traversable 
data. We must implement a recursive algorithm to process all comments and designate
them to appropriate lists based on the results of NLTK's Sentiment analysis.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='rHnLiSk0DwewqQ',
                     client_secret='0vIYtaw6gvZYTowoA1EvjWHdDj8',
                     user_agent='B+'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments
#Begin My Code
def process_comments(comments,c):
	#base case returns after reaching maximum reply depth + 1.
	if c==len(comments) or comments is None:
		return
	#test the comment for Sentiment scores
	pos = get_text_positive_proba(comments[c].body)
	neut = get_text_neutral_proba(comments[c].body)
	neg = get_text_negative_proba(comments[c].body)
	#passes sentiment scores and comment to sorting def
	list_sorting(comments[c].body,pos,neut,neg)
	#recursive call passing the current comments first reply making it current comment in the next call getting one level deeper into the replies.  
	process_comments(comments[c].replies,0)
	#recursive call remaining in current comment depth but next comment down list
	process_comments(comments,c+1)
#sorting Def taking in scores and comment to be placed in appropriate list based on score
def list_sorting(cmnt,pos_score,neut_score,neg_score):
	if pos_score > neut_score >neg_score:
		positive_comments_list.append(cmnt)
		#print("this comment was added to Pos  list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")
	if neut_score > pos_score >neg_score:
		neutral_comments_list.append(cmnt)
		#print("this comment was added to Neut list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")
	if neg_score > pos_score > neut_score:
		negative_comments_list.append(cmnt)
		#print("this comment was added to Neg  list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")


positive_comments_list = []
neutral_comments_list = []
negative_comments_list = []
#the following thread was chosen for the usual emotional charge in political conversation
comments = get_submission_comments('https://www.reddit.com/r/Conservative/comments/9clfbn/the_horror/')
process_comments(comments,0)


