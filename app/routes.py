from app import app, db
from flask import render_template, request, redirect, url_for

# Import for Forms
from app.forms import UserInfoForm

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

        return redirect(url_for('index'))
    return render_template('register.html', **context)