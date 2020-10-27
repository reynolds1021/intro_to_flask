from app import app
from flask import render_template


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

@app.route('/register')
def register():
    return render_template('register.html')