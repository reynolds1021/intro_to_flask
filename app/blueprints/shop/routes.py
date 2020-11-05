from . import bp as shop
from flask import render_template, redirect, url_for, request, session, flash
from .models import Product

@shop.route('/')
def get_products():
    context = {
        'products': Product.query.all()
    }
    return render_template('marketplace.html', **context)


@shop.route('/add')
def add_to_cart():
    _id = int(request.args.get('id'))
    p = Product.query.get(_id)
    item = {
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'image': p.image,
        'in_stock': p.in_stock,
        'description': p.description
    }
    session['cart']['items'].append(item)
    session['cart']['cart_total'] = 0
    for i in session['cart']['items']:
        session['cart']['cart_total'] += i['price']
            
    flash(f'{p.name} has been added to your cart', 'success')
    return redirect(url_for('shop.get_products'))

@shop.route('/cart')
def cart():
    display_cart = []
    session['cart']['cart_total'] = 0
    for i in session['cart']['items']:
        if i not in display_cart:
            display_cart.append(i) 
        session['cart']['cart_total'] += i['price']
    # for i in display_cart:
    #     i['qty'] = session['cart']['items'].count(i)
    context = {
        'items': display_cart,
        'cart_total': session['cart']['cart_total']
    }
    return render_template('cart.html', **context)

@shop.route('/remove')
def remove_from_cart():
    _id = int(request.args.get('id'))
    for item in session['cart']['items']:
        if _id == item['id']:
            session['cart']['items'].remove(item)
            flash('You have removed {} from you cart'.format(item['name']), 'danger')
            break
    return redirect(url_for('shop.cart'))

@shop.route('/clear')
def clear_cart():
    session['cart']['items'].clear()
    session['cart']['cart_total'] = 0
    flash('All items have been cleared from your cart', 'danger')
    return redirect(url_for('shop.cart'))
