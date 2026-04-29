import pandas as pd  # Importing pandas library for data manipulation (if needed later)
import joblib  # Importing joblib for loading machine learning models
import os  # Importing os to handle file paths and directories
from datetime import datetime  # Importing datetime to work with timestamps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify  # Importing Flask core components
from flask_sqlalchemy import SQLAlchemy  # Importing SQLAlchemy for database management
from werkzeug.security import generate_password_hash, check_password_hash  # Importing security tools for password hashing

app = Flask(__name__)  # Initializing the Flask application
app.secret_key = 'super_secret_key_for_session'  # Setting a secret key for session management and flash messages

# --- DATABASE CONFIGURATION ---
# We define the path for the database inside the 'instance' folder as requested.
# Flask automatically handles the 'instance' folder path for SQLite databases.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Setting the SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabling modification tracking to save resources

db = SQLAlchemy(app)  # Initializing the SQLAlchemy database object connected to our app

# --- USER MODEL ---
# This class defines the structure of the 'User' table in our database.
class User(db.Model):  # Creating a User class that inherits from db.Model
    id = db.Column(db.Integer, primary_key=True)  # Defining a unique ID for each user (Primary Key)
    first_name = db.Column(db.String(50), nullable=False)  # Defining a column for First Name (Required)
    last_name = db.Column(db.String(50), nullable=False)  # Defining a column for Last Name (Required)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Defining a column for Email (Must be unique and required)
    password_hash = db.Column(db.String(200), nullable=False)  # Defining a column to store the SECURELY HASHED password

# --- INITIALIZE DATABASE ---
# This block ensures that the 'instance' folder and database file are created on startup.
with app.app_context():  # Creating an application context to interact with the database
    db.create_all()  # Creating all tables defined as models (like the User table) if they don't exist


@app.route('/')  # Defining the route for the Home page
def home():  # Function to handle Home page requests
    return render_template('home.html')  # Rendering the 'home.html' template

@app.route('/about')  # Defining the route for the About page
def about():  # Function to handle About page requests
    return render_template('about.html')  # Rendering the 'about.html' template

@app.route('/dashboard')  # Defining the route for the Dashboard page
def dashboard():  # Function to handle Dashboard requests
    return render_template('dashboard.html')  # Rendering the 'dashboard.html' template if logged in

@app.route('/model')  # Defining the route for the Model page
def model():  # Function to handle Model requests
    return render_template('model.html')  # Rendering the 'model.html' template

@app.route('/data_drift')  # Defining the route for the Data Drift page
def data_drift():  # Function to handle Data Drift requests
    return render_template('data_drift.html')  # Rendering the 'data_drift.html' template

@app.route('/sign_up', methods=['GET', 'POST'])  # Defining the route for Sign Up (supports both GET and POST)
def sign_up():  # Function to handle Sign Up requests
    if request.method == 'POST':  # Checking if the user submitted the form (POST request)
        # Extracting data from the form fields
        first_name = request.form.get('first_name')  # Getting the first name from the input field
        last_name = request.form.get('last_name')  # Getting the last name from the input field
        email = request.form.get('email')  # Getting the email from the input field
        password = request.form.get('password')  # Getting the password from the input field

        # Checking if a user with this email already exists in the database
        user_exists = User.query.filter_by(email=email).first()  # Querying the User table for the email
        if user_exists:  # If a user is found
            flash('Email address already exists!')  # Flashing an error message
            return redirect(url_for('sign_up'))  # Redirecting back to the sign-up page

        # Creating a new User object with hashed password
        new_user = User(
            first_name=first_name,  # Setting first name
            last_name=last_name,  # Setting last name
            email=email,  # Setting email
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')  # Hashing the password for security
        )

        db.session.add(new_user)  # Adding the new user to the database session
        db.session.commit()  # Committing the changes to save the user to the database file

        flash('Account created successfully! Please sign in.')  # Flashing a success message
        return redirect(url_for('sign_in'))  # Redirecting to the sign-in page

    return render_template('sign_up.html')  # Rendering the 'sign_up.html' template for GET requests

@app.route('/sign_in', methods=['GET', 'POST'])  # Defining the route for Sign In (supports both GET and POST)
def sign_in():  # Function to handle Sign In requests
    if request.method == 'POST':  # Checking if the form was submitted (POST request)
        email = request.form.get('email')  # Getting the email from the sign-in form
        password = request.form.get('password')  # Getting the password from the sign-in form

        user = User.query.filter_by(email=email).first()  # Searching for the user in the database by email

        # Verifying user existence and checking if the password matches the hash
        if user and check_password_hash(user.password_hash, password):  # If user exists and password is correct
            session['user_id'] = user.id  # Storing user ID in the session
            session['user_name'] = user.first_name  # Storing user's first name in the session for display
            flash(f'Welcome back, {user.first_name}!')  # Flashing a welcome message
            return redirect(url_for('dashboard'))  # Redirecting to the user dashboard
        else:  # If login fails
            flash('Login failed. Please check your email and password.')  # Flashing an error message

    return render_template('sign_in.html')  # Rendering the 'sign_in.html' template for GET requests

@app.route('/logout')  # Defining the route for Logging Out
def logout():  # Function to handle Logout requests
    session.pop('user_id', None)  # Removing user ID from the session
    session.pop('user_name', None)  # Removing user name from the session
    flash('You have been logged out.')  # Flashing a logout confirmation message
    return redirect(url_for('home'))  # Redirecting back to the home page

@app.route('/view_users')  # Defining a temporary route to see all registered users in the database
def view_users():  # Function to display all users
    users = User.query.all()  # Fetching all records from the User table
    # Returning the data as JSON so you can see 'everything in the DB file' easily
    return jsonify([{ 'id': u.id, 'name': f"{u.first_name} {u.last_name}", 'email': u.email } for u in users])

if __name__ == "__main__":
    app.run(debug=True)

