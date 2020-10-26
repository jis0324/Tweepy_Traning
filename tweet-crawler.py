import os
import json
import tweepy
import datetime
import xlsxwriter

base_dir = os.path.dirname(os.path.abspath(__file__))
secrets = json.loads(open(base_dir + '/secrets.json').read())
# credentials from https://apps.twitter.com/
consumerKey = secrets['api_key']
consumerSecret = secrets['api_secret_key']
accessToken = secrets['access_token']
accessTokenSecret = secrets['access_token_secret']

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

username = "FoxNews"
startDate = datetime.datetime(2019, 9, 1, 0, 0, 0)
endDate = datetime.datetime(2020, 10, 25, 0, 0, 0)
print("Finding Tweets of {} From {} To {}...".format(username, str(startDate), str(endDate)))

tweets = []
tmpTweets = api.user_timeline(username)
for tweet in tmpTweets:
    if tweet.created_at < endDate and tweet.created_at > startDate:
        tweets.append(tweet)

while (tmpTweets[-1].created_at > startDate):
    if tmpTweets[-1].created_at < endDate and tmpTweets[-1].created_at > startDate:
        print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")

    tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)

workbook = xlsxwriter.Workbook(username + ".xlsx")
worksheet = workbook.add_worksheet()

worksheet.write_string(0, 0, "favorite_count")
worksheet.write_string(0, 1, "source")
worksheet.write_string(0, 2, "text")
worksheet.write_string(0, 3, "in_reply_to_status_id")
worksheet.write_string(0, 4, "tweet.retweeted")
worksheet.write_string(0, 5, "tweet.created_at")
worksheet.write_string(0, 6, "tweet.retweet_count")
worksheet.write_string(0, 7, "id")

row = 1
for tweet in tweets:
    worksheet.write_string(row, 0, str(tweet.favorite_count))
    worksheet.write_string(row, 1, str(tweet.source))
    worksheet.write(row, 2, tweet.text)
    worksheet.write_string(row, 3, str(tweet.in_reply_to_status_id))
    worksheet.write_string(row, 4, str(tweet.retweeted))
    worksheet.write_string(row, 5, str(tweet.created_at))
    worksheet.write_string(row, 6, str(tweet.retweet_count))
    worksheet.write_string(row, 7, str(tweet.id))
    row += 1

workbook.close()
print("Excel file ready")
