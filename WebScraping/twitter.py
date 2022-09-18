import time
import tweepy
import pandas as pd
import json
#import yaml
import pprint
import csv


class TwitterScraper:

    def __init__(self,hashtag = "#wine",n_tweets=10,path="/Users/andre/PycharmProjects/DM2583-project/"):
        self.hashtag = hashtag
        self.n_tweets = n_tweets
        with open(path+'credentials.csv', mode='r') as credentials_file:

            credentials_csv=csv.reader(credentials_file, delimiter=',')
            for tmp in credentials_csv:
                self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret = tmp
        self.connect()
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.twitter = tweepy.API(self.auth)


    def connect(self):
        return

    def download(self):

        tweets_df = pd.DataFrame()

        for tweet in tweepy.Cursor(self.twitter.search_tweets, q=self.hashtag, lang="en", ).items(self.n_tweets):
            # tw_row = save_tweet(tweet)
            t = {"source": tweet.source, "retweets": int(tweet.retweet_count), "Text": tweet.text,
                 "timestamp": tweet.created_at, "userlocation": tweet.user.location, }
            # print(tweet.user.)
            # tweet.user.description  user bio
            tweets_df = tweets_df.append(t, ignore_index=True)

        return tweets_df