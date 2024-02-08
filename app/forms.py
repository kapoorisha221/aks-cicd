# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class OrderForm(FlaskForm):
    customer_name = StringField('Your Name')
    shipping_address = StringField('Shipping Address')
    submit = SubmitField('Place Order')
