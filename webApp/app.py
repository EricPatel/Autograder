# Run with command "python app.py"
# Will reload on save

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import os
import sys
sys.path.append('../')
from pythonSupport import grader

UPLOAD_FOLDER = r"C:\Users\shrey\Documents\Prin Prog\Final Project\AutograderApp\studentSubmissions"
ALLOWED_EXTENSIONS = set(['txt', 'py', 'c', 'java', 'hs'])


app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/AutoGrader"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('pages/assignment.html', status="")

    student_file = request.files['file']
    if student_file.filename == '':
        return render_template('pages/assignment.html', status="noFile")

    if student_file and allowed_file(student_file.filename):
        filename = secure_filename(student_file.filename)
        student_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mypath = os.path.join(os.path.dirname(__file__))
        mypath = mypath[0:len(mypath) - 7] + "\\studentSubmissions\\" + filename
        print(mypath, file=sys.stdout)
        score, total = grader.grade(mypath)
        return render_template('pages/assignment.html', status="uploaded", score=score, total=total)
    
        

#routing for the main page
@app.route('/')
def main():
    return render_template('pages/main.html')

#routing for the login page
@app.route('/login')
def login():
    return render_template('pages/login.html', error="")

#check the login request
@app.route('/login', methods=["POST"])
def validateLogin():
    #redirect as post
    user = mongo.db.User.find_one({'emailAddress' : request.form['email']})
    if user != None and user['password'] == request.form['password']:
        session['user'] = str(user['_id'])
        session['type'] = user['type']
        print(session)
        return redirect(url_for('dashboard'), code=307)
    return render_template('pages/login.html', error="error")

@app.route('/signup', methods=["POST"])
def createUser():
    print(request.form)
    type = 'student'
    if(len(request.form.getlist('type')) < 1):
        type = 'professor'
    error = mongo.db.User.insert_one({
        'name' : request.form['name'],
        'classes' : [],
        'type' : type,
        'emailAddress' : request.form['email'],
        'password' : request.form['password']
    })
    print(error)
    return redirect(url_for('login'))

#routing for the dashboard
@app.route('/dashboard', methods=["POST"])
def dashboard():
    if(session['type'] == 'student'):
        return render_template('pages/dashboard.html')
    else:
        return render_template('pages/dashboardP.html')

@app.route('/assignment', methods=["POST"])
def assignment():
    return render_template('pages/assignment.html')

@app.route('/signout', methods=["POST"])
def signOut():
    #redirect as post
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
