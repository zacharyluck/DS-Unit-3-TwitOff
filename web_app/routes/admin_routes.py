# web_app/routes/admin_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client

from web_app.models import db, User, Tweet, parse_records

admin_routes = Blueprint("admin_routes", __name__)

API_KEY = 'abc123'  # TODO: grab this from env or html request

@admin_routes.route('/admin')
def admin_index():
    return render_template('admin.html')

@admin_routes.route("/admin/db/reset")
def reset_db():
    if API_KEY == 'abc123': 
        print(type(db))
        db.drop_all()
        db.create_all()
        return jsonify({"message": "DB RESET OK"})
    else:
        flash("Permission Denied", 'danger')
        return redirect('/')

@admin_routes.route("/admin/db/seed")
def seed_db():
    print(type(db))
    api = twitter_api_client()

    for screen_name in ['elonmusk','justinbieber','s2t2']:
        twitter_user = api.get_user(screen_name)
        statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
        print("STATUSES COUNT:", len(statuses))
        
        # get existing user from the db or initialize a new one:
        db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
        db_user.screen_name = twitter_user.screen_name
        db_user.name = twitter_user.name
        db_user.location = twitter_user.location
        db_user.followers_count = twitter_user.followers_count
        db.session.add(db_user)
        db.session.commit()

        basilica_api = basilica_api_client()

        all_tweet_texts = [status.full_text for status in statuses]
        embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
        print("NUMBER OF EMBEDDINGS", len(embeddings))

        counter = 0
        for status in statuses:
            print(status.full_text)
            print("----")
            # get existing tweet from the db or initialize a new one:
            db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
            db_tweet.user_id = status.author.id # or db_user.id
            db_tweet.full_text = status.full_text
            embedding = embeddings[counter]
            print(len(embedding))
            db_tweet.embedding = embedding
            db.session.add(db_tweet)
            counter+=1
    db.session.commit()

    return jsonify({"message": "DB SEEDED OK"})