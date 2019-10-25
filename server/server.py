'''
flask-tweepy-oauth
an example showing how to authorize a twitter application
in python with flask and tweepy.
find me on github at github.com/whichlight
see my other projects at whichlight.com
KAWAN!
'''
# Local Modules
import os

# 3rd Party Modules
from flask import Flask, render_template, request
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

# Local Modules
from string_analyzer import StringAnalyser
from twitter_client import TwitterClient


# Global Variables
string_analyzer = StringAnalyser()
twitter_client = TwitterClient()
# Create our flask object
app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_twitter_blueprint(
    api_key=os.environ['CONSUMER_KEY'],
    api_secret=os.environ['CONSUMER_SECRET'],
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/", methods=['GET'])
def index():
    # Function for our homepage
    # Check if our user is authorized already
    if not twitter.authorized:
        # TODO: Maybe do something else if we're already authorized
        pass

    return render_template('index.html')


@app.route("/get_twitter_data", methods=['GET'])
def get_twitter_data():
    """Function to authenticate and analyze a twitter user"""
    # Check if our user is authorized already
    if not twitter.authorized:
        # TODO: Redirect a user to another page here
        return 400
    response = twitter.get("statuses/home_timeline.json", params={'count': '200'})
    if response.status_code != 200:
        # TODO: Something went wrong
        return 400

    # Loop over the results building a long string with all tweets from their timeline
    results = response.json()
    final_string = ""
    for result in results:
        final_string += result['text'] + " ."

    # Analyzer our final string and display the info to the user
    tones = string_analyzer.string_analysis(final_string)

    return render_template('twitter_analysis.html', tones=tones)





if __name__ == "__main__":
    app.run()