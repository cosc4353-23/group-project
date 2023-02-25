# this stores URL endpoints for the front-end of website
# anything that the user can navigate to, will be handled here (excpet anything related to authentication)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
views = Blueprint('views', __name__)

# @name.rout(only slash here bc in home directory)
# function below decorator will only run whenever we are in URL defined by decorator


@views.route('/')
def home():
    return render_template('home.html', isIndex=True)


@views.route('/profile')
def profile():
    return render_template('profile.html', isIndex=True)


@views.route('/price_module')
def price_module():
    return render_template('price_module.html', isIndex=True)


@views.route('/logout')
def logout():
    return redirect(url_for('auth.login'))
