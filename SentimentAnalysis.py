"""
@author Rocorral
ID: 80416750
Instructor: David Aguirre
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
	#print(cmnt)
	if pos_score > neut_score and pos_score > neg_score:
		positive_comments_list.append(cmnt)
		#print("this comment was added to Pos  list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")
	elif neut_score > pos_score and  neut_score > neg_score:
		neutral_comments_list.append(cmnt)
		#print("this comment was added to Neut list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")
	elif neg_score > pos_score and neg_score > neut_score:
		negative_comments_list.append(cmnt)
		#print("this comment was added to Neg  list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")
		

positive_comments_list = []
neutral_comments_list = []
negative_comments_list = []
# The following thread was chosen for the usual emotional charge in political conversation. personally
# I think NLTK can miss context and calculate on good words vs bad. The clear majority of the comments got a neutral rating.
# even some of the sarcastically unsavory ones.
test1 = get_submission_comments('https://www.reddit.com/r/Conservative/comments/9clfbn/the_horror/')
# The second test come from r/awww I wanted to get some positive comments tests as few of the comments in test one got a winning positive score... but oddly no negative
test2 = get_submission_comments('https://www.reddit.com/r/aww/comments/9fjme3/for_my_birthday_i_give_you_one_of_the_sweetest/')
# Test 3 uses a controversial thread with many comments and replies yet I only find 2 negatives. the only 2 negatives in 3 tests. 
#Most threads are moderated for hate speech and vitriolic comments this may be the casue of my results
test3 = get_submission_comments('https://www.reddit.com/r/politics/comments/9florm/ocasiocortez_slams_trumps_puerto_rico_comments_my/')
process_comments(test1,0)
process_comments(test2,0)
process_comments(test3,0)

