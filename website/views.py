from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Transaction
from . import db
import json

# Current price per gallon = $1.50 (this is the price what distributor gets from refinery and it varies based upon crude price. But we are keeping it constant for simplicity)
# Margin =  Current Price * (Location Factor - Rate History Factor + Gallons Requested Factor + Company Profit Factor)
# Consider these factors:
# Location Factor = 2% for Texas, 4% for out of state.
# Rate History Factor = 1% if client requested fuel before, 0% if no history (you can query fuel quote table to check if there are any rows for the client)
# Gallons Requested Factor = 2% if more than 1000 Gallons, 3% if less
# Company Profit Factor = 10% always
# Example:
# 1500 gallons requested, in state, does have history (i.e. quote history data exist in DB for this client)
# Margin => (.02 - .01 + .02 + .1) * 1.50 = .195
# Suggested Price/gallon => 1.50 + .195 = $1.695
# Total Amount Due => 1500 * 1.695 = $2542.50
# Additional Validations:
# • Make suggested price and total amount fields in your Quote form read-only, i.e. user cannot enter these values.
# • Create another button on Quote Form before Submit, call it "Get Quote".
# • After user enters all other fields in the form other than Suggested Price and Total Amount, allow user to click on "Get Quote", i.e. Get Quote and Submit Quote buttons should be disabled if there are no values entered in the form. 
# • When user clicks on "Get Quote" button make a call to Pricing Module and populate the suggested price and total. 
# • Display Suggested Price and Total Amount once you get the values from pricing module. 
# • Make sure you do not lose any form values when you make a call to Pricing module.
# • You can use AJAX call to achieve this i.e.  partial form submission. 
# • Then user clicks on Submit Quote and you save the quote.


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("home.html", user=current_user)



@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profileMgmnt():
    if request.method == 'POST':
        #email = current_user.email
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
        
        # print(current_user.email)
        # print(current_user.fullName)
        # print(current_user.address1)
        # print(current_user.address2)
        # print(current_user.city)
        # print(current_user.state)
        # print(current_user.zipcode)



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
            if(gallons <= 0):
                flash("Please enter a valid numerical value for gallons requested", category="error")
            if(delivery_date == ""):
                flash("Please enter a date for delivery", category="error")
            else:
                base_per_gallon = 1.5
                # Location Factor = 2% for Texas, 4% for out of state.
                tex = 0.02
                not_tex = 0.04
                tex_factor = 0
                if(current_user.state == "TX"):
                    tex_factor = tex
                if(current_user.state != "TX"):
                    tex_factor = not_tex
                #print("tex_factor: ", tex_factor)
                # Rate History Factor = 1% if client requested fuel before, 0% if no history
                hist = 0.01
                no_hist = 0
                hist_factor = 0
                if(len(current_user.transactions) == 0):
                    hist_factor = no_hist
                if(len(current_user.transactions) > 0):
                    hist_factor = hist

                # Gallons Requested Factor = 2% if more than 1000 Gallons, 3% if less
                gallon_over = 0.02
                gallon_under = 0.03
                gallon_factor = 0
                if(gallons >= 1000):
                    gallon_factor = gallon_over
                if(gallons < 1000):
                    gallon_factor = gallon_under

                # Company Profit Factor = 10% always
                profit = 0.1
                # Margin =  Current Price * (Location Factor - Rate History Factor + Gallons Requested Factor + Company Profit Factor)
                margin = base_per_gallon*((tex_factor - hist_factor) + (gallon_factor + profit))
                # Suggested Price/gallon => 1.50 + .195 = $1.695
                # Total Amount Due => 1500 * 1.695 = $2542.50
                price = base_per_gallon + margin
                total = gallons * price
                # print(base_per_gallon, '+', margin)
                # print(gallons,'*',price)

                newTransaction = Transaction(gallons=gallons,total=total, delivery_date=delivery_date, user_id=current_user.id)
                db.session.add(newTransaction) 
                db.session.commit()

                # printing these values to terminal for debugging purposes
                # print(gallons)
                # print(address)
                # print(type(delivery_date))
                # print(delivery_date)
        except:
            flash("Please enter a numeric value for gallons requested", category="error")

    return render_template("price_module.html", user=current_user)



@views.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    return render_template("history.html", user=current_user)

