'''
flask-tweepy-oauth
an example showing how to authorize a twitter application
in python with flask and tweepy.
find me on github at github.com/whichlight
see my other projects at whichlight.com
KAWAN!
'''

# 3rd Party Modules
from flask import Flask, render_template, request

# Local Modules
from string_analyzer import StringAnalyser
from twitter_client import TwitterClient

app = Flask(__name__)

# Global Variables
string_analyzer = StringAnalyser()
twitter_client = TwitterClient()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html', name='test')

@app.route("/submit_username", methods=['POST'])
def submit_username():
    if not request.form.get('username', None):
        # There was no username passed
        return render_template('error.html')

    username = request.form['username']
    tones = twitter_client.analyzer_user(username)

    if not tones:
        # The user had no tweets
        return render_template('error.html')

    return render_template('twitter_analysis.html', tones=tones)





if __name__ == "__main__":
    app.run()