# whatever is inside this will run automatically when we import this folder

from flask import Flask

# create app, initialize secret key, return the app


def createApp():
    app = Flask(__name__)
    # secret key for the app, doesnt matter what this is
    app.config['SECRET_KEY'] = 'abc123456789'

    # we have blueprints containing URL, here is where they are
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
