# Run with command "python app.py"
# Will reload on save

from flask import Flask, render_template, redirect, url_for, request, session, send_file
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.utils import secure_filename
import os
import sys
import random
from datetime import datetime
import grader

ALLOWED_EXTENSIONS = set(['txt', 'py', 'c', 'java', 'hs'])

app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/AutoGrader"

mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download', methods=['POST'])
def downloadDescription():
    return send_file(request.form['descPath'], as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    classInfo = request.form['class']
    assignId = request.form['assignId']
    assignment = mongo.db.Assignment.find_one({'_id' : ObjectId(assignId)})
    if 'file' not in request.files:
        return render_template('pages/assignment.html', status="noFile", assignment=assignment, classInfo=classInfo, assignId=assignId)

    student_file = request.files['file']
    if student_file.filename == '':
        return render_template('pages/assignment.html', status="noFile", assignment=assignment, classInfo=classInfo, assignId=assignId)

    if student_file and allowed_file(student_file.filename):
        filename = secure_filename(student_file.filename)
        mypath = os.path.dirname(__file__)
        mypath = mypath[0:len(mypath) - 7] + "/studentSubmissions/"
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        student_file.save(os.path.join(mypath, filename))
        mypath = mypath + filename
        if assignment['language'] == 'C':
            score = grader.gradeC(mypath, filename, assignId, assignment['type'])
        elif assignment['language'] == 'Java':
            score = grader.gradeJava(mypath, assignId, assignment['type'])
        else:
            score = grader.gradePython(mypath, assignId, assignment['type'])
        mongo.db.Assignment.update({'_id' : ObjectId(assignId)}, {'$set': {'score': score}})
        assignment = mongo.db.Assignment.find_one({'_id' : ObjectId(assignId)})
        userId = session['user']
        submission = createSubmission(userId, assignId, score)
        pastDue = checkOpen(assignment['dueDate'].split('/'))
        return render_template('pages/assignment.html', status="uploaded", assignment=assignment, classInfo=classInfo, assignId=assignId, submission=submission, open=pastDue)

def createSubmission(userId, assignId, score):
    mongo.db.Submission.update(
        {
            'user' : ObjectId(userId),
            'assignment' : ObjectId(assignId),
        },
        {
            'user' : ObjectId(userId),
            'assignment' : ObjectId(assignId),
            'score' : score
        }, upsert=True)

    id = mongo.db.Submission.find_one({
        'user' : ObjectId(userId),
        'assignment' : ObjectId(assignId),
        'score' : score
    })

    return id

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
@app.route('/dashboard', methods=["POST", "GET"])
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
    userId = session['user']
    assignId = request.form['assignment']
    submission = mongo.db.Submission.find_one({'user' : ObjectId(userId), 'assignment' : ObjectId(assignId)})
    if submission == None:
        submission = createSubmission(userId, assignId, 0)
    pastDue = checkOpen(assignment['dueDate'].split('/'))
    descPath = getDescriptionFile(assignId)
    return render_template('pages/assignment.html', descPath=descPath, submission=submission, classInfo=classInfo, assignment=assignment, assignId=assignId, open=pastDue)

def getDescriptionFile(assignId):
    path = os.path.dirname(__file__)
    path = path[0:len(path) - 7] + "/assignmentFiles/" + assignId + "/desc/"
    path += os.listdir(path)[0]
    return path

def checkOpen(dueDate):
    due = datetime(int(dueDate[2]), int(dueDate[0]), int(dueDate[1]))
    date = datetime.today()
    return(due > date)

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
    return redirect(url_for('dashboard'))

@app.route('/createAssignment', methods=["POST"])
def createAssignmentRoute():
    return render_template('pages/createAssignment.html', id=request.form['class'])

@app.route('/createAssignmentSubmit', methods=["POST"])
def createAssignment():
    result_files = request.files.getlist("resultFiles")
    total = len(result_files)*10
    id = mongo.db.Assignment.insert_one({
        'name' : request.form['name'],
        'dueDate' : request.form['dueDate'],
        'language' : request.form['language'],
        'type' : request.form['runType'],
        'total' : total,
    }).inserted_id
    mongo.db.Class.update({
        '_id' : ObjectId(request.form['class'])
    },{
        '$push' : { 'assignments' : id }
    })

    renameFiles(id, result_files,"results/")
    test_files = request.files.getlist("testFiles")
    renameFiles(id, test_files, "tests/")
    desc_file = request.files.getlist("descFile")
    renameFiles(id, desc_file, "desc/")
    return redirect(url_for('dashboard'))

def renameFiles(id, files, ty):
    for f in files:
        filename = secure_filename(f.filename)
        path = os.path.dirname(__file__)
        path = path[0:len(path) - 7] + "/assignmentFiles/"
        if not os.path.isdir(path):
            os.makedirs(path)

        path = path + str(id) + "/"

        try:
            os.makedirs(path)
        except:
            pass

        path = path + ty
        try:
            os.makedirs(path)
        except:
            pass

        f.save(os.path.join(path, filename))
    return

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
    assignment = request.form['assignment']
    submissions = mongo.db.Submission.find({'assignment' : ObjectId(assignment)})
    grades = {}
    for sub in submissions:
        user = sub['user']
        user = mongo.db.User.find_one({
            '_id' : user
        })
        grades[user['name']] = sub['score']
    return render_template('pages/result.html', classInfo=classInfo, grades=grades)

@app.route('/signout', methods=["POST"])
def signOut():
    #redirect as post
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=int(80), host='0.0.0.0')
