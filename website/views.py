# this stores URL endpoints for the front-end of website
# anything that the user can navigate to, will be handled here (excpet anything related to authentication)

from flask import Blueprint, render_template
views = Blueprint('views', __name__)

# @name.rout(only slash here bc in home directory)
# function below decorator will only run whenever we are in URL defined by decorator


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/price_module')
def price_module():
    return render_template('price_module.html')


@views.route('/logout')
def logout():
    return render_template('logout.html')
