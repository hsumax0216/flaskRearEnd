from flask import Flask
#from flask_bootstrap import Bootstrap
#from flask_mail import Mail
#from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

#bootstrap = Bootstrap()
#mail = Mail()
#moment = Moment()
db = SQLAlchemy()

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #bootstrap.init_app(app)
    #mail.init_app(app)
    #moment.init_app(app)
    db.init_app(app)
    migrate = Migrate(app,db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.after_request(after_request)
    return app
