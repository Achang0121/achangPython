from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 注意这里不再传入 app 了
db = SQLAlchemy()


class Base(db.Model):
    """所有 model 的一个基类，默认添加了时间戳"""
    # 表示不要把这个类当作 Model 类
    __abstract__ = 'True'
    # 设置了 default 和 onupdate 这两个时间戳都不需要自己去维护
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow)

    
class User(Base, UserMixin):
    __tablename__ = 'user'
    # 用数值表示角色， 方便判断是否有权限，比如说有个操作要角色是员工
    # 及以上的用户才可以做，那么只要判断 user.role >= ROLE_SATFF
    # 就可以了，数值之间设置了 10 的间隔是为了方便以后加入其它角色
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    # 默认情况下，sqlalchemy 会以字段名来定义列名， 但这里是 _password, 所以明确指定数据库列表名为 password
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))
    publish_courses = db.relationship('Course')
    
    def __repr__(self):
        return '<User:{}>'.format(self.username)
    
    @property
    def password(self):
        """python 风格的 getter """
        return self._password
    
    @password.setter
    def password(self, orig_password):
        """python 风格的 setter， 这样设置 user.password 就会自动为
        password 生成哈希值存入 _password字段
        """
        self._password = generate_password_hash(orig_password)
        
    def check_password(self, password):
        """判断用户输入的密码和存储的hash密码是否相等"""
        return check_password_hash(self._password, password)
    
    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
    
    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

    
class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author= db.relationship('User', uselist=False)
    