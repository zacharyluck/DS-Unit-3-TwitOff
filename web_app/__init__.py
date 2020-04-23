# from flask import Flask

# app = Flask(__name__)

# # handle requests to the home page
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# @app.route('/about')
# def about():
#     x = 2 + 2
#     return f'About Me {x}'

# web_app/__init__.py

from flask import Flask
import os
from dotenv import load_dotenv

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.data_routes import data_routes
from web_app.routes.twitter_routes import twitter_routes
from web_app.routes.admin_routes import admin_routes
from web_app.routes.stats_routes import stats_routes

load_dotenv()

def create_app():
    app = Flask(__name__)

    # TODO: fix this
    URI = os.getenv('DATABASE_URI')
    app.config["SQLALCHEMY_DATABASE_URI"] = URI
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    print('URI:',URI)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(data_routes)
    app.register_blueprint(twitter_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(stats_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)