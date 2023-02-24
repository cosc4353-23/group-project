# stores anything related to authentication --> login, logout, sign-up
from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

# functions will only run whenever we are in URL defined by decorator


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<h1>You Have Logged Out</h1>"


@auth.route('/sign-up')
def signUp():
    return render_template('sign_up.html')
