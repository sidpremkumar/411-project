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
from flask import Flask, render_template, redirect, request, url_for, session
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from pymongo import MongoClient

# Local Modules
from string_analyzer import StringAnalyser
from twitter_client import TwitterClient
from image_analysis import ImageAnalyser
from matcher import Matcher, LOCAL_DOG_IMAGES


# Global Variables
string_analyzer = StringAnalyser()
twitter_client = TwitterClient()
image_analyzer = ImageAnalyser()
matcher = Matcher()
# Create our flask object
app = Flask(__name__, static_url_path = "", static_folder = "templates/static")
app.secret_key = "supersekrit"
blueprint = make_twitter_blueprint(
    api_key=os.environ['CONSUMER_KEY'],
    api_secret=os.environ['CONSUMER_SECRET'],
)
app.register_blueprint(blueprint, url_prefix="/login")
# Create our database data
import pdb; pdb.set_trace()
client = MongoClient(f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}>@ds063160.mlab.com:63160/woof-are-you")
database = client.local
db_client = database.user_data
DATABASE_SCHEMA = {
    'username': None,
    'twitter_analysis': None,
    'image_analysis': None,
    'dog_match': None,
}


@app.route("/", methods=['GET'])
def index():
    """This is our front page"""
    # Function for our homepage
    # Check if our user is authorized already
    if twitter.authorized:
        return redirect('/homepage')

    return render_template('index.html')


@app.route("/login", methods=['GET'])
def login():
    """Function to authenticate and login a twitter user"""
    # Check if our user is authorized already
    if twitter.authorized:
        return redirect('/homepage')

    return redirect(url_for("twitter.login"))

@app.route("/logout", methods=['GET'])
def logout():
    """Function to logout a twitter user"""
    # Check if our user is authorized already
    if not twitter.authorized:
        return render_template('error.html')

    # Clear the session of the user
    session.clear()

    return render_template('index.html')


@app.route("/homepage", methods=['GET'])
def homepage():
    """This is the users homepage"""
    # Don't let them in if they are not authorized
    if not twitter.authorized:
        return render_template('error.html')

    # Get our users username
    query = twitter.get("account/settings.json")
    if not query.ok:
        return render_template('error.html', status_code=query.status_code)
    result = query.json()
    username = result["screen_name"]

    # Get our users data, if they don't have any data create it
    if db_client.find_one({"username": username}):
        # Update a users data
        try:
            data = db_client.find_one({"username": username})
        except:
            print(f"[DB]: Something went wrong when getting data for {username}")
            return render_template('error.html', status_code=487)

    else:
        # Create the user document
        try:
            data = DATABASE_SCHEMA
            data['username'] = username
            db_client.insert_one(data)
        except:
            print(f"[DB]: Something went wrong when updating {username}")
            return render_template('error.html', status_code=487)

    # Render our home screen with the username
    return render_template('user/homepage.html',
                           username=username,
                           data=data,
                           local_images=LOCAL_DOG_IMAGES)

@app.route("/match_user", methods=['GET'])
def match_user():
    """Function to match our user"""
    # Get our users username
    query = twitter.get("account/settings.json")
    if not query.ok:
        return render_template('error.html', status_code=query.status_code)
    result = query.json()
    username = result["screen_name"]

    # Get our users data, if they don't have any data create it
    if db_client.find_one({"username": username}):
        # Update a users data
        try:
            to_insert = db_client.find_one({"username": username})
            match_ret = matcher.match_data(to_insert)
            match_ret = (match_ret[0], int(match_ret[1]))
            to_insert['dog_match'] = match_ret
            db_client.update_one({'username': username}, {"$set": to_insert}, upsert=False)
        except:
            print(f"[DB]: Something went wrong when getting data for {username}")
            return render_template('error.html', status_code=487)

    else:
        print(f"[DB]: No data for {username}")
        return render_template('error.html', status_code=487)

    # If everything went well return the user the data
    return render_template('user/match.html', tones=to_insert['dog_match'])


@app.route("/get_twitter_data", methods=['GET'])
def get_twitter_data():
    """Function to authenticate and analyze a twitter user"""
    # Check if our user is authorized already
    if not twitter.authorized:
        return redirect('/homepage')

    # Query twitter for the users tweets and name
    response = twitter.get("statuses/home_timeline.json", params={'count': '200'})
    username = twitter.get("account/settings.json")
    if response.status_code != 200 or username.status_code != 200:
        return render_template('error.html', status_code=response.status_code)

    # Get our username
    username = username.json()['screen_name']

    # Loop over the results building a long string with all tweets from their timeline
    results = response.json()
    final_string = ""
    for result in results:
        final_string += result['text'] + " ."

    # Analyzer our final string and display the info to the user
    tones = string_analyzer.string_analysis(final_string)

    # Remove duplicates
    new_tones = []
    [new_tones.append(x) for x in tones if x not in new_tones]
    tones = new_tones

    # Add this data to our database
    if db_client.find_one({"username": username}):
        # Update a users data
        try:
            to_insert = db_client.find_one({"username": username})
            to_insert['twitter_analysis'] = tones
            db_client.update_one({'username': username}, {"$set": to_insert}, upsert=False)
        except:
            print(f"[DB]: Something went wrong when updating {username}")
            return render_template('user/twitter_analysis.html', tones=tones)

    else:
        # Create the user document
        try:
            to_insert = DATABASE_SCHEMA
            to_insert['username'] = username
            to_insert['twitter_analysis'] = tones
            db_client.insert_one(to_insert).inserted_id
        except:
            print(f"[DB]: Something went wrong when updating {username}")
            return render_template('user/twitter_analysis.html', tones=tones)

    # Return
    return render_template('user/twitter_analysis.html', tones=tones)


@app.route("/get_image_data", methods=['GET'])
def get_image_data():
    """Function to authenticate and analyze a image data"""
    # Check if our user is authorized already
    if not twitter.authorized:
        return redirect('/homepage')

    # Query twitter for the users username and display picture
    username = twitter.get("account/settings.json")
    if username.status_code != 200:
        return render_template('error.html', status_code=username.status_code)

    # Get our username
    username = username.json()['screen_name']

    response = twitter.get("users/show.json", params={'screen_name': username})
    if response.status_code != 200:
        return render_template('error.html', status_code=reponse.status_code)

    # Get our profile picture URL
    image_url = response.json()['profile_image_url']

    # Analyze it
    image_tones = image_analyzer.analyse(image_url)

    # Remove duplicates
    new_tones = []
    [new_tones.append(x) for x in image_tones if x not in new_tones]
    image_tones = new_tones

    # Add this data to our database
    if db_client.find_one({"username": username}):
        # Update a users data
        try:
            to_insert = db_client.find_one({"username": username})
            to_insert['image_analysis'] = image_tones
            db_client.update_one({'username': username}, {"$set": to_insert}, upsert=False)
        except:
            print(f"[DB]: Something went wrong when updating {username}")
            return render_template('error.html', status_code=487)

    else:
        # Create the user document
        try:
            to_insert = DATABASE_SCHEMA
            to_insert['username'] = username
            to_insert['image_analysis'] = image_tones
            db_client.insert_one(to_insert).inserted_id
        except:
            print(f"[DB]: Something went wrong when updating {username}")
            return render_template('error.html')

    # Return
    return render_template('user/image_analysis.html', tones=image_tones)


if __name__ == "__main__":
    app.run()
