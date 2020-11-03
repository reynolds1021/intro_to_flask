from app import db, mail, Message
from . import bp as auth
from flask import request, render_template, redirect, url_for, flash
from app.forms import UserInfoForm, LoginForm
from app.models import User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash



@auth.route('/register', methods=['GET', 'POST'])
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


@auth.route('/login', methods=['GET', 'POST'])
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


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))

