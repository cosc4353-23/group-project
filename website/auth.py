# stores anything related to authentication --> login, logout, sign-up
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

auth = Blueprint('auth', __name__)

# functions will only run whenever we are in URL defined by decorator


@auth.route('/login')
def login():
    return render_template('login.html', user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    return render_template('sign_up.html', user=current_user)
