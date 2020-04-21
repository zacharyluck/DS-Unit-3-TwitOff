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

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.data_routes import data_routes

def create_app():
    app = Flask(__name__)

    # TODO: fix this
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:\\\\\\data.sqlite3"

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(data_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)