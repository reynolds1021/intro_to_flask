from app import app, db, Message, mail
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

# Import for Forms
from app.forms import UserInfoForm, LoginForm

# Import for Models
from app.models import User

@app.route('/')
def index():

    context = {
        "customer_name": "Brian",
        "customer_username": "bstanton",
        "items": {
            1: 'Ice Cream',
            2: 'Bread',
            3: 'Lemons',
            4: 'Cereal'
        }
    }
    return render_template('index.html', **context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()
    context = {
        'form': form
    }
    if request.method == 'POST' and form.validate():

        # Get Information
        username = form.username.data
        email = form.email.data
        password = form.password.data

        print(username, email, password)

        # Create new instance of User
        new_user = User(username, email, password)

        # Add user to db
        db.session.add(new_user)
        db.session.commit()

        # flash success message
        flash("You have successfully registered", 'success')

        # Flask Email Sender
        msg = Message(f'Thanks for signing up, {username}!', recipients=[email])
        msg.body = ('Congrats on signing up! I hope you enjoy our site!!')
        msg.html = ('<h1>Welcome to Our Site</h1>' '<p>This will be super cool!</p>')

        mail.send(msg)

        return redirect(url_for('index'))
    return render_template('register.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {
        'form': form
    }
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        # Query database for user with email
        user = User.query.filter_by(email=email).first()
        # If no user, flash incorrect credentials
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect Email/Password. Please try again', 'danger')
            return redirect(url_for('login'))
        # Log user in
        login_user(user, remember=form.remember_me.data)
        # Flash success message
        flash('You have successfully logged in', 'success')
        # redirect to index
        return redirect(url_for('index'))

    return render_template('login.html', **context)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))


@app.route('/users')
@login_required
def users():
    context = {
        'users': User.query.all()
    }
    return render_template('users.html', **context)