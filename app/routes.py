from app import db, Message, mail
from flask import current_app as app, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# Import for Forms
from app.forms import UserInfoForm, LoginForm

# Import for Models
from app.models import User, Post

@app.route('/')
def index():

    context = {
        "posts": Post.query.all()
    }
    return render_template('index.html', **context)


@app.route('/users')
@login_required
def users():
    context = {
        'users': User.query.all()
    }
    return render_template('users.html', **context)

