#!/usr/bin/env python3

from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request

app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello Shiyanlou!'

@app.route('/httptest', methods=['GET', 'POST'])
def httptest():
    if request.method == 'GET':
        return 'It is a get request!'
    if request.method == 'POST':
        return 'It is a post request!'

@app.route('/test')
def test():
    print(url_for('courses', name='java', _external=True))
    return redirect(url_for('index')) 

@app.route('/courses/<name>')
def courses(name):
    return render_template('courses.html', coursename=name)
if __name__ == '__main__':
    app.run()
