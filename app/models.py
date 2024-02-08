# models.py

from sqlalchemy.orm import relationship
from app import db

class Product(db.Model):
    # __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    order_details = relationship('OrderDetail', back_populates='product')
    # Add other fields as needed

class Order(db.Model):
    # __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    # Add other fields as needed

class OrderDetail(db.Model):
    # __tablename__ = "orderdetail"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    product = relationship('Product', back_populates='order_details')
    # Add other fields as needed
