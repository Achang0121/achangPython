#!/usr/bin/env python3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/challenge',
    SQLALCHEMY_TRACK_MODIFICATIONS = False))

db = SQLAlchemy(app)


class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name
    

def insert_data():
    java = Category('Java')
    python = Category('Python')

    file1 = File('Hello Java', datetime.now(), java, 'File Content -Java is cool!')
    file2 = File('Hello Python', datetime.now(), python, 'File content -Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()


@app.route('/')
def index():
    # 显示文章名称的列表
    # 页面中需要显示所有文章的标题（title）列表，此外每个标题都需要使用'<a href=""></a>'链接到对应的文章内容页面
    return render_template('index.html', files=File.query.all())


@app.route('/files/<int:file_id>')
def file(file_id):
    # file_id 为File表中的文章ID
    # 需要显示file_id 对应的文章内容、创建时间及类别信息（需要显示类别名称）
    # 如果指定 file_id 的文章不存在，则显示包含字符窗 'shiyanlou 404' 404 错误页面
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html', file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
        
        
if __name__ == '__main__':
    app.run()
