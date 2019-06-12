from flask import Blueprint, render_template
from simpledu.models import Course
from simpledu.forms import LoginForm, RegisterForm
from flask import flash
from flask import redirect, url_for
from flask_login import login_user, logout_user, login_required


front = Blueprint('front', __name__)

@front.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@front.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # validate_on_submit 是flask-wtf 提供的FlaskForm中封装的一个方法
    # 返回值是一个布尔值，若表单提交了并且在对应的form中声明的表单数据验证器对用户
    # 提交的表单数据验证通过，则返回True，否则返回False
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'success')
    return redirect(url_for('.index'))