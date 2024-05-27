from flask_restful import fields

UserFields = {
    'id' : fields.Integer ,
    'username' : fields.String,
    'email' : fields.Integer,
    'password_hash': fields.String,
    'role_id': fields.Integer

}
ProductFields={
    'id': fields.Integer,
    'code': fields.String,
    'name': fields.String,
    'quantity': fields.Integer,
    'price': fields.Integer,
    'product_id': fields.Integer
}
SaleFields={
    'id': fields.Integer,
    'product_id': fields.Integer,
    'customer_id': fields.Integer,
    'quantity': fields.Integer,
    'price': fields.Integer,
    'date_sold': fields.DateTime
}
CustomerFields={
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}
InventoryFields={
    'id': fields.Integer,
    'product_id': fields.Integer,
    'quantity': fields.Integer,
    'action': fields.String,
    'date': fields.DateTime
}