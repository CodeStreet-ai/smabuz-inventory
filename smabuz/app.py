from flask import Flask
from flask_restful import Api
from config import conn

app = Flask(__name__)
api = Api(app) # RESTful instance.

app.config['SQLALCHEMY_DATABASE_URI'] = conn()


from routes import *

api.add_resource(GetUsers, '/users') #smabuz restricted
api.add_resource(GetPostUser, '/user/<int:ui>')

api.add_resource(GetProducts, '/products')
api.add_resource(GetPostPutDelProduct, '/product/<int:ui>')


api.add_resource(GetSales, '/sales')
api.add_resource(GetPostSale, '/sale/<int:ui>')

api.add_resource(GetCustomers, '/customers')
api.add_resource(GetPostCustomer, '/customer/<int:ui>')

api.add_resource(GetPostInventoryLogs, '/logs')
