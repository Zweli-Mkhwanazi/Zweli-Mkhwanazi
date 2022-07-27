from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .import db
from werkzeug.security import generate_password_hash, check_password_hash # this is for hashing a password!
from flask_login import login_user, login_required, logout_user, current_user # to prevent unSigned user from accessing home page, if signed in hide login option etc...


auth = Blueprint('auth', __name__)

@auth.route('/Login', methods=['GET', 'POST']) # methods--> allows us to get HTML and input (change state)
def login() :
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # we are querying the database to check if a particular email exists
        if user: # if it exists then continue else the user does not have an Account
            if check_password_hash(user.password, password): # checking the password provided if it matches with the hashed password in the database
                flash('Login Successful', category='success')
                login_user(user, remember=True) # remembers that the user is logged in
                return redirect(url_for('views.home'))

            else: # if it does not
                flash('Login Failure', category='error')
                flash('Re-Enter password', category='error')
        else: 
            flash('Account does not exist', category='error')        


    return render_template("login.html", user=current_user)


@auth.route('/Log out')
@login_required # this ensures that a user must be logged in in order to get logut page
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/Sign-up', methods=['GET', 'POST'] )
def signup():
    if request.method == 'POST': # getting information from the form
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first() 
        if user:
            flash('Email addresss already exists!', category='error')

        # verifying if the data we got is correct (BASIC VERIFICATION)

        elif not firstName[0].isalpha():
            flash('Name should start with an alphabet', category='error')

        elif not lastName[0].isalpha():
            flash('Last Name should start with an alphabet', category='error')   

        

        elif len(email) < 5:
            flash('Email address must be greater than 5 characters', category='error')

        elif len(firstName) < 2:
            flash('First Name is too short', category='error')

        elif len(lastName) < 2:
            flash('Last Name is too short', category='error')    

        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')

        elif password1 != password2:
            flash('Password does not match', category='error')

        else:
            # create new user
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'),
            firstName=firstName, lastName=lastName)
            #sha256 is a hashing algorithm
            db.create_all() # links all the db objects from different file to point to one database object
            db.session.add(new_user) # adding new user to the database
            db.session.commit() # update the database
            flash('Account created succesfully')  
            login_user(new_user, remember=True) # remembers that the user is logged in
            return redirect(url_for('views.home')) # redirecting the user to the home page after sign-in 

    return render_template("signup.html", user=current_user)


