import tweepy
import sys
import os
import json



API_KEY = "mtdKUrsxqirqxKeQ3RUquKkEu"
API_SECRET = "EwA3tSNfe3eEhNw7HE4Yn2uZtp7osmiarUH8c51JVgy8O9KqNA"


auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth)#, wait_on_rate_limit=True,
				   #wait_on_rate_limit_notify=True)
print("Emad")
if (not api):
	print ("Can't Authenticate")
	sys.exit(-1)


#searchQuery = 'http'  # this is what we're searching for
searchQuery = 'Predictim'	# this is what we're searching for
maxTweets = 500000000 # Some arbitrary large number
tweetsPerQry = 100	 # this is the max the API permits
fName = 'SearchTwitterTest.csv' # We'll store the tweets in a text file.


sinceId = None

for user in tweepy.Cursor(api.friends, screen_name="kebouskill").items():
    print('friend: ' + user.screen_name)

# max_id = 0
# #953813743154147329
# tweetCount = 0
# count=0
# print("Downloading max {0} tweets".format(maxTweets))
# with open(fName, 'w',encoding="utf-8") as f:
	# while tweetCount < maxTweets:
		# new_tweets = []
		# try:
			# if (max_id <= 0):
				# if (not sinceId):
					# new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
					# #new_tweets = api.search_users(q=searchQuery)
				# else:
					# new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
											# since_id=sinceId)
			# else:
				# if (not sinceId):
					# new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
											# max_id=str(max_id - 1))
				# else:
					# new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
											# max_id=str(max_id - 1),
											# since_id=sinceId)
			# if not new_tweets:
				# print("No more tweets found")
				# break
			# for tweet in new_tweets:
				# f.write("[")
				# #print(tweet._json["text"])
				# json.dump(tweet._json,f)#f.write(tweet._json["text"].strip("\n").encode("utf-8") +'\n')
				# f.write("],\n")
			# tweetCount += len(new_tweets)
			# print("Downloaded {0} tweets".format(tweetCount))
			# max_id = new_tweets[-1].id
			# count=count+1
			# if (count%35==0): time.sleep(60*15)
			# print(max_id)
		# except tweepy.TweepError as e:
			# # Just exit if any error
			# print("some error : " + str(e))
			# break
		# f.flush()
		# os.fsync(f.fileno())				
# print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
