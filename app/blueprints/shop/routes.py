from . import bp as shop
from flask import render_template, redirect, url_for, request, session, flash
from .models import Product
import stripe, os

stripe_keys = {
    'secret_key': os.getenv('STRIPE_SECRET_KEY'),
    'publishable_key': os.getenv('STRIPE_PUBLISHABLE_KEY')
}

stripe.api_key = stripe_keys.get('secret_key')

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
    session['display_cart'] = display_cart
    context = {
        'items': display_cart,
        'cart_total': session['cart']['cart_total'],
        'stripe_publishable_key': stripe_keys.get('publishable_key')
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


@shop.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    stripe_line_items = []
    for p in session['display_cart']:
        product_dict = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': p['name'],
                    'description': p['description'],
                    'images': [p['image']]
                },
                'unit_amount': int(p['price'] * 100)
            },
            'quantity': session['cart']['items'].count(p)
        }
        stripe_line_items.append(product_dict)

    
    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=stripe_line_items,
        mode='payment',
        success_url='http://localhost:5000/shop/checkout/success',
        cancel_url='http://localhost:5000/shop/checkout/cancel'
    )
    # Pass session info to success/cancel route
    session['stripe_info'] = stripe_session

    # Clear all items from cart and reset cart_total to 0
    session['cart']['items'].clear()
    session['cart']['cart_total'] = 0

    # Return stripe session back to js in cart.html
    return stripe_session

@shop.route('/checkout/success')
def checkout_success():
    flash('Your order has been completed', 'success')
    return render_template('checkout_success.html', stripe_info=session['stripe_info'])

@shop.route('/checkout/cancel')
def checkout_cancel():
    return render_template('checkout_cancel.html')