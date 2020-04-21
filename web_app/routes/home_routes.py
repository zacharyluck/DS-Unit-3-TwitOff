# web_app/routes/home_routes.py

from flask import Blueprint, jsonify, request, render_template
from web_app.old_models import Tweet, User


home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    # get tweet and user data from sql,
    # put it into a list and return it as tweets
    tweets = Tweet.query.all()

    tweetlist = []
    for tweet in tweets:
        tweetpak = {}
        tweetpak['tweet'] = tweet.tweet
        tweetpak['username'] = User.query.filter_by(userid=tweet.userid).first().username
        tweetlist.append(tweetpak)

    print(tweetlist)

    # this should return it as a list of dicts
    # which will then be displayed by the
    # homepage correctly
    return render_template('index.html',tweetlist=tweetlist)

@home_routes.route("/about")
def about():
    return "Cause it feels so empty without me."