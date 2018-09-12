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

def process_comments(comments,c):

	
	if c==len(comments) or comments is None:
		return
	
	pos = get_text_positive_proba(comments[c].body)
	neut = get_text_neutral_proba(comments[c].body)
	neg = get_text_negative_proba(comments[c].body)

	
	list_sorting(comments[c].body,pos,neut,neg)

	process_comments(comments[c].replies,0)
	process_comments(comments,c+1)

def list_sorting(cmnt,pos_score,neut_score,neg_score):
	if pos_score > neut_score >neg_score:
		pos_c_list.append(cmnt)
		print("this comment was added to Pos  list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")
	if neut_score > pos_score >neg_score:
		neu_c_list.append(cmnt)
		print("this comment was added to Neut list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")
	if neg_score > pos_score > neut_score:
		neg_c_list.append(cmnt)
		print("this comment was added to Neg  list with a Pos Score of",pos_score," a neg score of ",neg_score," and a neut_score of ",neut_score," -------->")

pos_c_list = []
neu_c_list = []
neg_c_list =[]

comments = get_submission_comments('https://www.reddit.com/r/Conservative/comments/9clfbn/the_horror/')
process_comments(comments,0)

