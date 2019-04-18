# Run with command [FLASK_APP=app.py FLASK_DEBUG=1 flask run]
# Will reload on save

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('pages/main.html')
