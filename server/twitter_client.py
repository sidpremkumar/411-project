# Built In Modules
import os
import re

# 3rd Party Modules
from tweepy import OAuthHandler
import tweepy

# Local Modules
from string_analyzer import StringAnalyser

class TwitterClient(object):
    """
    Twitter client used to interact with a users tweets and do analysis
    """

    def __init__(self):
        """Constructor"""
        self.consumer_key = os.environ['CONSUMER_KEY']
        self.consumer_secret = os.environ['CONSUMER_SECRET']
        self.access_token = os.environ['ACCESS_TOKEN']
        self.access_token_secret = os.environ['ACCESS_SECRET']
        # attempt authentication
        try:
            # create OAuthHandler, tweepy object and connect to Twitter
            self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
        # Create instance of our string analyser
        self.analyser = StringAnalyser()

    def strip_tweet(self, tweet):
        """
        Helper function to clean tweets.

        :param String tweet: Tweet to clean
        :return: Cleaned tweet
        :rtype: String
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyzer_user(self, username):
        """
        Helper function to get analyzer user.

        :param String username: Username to query for
        :return: List of users tweets cleaned
        :rtype: List
        """
        final_string = ""
        for tweet in self.api.user_timeline(username, count=5000):
            cleaned_tweet = self.strip_tweet(tweet.text)
            final_string += cleaned_tweet + "."

        if not final_string:
            return None
        # Analyze our tweets
        tones = self.analyser.string_analysis(final_string)

        return tones


if __name__ == '__main__':
    # Main method for debugging only
    client = TwitterClient()
    client.analyzer_user('AlliDoisQuinnn')