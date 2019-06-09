from flask import Flask, render_template
from simpledu.config import configs
from simpledu.models import db, Course


def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    

def create_app(config):
    """可以根据传入的 config 名称，加载不同的配置"""
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    # SQLAlchemy 的初始化方式改为用 init_app
    db.init_app(app)
    register_blueprints(app)
    
    return app

