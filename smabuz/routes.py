from flask_restful import Resource
from flask import request
from models import db, UserRoles, Users, Products, Sales, Customers, InventoryLogs



class GetUsers(Resource):
    def get(self):
        users = Users.query.all()
        return users
    
class GetPostUser(Resource):
    def get(self, ui):
        user = Users.query.filter_by(id=ui).first()
        return user
    
    def post(self):
        data = request.json
        user = Users(username=data['name'], email=data['email'], 
                    password_hash=data['password_hash']
                     )
        # TODO hashing, and password authentication, jwt.
        db.session.add(user)
        db.session.commit()

        users = GetUsers.get()

        return users

# TODO logging in and out, jwt authentication.
class LoginUser(Resource):
    def post():
        pass

class GetProducts(Resource):
    def get(self):
        products = Products.query.all()
        return products
    
class GetPostPutDelProduct(Resource):
    def get(self, ui):
        product = Products.query.filter_by(id=ui).first()
        return product
    
    def post(self):
        data = request.json
        product = Products(code=data['code'], name=data['name'],
                           quantity=data['quantity'], price=data['price'])
        db.session.add(product)
        db.session.commit()

        products = GetProducts.get()
        return products

    def put(self):
    # TODO route for editing products.
        pass
    
    def delete(self):
    # TODO route for deleting products.
        pass

class GetSales(Resource):
    def get(self, ui):
        sales = Sales.query.all()
        return sales
    
class GetPostSale(Resource):
    def get(self, ui):
        sale = Sales.query.filter_by(id=ui).first()
        return sale
    
    def post(self):
        data = request.json
        sale = Sales(quantity=data['quantity'], price=data['price'],
                     date_sold=data['date_sold'])
        db.session.add(sale)
        db.session.commit()

        sales = GetSales.get()
        return sales

#supply to retail(not day-day customer)

class GetCustomers(Resource):
    def get(self):
        customers = Customers.query.all()
        return customers
    

class GetPostCustomer(Resource):
    def get(self,ui):
        customers = Customers.query.filter_by(id=ui).first()
        return customers
    
    def post(self):
        data = request.json
        #name -> business name
        customer = Customers(name=data['name'], email=data['email'])

        db.session.add(customer)
        db.session.commit()

        customers = GetCustomers.get()
        return customers

class GetPostInventoryLogs(Resource):
    def get(self):        
        inventory = InventoryLogs.query.all()
        return inventory
    
    def post(self):
        data = request.json
        
        inventory = InventoryLogs(quantity=data['quantity'], action=data['action'],
                                  date=data['date'])
        
        db.sesssion.add(inventory)
        db.session.commit()

        logs = GetPostInventoryLogs.get()
        return logs



    




