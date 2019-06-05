import math
import tqdm
import time
import numpy as np
from numpy import int32
import pandas as pd
import boto3


PASSWORD ='12_06_2018_1500'

#message_subject = 'Earn up to $0.20 in less than a minute playing The Estimation Game'
#message_subject_2 = 'Play the Estimation Game at 1:30pm CT (2:30pm ET) today! Earn up to $1 in less than 5 minutes!'

#message_text = 'Great news! Real Time Labs has a new task, \'The Estimation Game,\' an easy and fun way to earn.\n\nIt\'s simple: we ask a question, and you give your best answer. The whole thing takes less than a minute!\n\nYou get 10 cents for completing the task, and *up to* 10 cents extra based on accuracy.\n\nDue to the way this task is run, all payments are submitted via bonus.\n\nTo make it faster for you, this email includes a direct link to participate, which automatically logs your MTurk ID for payment via bonus. Your bonus will be attached to the original survey HIT you completed with Kellogg Behavioral Research.\n\nClick the link below to participate.\n\n' + link
#message_text_2 = 'Play the Estimation Game at 1:30pm CT (2:30pm ET) today! Earn up to $1 in less than 5 minutes!\n\n˗ˏˋ THE ESTIMATION GAME ˊˎ˗‏\n\nExciting news! Real Time Labs at Northwestern University is launching a series of estimation tasks---a fun, easy way to make above-average earnings.\n\nThe Estimation Game asks you to answer a brief question. That\'s it! The task takes 3-5 minutes including wait time, and will offer a base pay of 50 cents. You can also earn an extra 50 cents for correct answers. (That\'s $6-20/hour depending on accuracy and wait time.)\n\nBecause we need many people simultaneously, we\'re running this study a bit differently. Instead of posting a HIT, we\'ll send you a direct access link. All payments for this study will be via bonus to your Kellogg Behavioral Lab enrollment HIT.\n\n˗ˏˋ HOW IT WORKS ˊˎ˗‏\n\nThe game will start at exactly 1:30pm CT. (2:30pm ET.)\n\nWe will send a link about 15 minutes before game time.\n\nThis link will *close* at exactly 1:30pm CT. (2:30pm ET.) You must enter the game at or before 1:30pm CT (2:30pm ET) in order to participate.\n\nIf you arrive early, you\'ll be shown a countdown to start time.\n\nAfter the link closes at 1:30pm CT, there will be up to 1 minute additional wait time to ensure everyone is synchronized.\n\nThe game itself takes a maximum of 3 minutes.'


#message_subject_3 = '[Real Time Labs] It\'s time for The News Assessment Game! Earn up to $4 in less than 15 minutes.'

#message_text_3_1 = 'It\'s time for The News Assessment Game! Earn up to $4 in less than 15 minutes.\n\nWe have limited space, so click the link early to reserve your spot!\n\nClick the link to play:\n\n'
#message_text_3_2 = '\n\nThe game takes 12-15 minutes including wait time.  You get $2 for participating, and up to $2 extra for correct answers. All payments will be submitted via bonus to your Kellogg eLab enrollment HIT.\n\n˗ˏˋ HOW IT WORKS ˊˎ˗‏\n\nThe game starts at exactly 4:00pm ET (1:00pm PT)\n\nClick the link above to enter.\n\nThis link will *close* at exactly 4:00pm ET (1:00pm PT). You must enter before 4:00pm ET (1:00pm PT) to participate.\n\nIf you arrive early, you\'ll be shown a countdown to start time.\n\nAfter the link closes at 4:00pm ET (1:00pm PT), there will be up to 1 minute additional wait time to ensure everyone is synchronized.\n\nThe game itself takes less than 15 minutes.'


# ESTIMATION CHALLENGE
GAME_TIME = '4:00pm CT. (5:00pm ET.)'

message_subject_3 = '[Estimation Challenge] Play now! Earn up to $3 in less than 10 minutes.'

message_text_3_1 = 'LIVE NOW:  Play The Estimation Challenge! Earn up to $3 in less than 10 minutes.\n\nGive your best guess to a factual question.. that\'s it! You’ll have 5 minutes to discuss the question with other participants. The task takes 6 1/2 minutes total.\n\nPLEASE NOTE: Because we need to group people into discussions, we cannot guarantee everyone a spot.\n\nIf you are assigned to a discussion group, you get $1 for participating, and up to $2 extra for correct answers. (That\'s $8-24/hour depending on accuracy and wait time.) All payments will be submitted via bonus to your Kellogg eLab enrollment HIT.\n\nClick the link to play:\n\n'
message_text_3_2 = '\n\n˗ˏˋ HOW IT WORKS ˊˎ˗‏\nThe game starts at exactly ' + GAME_TIME + ' That’s in less than 15 minutes!\n\nClick the link above to enter.\n\nThis link will *close* at game time.  You must enter before game time to participate.\n\nIf you arrive early, you\'ll be shown a countdown to start time.\n\nAfter the link closes, there will be up to 1 minute additional wait time to ensure everyone is synchronized.\n\nThe game itself takes 6 1/2 minutes.'


# Client
client = boto3.client(service_name = 'mturk', region_name='us-east-1')



def hash(worker_id, password):
	hash_out = 0

	combined_string = worker_id + password

	for i in combined_string:
		#print(i)
		char_utf_8 = ord(i)
		hash_out = hash_out
		#print("old hash" + format(hash_out))
		#print("bit adjust" + format(np.int32(hash_out)))
		hash_out = ((np.int32(hash_out) << 5) - hash_out) + char_utf_8       
		hash_out = np.int32(hash_out)
		#print("new hash:" + format(hash_out))
	return abs(hash_out)



def message(worker_id, link):

	mt = message_text_3_1 + link + message_text_3_2

	w_id = [worker_id]

	try:
		client.notify_workers(
			Subject = message_subject_3,
			MessageText = mt,
			WorkerIds = w_id
		)
	
	except:
		print('Worker ' + worker_id + ' threw an error!')

	#time.sleep(0.25)



def main():

	s = pd.read_csv('sample_11802E_051619_5.csv', header = 0)
	ids = s.loc[:,'MID']
	workers = ids.tolist()

	for w_id in tqdm.tqdm(workers):

		l1 = 'http://estimation-challenge.meteorapp.com/?MID='

		l2 = '&passkey='

		h = hash(w_id, PASSWORD)

		link = l1 + w_id + l2 + str(h)

		message(w_id, link)



main()

## RECORD SENT OBJECT 
## MTurkR PACKAGE AS TEMPORARY 