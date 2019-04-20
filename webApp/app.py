# Run with command [FLASK_APP=app.py FLASK_DEBUG=1 flask run]
# Will reload on save

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

#routing for the main page
@app.route('/')
def main():
    return render_template('pages/main.html')

#routing for the login page
@app.route('/login')
def login():
    return render_template('pages/login.html')

#check the login request
@app.route('/login', methods=["POST"])
def validateLogin():
    #redirect as post
    return redirect(url_for('dashboard'), code=307)

#routing for the dashboard
@app.route('/dashboard', methods=["POST"])
def dashboard():
    return render_template('pages/dashboard.html')

@app.route('/assignment', methods=["POST"])
def assignment():
    return render_template('pages/assignment.html')

@app.route('/signout', methods=["POST"])
def signOut():
    #redirect as post
    return redirect('/')
