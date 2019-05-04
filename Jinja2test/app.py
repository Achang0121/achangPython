#!/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    course = {
        'python': 'lou+ python',
        'java': 'java base',
        'bigdata': 'spark sql',
        'teacher': 'shixiaolou',
        'is_unique': False,
        'has_tag': True,
        'tags': ['c', 'c++', 'docker']
    }

    return render_template('index.html', course=course)

@app.route('/courses/<name>')
def course(name):
    return 'Course: {}'.format(name)
