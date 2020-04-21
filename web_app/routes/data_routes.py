# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
import os
import sqlite3


data_routes = Blueprint("data_routes", __name__)

@data_routes.route("/newtweet")
def new_book():
    # show the tweet creation page
    # pass given data onto newtweet/create
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data.sqlite3')
    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    query = '''
    SELECT
        userid
        ,username
    FROM userdata
    '''

    # get the usernames
    userlist = curs.execute(query).fetchall()
    print(userlist)
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
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data.sqlite3')
    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    query = f'''
    INSERT INTO tweetdata
    VALUES (
        (
            SELECT
                count(tweetid) + 1
            FROM tweetdata
        )
        ,"{userdata['tweet']}"
        ,{int(userdata['userid'])}
    )
    '''
    curs.execute(query)
    flash(f"Tweet '{userdata['tweet']}' added successfully!", "success")
    return redirect("/")