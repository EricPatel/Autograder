# Run with command "python app.py"
# Will reload on save

from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.utils import secure_filename
import os
import sys
import random
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
        user = mongo.db.User.find_one({'_id' : ObjectId(session['user'])})
        classIds = user['classes']
        classes = []
        for id in classIds:
            classes.append(mongo.db.Class.find_one({'_id' : id}))
        print(classes)
        return render_template('pages/dashboard.html', classes=classes)
    else:
        classes = mongo.db.Class.find({'professor' : ObjectId(session['user'])})
        return render_template('pages/dashboardProfessor.html', classes=classes)

@app.route('/assignment', methods=["POST"])
def assignment():
    classInfo = request.form['class']
    assignment = mongo.db.Assignment.find_one({'_id' : ObjectId(request.form['assignment'])})
    return render_template('pages/assignment.html', classInfo=classInfo, assignment=assignment)

@app.route('/class', methods=["POST"])
def classPage():
    classInfo = mongo.db.Class.find_one({'_id' : ObjectId(request.form['class'])})
    assignments = []
    for assignmentID in classInfo['assignments']:
        assignments.append(mongo.db.Assignment.find_one({'_id' : assignmentID}))
    if(session['type'] == 'student'):
        return render_template('pages/classStudent.html', classInfo=classInfo, assignments=assignments)
    else:
        return render_template('pages/class.html', classInfo=classInfo, assignments=assignments)

@app.route('/create', methods=["POST"])
def create():
    return render_template('pages/create.html')

@app.route('/createClass', methods=["POST"])
def createClass():
    id = session['user']
    code = str(id)[-3:]+ str(random.randint(100,1000))
    id = mongo.db.Class.insert_one({
        'name' : request.form['name'],
        'professor' : ObjectId(id),
        'students' : [],
        'assignments' : [],
        'classCode' : code
    }).inserted_id
    mongo.db.User.update({ '_id' : ObjectId(session['user'])}, { '$push' : { 'classes' : id}})
    return redirect(url_for('dashboard'), code=307)

@app.route('/createAssignment', methods=["POST"])
def createAssignmentRoute():
    return render_template('pages/createAssignment.html', id=request.form['class'])

@app.route('/createAssignmentSubmit', methods=["POST"])
def createAssignment():
    id = mongo.db.Assignment.insert_one({
        'name' : request.form['name'],
        'dueDate' : request.form['dueDate'],
        'language' : request.form['language'],
        'runCommand' : request.form['runCommand'],
        'type' : request.form['runType']
    }).inserted_id
    mongo.db.Class.update({
        '_id' : ObjectId(request.form['class'])
    },{
        '$push' : { 'assignments' : id }
    })
    return redirect(url_for('dashboard'), code=307)

@app.route('/addAClass', methods=["POST"])
def addAClass():
    return render_template('pages/addClass.html')

@app.route('/enroll', methods=["POST"])
def enroll():
    mongo.db.Class.update({
        'classCode' : request.form['name']
    }, { '$push' : { 'students' : ObjectId(session['user'])}})
    id = mongo.db.Class.find_one({
        'classCode' : request.form['name']
    })
    print(id)
    mongo.db.User.update({
        '_id' : ObjectId(session['user'])
    }, { '$push' : { 'classes' : id['_id']}})
    return redirect(url_for('dashboard'), code=307)

@app.route('/result', methods=["POST"])
def result():
    classInfo = request.form['class']
    return render_template('pages/result.html', classInfo=classInfo)

@app.route('/signout', methods=["POST"])
def signOut():
    #redirect as post
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=int(80), host='0.0.0.0')
