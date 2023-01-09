from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.typing import ResponseValue
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login() -> str:
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post() -> ResponseValue:
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User(email=email)
    if not user.exists() or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET'])
def signup() -> str:
    return render_template('signup.html')


# # Note: this is not planned to be rolled out in the nearest future.
# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     email = request.args.get('email')
#     password = request.args.get('password')
#     name = request.args.get('name')
#
#     print(email, password, name)
#
#     user = User(
#         email=email,
#         password=generate_password_hash(password, method='sha256'),
#         name=name,
#     )
#
#     print(user.exists())
#
#     if user.exists():
#         flash('User with the specified e-mail address already exists')
#         return redirect(url_for('auth.signup'))
#
#     user.persist()
#
#     return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout() -> ResponseValue:
    logout_user()
    return redirect(url_for('main.index'))
