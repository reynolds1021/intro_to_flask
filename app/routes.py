from app import app, db, Message, mail
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

# Import for Forms
from app.forms import UserInfoForm, LoginForm, BlogPostForm

# Import for Models
from app.models import User, Post

@app.route('/')
def index():

    context = {
        "posts": Post.query.all()
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


@app.route('/createposts', methods=['GET', 'POST'])
@login_required
def createposts():
    form = BlogPostForm()
    context = {
        'form': form
    }
    if request.method == 'POST' and form.validate():
        # Get Information
        title = form.title.data
        content = form.content.data
        user_id = current_user.id

        # Create new instance of Post
        new_post = Post(title, content, user_id)

        # Add post to db
        db.session.add(new_post)
        db.session.commit()

        # flash success message
        flash("You have successfully created a new post", 'success')

        return redirect(url_for('createposts'))

    return render_template('createposts.html', **context)


@app.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    update_form = BlogPostForm()
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST' and update_form.validate():
        title = update_form.title.data
        content = update_form.content.data
        user_id = current_user.id 

        post.title = title
        post.content = content
        post.user_id = user_id

        db.session.commit()
        return redirect(url_for('post_update', post_id=post.id))

    return render_template('post_update.html', form=update_form, post=post)


@app.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))