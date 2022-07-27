from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager # manages all login processes
from flask_admin import Admin # for the admin section of app
from flask_admin.contrib.sqla import ModelView # view for admin section


db = SQLAlchemy() # initializing the database
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__) #initialize the app
    app.config['SECRET_KEY'] = 'Zweli' #this is a key that encrypts the cookies data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # database is stored at sqlite 3 ---> database name 
    db.init_app(app) # telling the database we are using this app to get and store data
    admin = Admin(app) # administrator of the app

     #registering the different views of the app
    from .views import views # importing views file
    from .auth import auth #importing auth file

    app.register_blueprint(views, url_prefix='/') #url_prefix defines how to access the views
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Dependents, Employment_status, Income, LoanAmount, LoanTerm, CreditScore, Documents
    admin.add_view(ModelView(User, db.session)) # adding the data from database to admin side
    admin.add_view(ModelView(Dependents, db.session))
    admin.add_view(ModelView(Employment_status, db.session))
    admin.add_view(ModelView(Income, db.session))
    admin.add_view(ModelView(LoanAmount, db.session))
    admin.add_view(ModelView(LoanTerm, db.session))
    admin.add_view(ModelView(CreditScore, db.session))
    admin.add_view(ModelView(Documents, db.session))

    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login' # if the user is not logged in, go to login page
    login_manager.init_app(app) # telling login manager which app we using

   
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # tells how we load a user, this looks for primary key entered
    
    return app


def create_database(app): # this function will check if the database already exists
    if not path.exists('Website/' + DB_NAME): # if theres no database, then create it
        db.create_all(app=app) # creates the whole database
        print('DATABASE CREATED SUCCESSFULLY!')

