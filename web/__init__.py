import os
import configparser
from flask import Flask
from flask_login import LoginManager
from flaskext.mysql import MySQL

db = MySQL(autocommit=True)


def create_app() -> Flask:
    config = configparser.ConfigParser()
    config.read(os.environ.get('UPDAEMON_CONFIG_FILE'))

    app = Flask(__name__)

    # replace with the result of
    # python -c 'import secrets; print(secrets.token_hex())'
    app.config['SECRET_KEY'] = '28d1a97bf8a78683fadd40686dbf0560a02abbb6ace48a255775490aac44cbb8'

    app.config['MYSQL_DATABASE_HOST'] = config.get('db', 'host')
    app.config['MYSQL_DATABASE_USER'] = config.get('db', 'user')
    app.config['MYSQL_DATABASE_PASSWORD'] = config.get('db', 'password')
    app.config['MYSQL_DATABASE_DB'] = config.get('db', 'name')

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id: int) -> User:
        return User.from_id(user_id)

    return app

