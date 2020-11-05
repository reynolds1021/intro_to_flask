from app import db, Message, mail
from flask import current_app as app, render_template, request, redirect, url_for, flash, session
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


@app.context_processor
def cart_stuff():
    if 'cart' not in session:
        session['cart'] = {
            'items': [],
            'cart_total': 0
        }
    # Reset cart total to 0 before recounting price of items in cart
    # session['cart']['cart_total'] = 0
    # for i in session['cart']['items']:
    #     session
    return {'cart': session['cart']}
