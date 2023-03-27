from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Transaction
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profileMgmnt():
    if request.method == 'POST':
        fullName = request.form.get('fullName')
        add1 = request.form.get('address1')
        add2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        #updating the database
        current_user.fullName = fullName
        current_user.address1 = add1
        current_user.address2 = add2
        current_user.city = city
        current_user.state = state
        current_user.zipcode = zipcode
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template("profile.html", user=current_user)

@views.route('/price_module', methods=['POST', 'GET'])
@login_required
def price_module():
    if request.method == 'POST': 
        gallons_text = request.form.get('gallons')
        delivery_date = request.form.get('date')
        #try/except block to ensure that you enter a numeric value for gallons
        try:
            gallons = int(gallons_text)
            if(delivery_date == ""):
                flash("Please enter a date for delivery", category="error")
            else:
                # in phase 4, the line below will look like
                # total = givePrice(gallons, state,...., other factors that may determine price)
                total = 5*gallons
                newTransaction = Transaction(gallons=gallons,total=total, delivery_date=delivery_date, user_id=current_user.id)
                db.session.add(newTransaction) 
                db.session.commit()
        except:
            flash("Please enter a numeric value for gallons requested", category="error")

    return render_template("price_module.html", user=current_user)

@views.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    return render_template("history.html", user=current_user)