from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)
"""flask shell

db.create_all()
# db migrations
flask db migrate -m "Description of your changes"
flask db upgrade
"""

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    google_id = db.Column(db.String(200), unique=True)
    products = db.relationship('Products', backref='user')  # One-to-Many (Optional)

    def __repr__(self):
        return "<Users {}>".format(self.id)

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Removed for flexibility
    sales = db.relationship('Sales', backref='product')  # One-to-Many
    inventory_logs = db.relationship('InventoryLogs', backref='product')  # One-to-Many

    def __repr__(self):
        return "<Products {}>".format(self.id)

class Sales(db.Model): #record
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))  # Optional - Foreign Key for Customer
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    date_sold = db.Column(db.DateTime)
    customer = db.relationship('Customers', backref='customer_sales')  # One-to-Many (Optional)

    def __repr__(self):
        return "<Sales {}>".format(self.id)

class Customers(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return "<Customers {}>".format(self.id)

class InventoryLogs(db.Model):
    __tablename__ = 'inventory_logs'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer)
    action = db.Column(db.String(50))  # "Added", "Removed", "Sold" etc.
    date = db.Column(db.DateTime)

    def __repr__(self):
        return "<InventoryLogs {}>".format(self.id)
