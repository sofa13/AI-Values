import tweepy
import sys
import os
import json
from pprint import pprint

import datetime

class TwitterAPI:
	def __init__(self):
		
		API_KEY = "mtdKUrsxqirqxKeQ3RUquKkEu"
		API_SECRET = "EwA3tSNfe3eEhNw7HE4Yn2uZtp7osmiarUH8c51JVgy8O9KqNA"
		
		auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
		self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		self.date = "2019-09-02"

		if (not self.api):
			print ("Can't Authenticate")
			sys.exit(-1)
	
	def getFollowings(self, username, date=None, folder="followings"):
		if date is None: date = self.date
		
		# create file name
		fname = os.path.join(folder, username)
		if date is None: date = datetime.datetime.now().strftime("%Y-%m-%d")
		fname = '-'.join([fname,date]) 
		print(fname)
		
		# check if file exists
		if os.path.isfile(fname):
			print("file exists")
			with open(fname, 'r', encoding="utf-8") as fin:
				friends = eval(fin.read())
			
			return friends
			
		# get user followings
		friends = [user.screen_name for user in tweepy.Cursor(self.api.friends, screen_name=username).items()]
		
		# write file
		with open(fname, 'w', encoding="utf-8") as fout:
			pprint(friends, fout)
			
		return friends
		
	def getAccountsUrls(self, username, accounts, date=None, folder="accounturls"):
		if date is None: date = self.date
		
		# create file name
		fname = os.path.join(folder, username)
		if date is None: date = datetime.datetime.now().strftime("%Y-%m-%d")
		fname = '-'.join([fname,date]) 
		print(fname)
		
		# check if file exists
		if os.path.isfile(fname):
			print("file exists")
			with open(fname, 'r', encoding="utf-8") as fin:
				acc_to_urls = eval(fin.read())
			
			return acc_to_urls
	
		acc_to_urls = dict()
		for acc in accounts:
			acc_to_urls[acc] = self.getAccountUrls(acc)
			
		# write file
		with open(fname, 'w', encoding="utf-8") as fout:
			pprint(acc_to_urls, fout)
			
		return acc_to_urls
			
	def getAccountUrls(self, acc, folder="twitterids"):
		searchQuery = ''.join(['from:', acc, ' filter:links'])
		print("searchQuery:",searchQuery)
		
		maxTweets = 500000000 # Some arbitrary large number
		tweetsPerQry = 100 # this is the max the API permits

		sinceId = None

		max_id = 0
		tweetCount = 0
		count=0
		print("Downloading max {0} tweets".format(maxTweets))
		
		acc_to_text = set()
		while tweetCount < maxTweets:
			new_tweets = []
			try:
				if (max_id <= 0):
					if (not sinceId):
						new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry)
					else:
						new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry,
												since_id=sinceId)
				else:
					if (not sinceId):
						new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry,
												max_id=str(max_id - 1))
					else:
						new_tweets = self.api.search(q=searchQuery, count=tweetsPerQry,
												max_id=str(max_id - 1),
												since_id=sinceId)
				if not new_tweets:
					print("No more tweets found")
					break
				for tweet in new_tweets:
					
					id_str = tweet._json["id_str"]
					acc_to_text.add(id_str)
				
				tweetCount += len(new_tweets)
				print("Downloaded {0} tweets".format(tweetCount))
				max_id = new_tweets[-1].id
				count=count+1
				if (count%35==0): time.sleep(60*15)
				print(max_id)
			
			except tweepy.TweepError as e:
				# Just exit if any error
				print("some error : " + str(e))
				break

		return acc_to_text
	
	def processUrls(user, ids):
		
		# call multiprocess to get twitter urls and fetch expanded url
		
		# should I grab the final url to process the domains?
		
		# should I grab the tweet ID and save it as a file with the extended_url
		
		pass
	
	def getUrlTitle(self, url):
		# follow url
		pass
		
if __name__ == '__main__':
	tapi = TwitterAPI()
	
	user = "lfountain6655"
	accs = tapi.getFollowings(user)
	ids = tapi.getAccountsUrls(user, accs)
	pprint(ids)
	
	# create list of ids to crawl and process
	