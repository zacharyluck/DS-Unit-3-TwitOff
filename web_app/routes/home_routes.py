# web_app/routes/home_routes.py

from flask import Blueprint, jsonify, request, render_template
from web_app.models import Tweet, User


home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    # get tweet and user data from sql,
    # put it into a list and return it as tweets
    users = User.query.all()
    userlist = []
    for user in users:
        userlist.append(user.name)

    print(userlist)

    # this should return it as a list of dicts
    # which will then be displayed by the
    # homepage correctly
    return render_template('index.html',userlist=users)

@home_routes.route("/about")
def about():
    return "Cause it feels so empty without me."