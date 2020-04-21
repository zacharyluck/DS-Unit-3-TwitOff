# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.old_models import Tweet, User, db


data_routes = Blueprint("data_routes", __name__)

@data_routes.route("/newtweet")
def new_tweet():
    # show the tweet creation page
    # pass given data onto newtweet/create
    userlist = User.query.all()
    test_list = []
    for user in userlist:
        test = {}
        test['userid'] = user.userid
        test['username'] = user.username
        test_list.append(test)

    print(test_list)

    return render_template(
        "new_tweet.html", userlist=userlist
    )

@data_routes.route("/newtweet/create", methods=["POST"])
def create_tweet():
    # TODO: get data from user
    userdata = dict(request.form)

    # see how it's formed
    print("FORM DATA:", userdata)

    # save it in database
    userinput = Tweet(
        tweetid=(len(Tweet.query.all()) + 1), # should make incrementing ids
        tweet=userdata['tweet'],
        userid=userdata['userid']
    )
    db.session.add(userinput)
    db.session.commit()

    flash(f"Tweet '{userdata['tweet']}' added successfully!", "success")
    return redirect("/")

@data_routes.route('/newuser')
def new_user():
    # show user creation page
    # pass given data onto newuser/create
    return render_template('new_user.html')

@data_routes.route("/newuser/create", methods=["POST"])
def create_user():
    # TODO: get data from user
    userdata = dict(request.form)

    # see how it's formed
    print("FORM DATA:", userdata)

    # save it in database
    userinput = User(
        userid=(len(User.query.all()) + 1), # should make incrementing ids
        username=userdata['username']
    )
    db.session.add(userinput)
    db.session.commit()

    flash(f"User '{userdata['username']}' added successfully!", "success")
    return redirect("/")