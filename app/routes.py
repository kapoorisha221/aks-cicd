# routes.py

from flask import render_template, request, redirect, flash, url_for, session
from app import app, db
from datetime import datetime  # Import the datetime module
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField

from app.models import Product, Order, OrderDetail
from app.forms import OrderForm  # Import your Flask-WTF form


class SearchForm(FlaskForm):
    print("hello")
    search = StringField('Search', validators=[DataRequired()])
    print(search)

@app.route('/', methods=['GET'])
def landing_page():
    search_form = SearchForm(request.args)
    query = Product.query

    if search_form.search.data:
        query = query.filter((Product.category.like(f"%{search_form.search.data}%")) | (Product.category == search_form.search.data))
    # Implement the landing page to search and filter products
    # Query products from the database based on user filters
    products = query.all()
    return render_template('landing_page.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # Implement the product detail page
    product = Product.query.get(product_id)
    return render_template('product_detail.html', product=product)

# @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
# def add_to_cart(product_id):
#     if 'shopping_cart' not in session:
#         session['shopping_cart'] = []  # Initialize the shopping cart as an empty list in the session

#     quantity = int(request.form.get('quantity', 1))  # Get the quantity from the form

#     product = Product.query.get(product_id)  # Query the product based on the product_id

#     if product:
#         # Create an entry for the selected product in the shopping cart
#         cart_item = {
#             'product_id': product.id,
#             'name': product.name,
#             'price': product.price,
#             'quantity': quantity,
#             'subtotal': product.price * quantity
#         }

#         # Add the cart item to the shopping cart in the session
#         session['shopping_cart'].append(cart_item)

#     return redirect(url_for('shopping_basket'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Get the quantity of the product to add from the form data
    quantity = int(request.form.get('quantity'))

    # Retrieve the product from the database
    product = Product.query.get(product_id)

    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('landing_page'))

    # Check if the user has an active (incomplete) order
    user_id = 1  # Replace with your user identification logic
    active_order = Order.query.filter_by(customer_id=user_id).first()

    if not active_order:
        # If the user doesn't have an active order, create one
        active_order = Order(customer_id=user_id, order_date=datetime.now(), total_price=0)
        db.session.add(active_order)
        db.session.commit()

    # Check if the product is already in the user's shopping cart
    existing_item = OrderDetail.query.filter_by(order_id=active_order.id, product_id=product_id).first()

    if existing_item:
        # If the product is already in the cart, update the quantity
        existing_item.quantity += quantity
        existing_item.subtotal = existing_item.quantity * product.price
    else:
        # If the product is not in the cart, create a new OrderDetail record
        new_item = OrderDetail(order_id=active_order.id, product_id=product_id, quantity=quantity, subtotal=quantity * product.price)
        db.session.add(new_item)

    db.session.commit()

    flash('Product added to cart', 'success')
    return redirect(url_for('shopping_basket'))


@app.route('/remove_from_cart/<int:product_id>', methods=['GET'])
def remove_from_cart(product_id):
    # Get the user's active (incomplete) order
    user_id = 1  # Replace with your user identification logic
    active_order = Order.query.filter_by(customer_id=user_id).first()

    if active_order:
        # Check if the product exists in the user's shopping cart
        order_detail = OrderDetail.query.filter_by(order_id=active_order.id, product_id=product_id).first()

        if order_detail:
            # If the product is found in the cart, remove it
            db.session.delete(order_detail)
            db.session.commit()
            flash('Product removed from cart', 'success')
        else:
            flash('Product not found in the cart', 'danger')
    else:
        flash('No active order found', 'danger')

    return redirect(url_for('shopping_basket'))

@app.route('/basket')
def shopping_basket():
    # Implement the shopping basket page
    # Query the user's shopping cart content and display it
    # ...
    # Get the user's shopping cart data (you should implement your own logic to identify the user)
    user_id = 1  # Replace with your user identification logic
    order = Order.query.filter_by(customer_id=user_id).first()
    order_detail = OrderDetail.query.filter_by(order_id=order.id).first()
    if order:
        shopping_cart = OrderDetail.query.filter_by(order_id=order.id).all()
        # shopping_cart.append(product_name)
        total_price = sum(item.subtotal for item in shopping_cart)
    else:
        shopping_cart = []
        total_price = 0.0

    return render_template('basket.html', shopping_cart=shopping_cart ,total_price=total_price)



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Implement the checkout page
    form = OrderForm()  # Create an instance of your Flask-WTF form
    user_id = 1  # Replace with your user identification logic
    order = Order.query.filter_by(customer_id=user_id).first()

    if order:
        # Get the order details for the shopping cart
        shopping_cart = OrderDetail.query.filter_by(order_id=order.id).all()
        total_price = sum(item.subtotal for item in shopping_cart)
    else:
        shopping_cart = []
        total_price = 0.0


    if form.validate_on_submit():
        # Process the user's order and create entries in the Orders and OrderDetails tables

        # Create a new order
        if not order:
            order = Order(customer_id=user_id)
            db.session.add(order)

        # Iterate through items in the shopping cart and create corresponding OrderDetail records
        for item in shopping_cart:
            order_detail = OrderDetail(order_id=order.id, product_id=item.product_id, quantity=item.quantity, subtotal=item.subtotal)
            db.session.add(order_detail)

        # Update the order's total price
        order.total_price = total_price

        # Commit changes to the database
        db.session.commit()

        # After successfully processing the order, you can display a success message and redirect to the 'thank_you' page
        flash('Order successfully processed', 'success')
        return redirect(url_for('thank_you'))
    return render_template('checkout.html', form=form, shopping_cart=shopping_cart, total_price=total_price)

@app.route('/thank_you',methods=['GET', 'POST'])
def thank_you():
    # A thank you page to show order confirmation
    return render_template('thank_you.html')
