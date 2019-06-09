from flask import Blueprint, render_template
from simpledu.models import Course

# 省略了 url_prefix，那么默认就是'/'
front = Blueprint('front', __name__)

@front.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)