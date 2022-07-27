from typing import final
from unicodedata import category
from flask import Blueprint, flash, render_template, request, redirect, jsonify, url_for
from flask_login import login_required, current_user
from .models import CreditScore, Employment_status, Dependents, Income, LoanAmount, LoanTerm, Documents
from .import db
import json
import numpy as np
import pickle
import os
from werkzeug.utils import secure_filename
# blueprint allows u multiple views defined in the same application --->  many pages

views = Blueprint('views', __name__)
model = pickle.load(open('model.pkl', 'rb'))

@views.route('/', methods=['GET', 'POST'] ) # this is the route to get the home page "/"
@login_required
def home(): 
       
    return render_template("home.html", user=current_user) # returns the HTML for the home page


@views.route('/Apply', methods = ['GET','POST'])
@login_required
def predict():
    if request.method == 'POST':
        dependents = request.form.get('dependents') # getting the value from key ---> refers to the naming used in html form
        work_status = request.form.get('work_status')
        income = request.form.get('income')
        amount = request.form.get('amount')
        duration = request.form.get('duration')
        credit_score = request.form.get('credit_score')
 
        # taking form values to store in database
        user_dependents = Dependents(dependents=dependents, user_id = current_user.id)
        user_work_status = Employment_status(work_status=work_status, user_id = current_user.id)
        user_income = Income(income=income, user_id = current_user.id)
        user_amount = LoanAmount(amount=amount, user_id = current_user.id)
        user_duration = LoanTerm(duration=duration, user_id = current_user.id)
        user_credit = CreditScore(credit_score=credit_score, user_id = current_user.id)


        # adding the user values and updating the database
        db.session.add(user_dependents)
        db.session.commit()
        db.session.add(user_work_status)
        db.session.commit()
        db.session.add(user_income)
        db.session.commit()
        db.session.add(user_amount)
        db.session.commit()
        db.session.add(user_duration)
        db.session.commit()
        db.session.add(user_credit)
        db.session.commit()

        # converting the form values into integers for model interpretation
        dependents = int(dependents)
        work_status = int(work_status)
        income = int(income)
        amount = int(amount)
        duration = int(duration)
        credit_score = int(credit_score)



        attributes = [dependents, work_status, income, amount, duration, credit_score]
        final_list = [np.array(attributes)]
        prediction = model.predict(final_list)
        answer = prediction[0]
        return f'Answer: {answer}'

    return render_template("apply.html", user=current_user)


@views.route('/Upload', methods = ['GET','POST'])
@login_required
def upload():
    if request.method == 'POST':
        if request.files: # same like request.form but for files
            doc = request.files['document']
            filename = secure_filename(doc.filename)
            mimetype = doc.mimetype
            user_doc = Documents(document=doc.read(), name=filename, mimetype=mimetype, user_id = current_user.id)
            db.session.add(user_doc)
            db.session.commit()
            flash('File uploaded successfully', category='success')
            

            return redirect(request.url)

    return render_template('uploadFiles.html', user=current_user)    

