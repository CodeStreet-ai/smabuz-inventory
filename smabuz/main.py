from app import app, google
from models import db, Users, Products, Sales, Customers, InventoryLogs
from flask import jsonify, session, url_for, request, redirect, render_template


##### LOGIN/GOOGLE OAUTH ROUTES #####

@app.route('/home')
def index():
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()     
        return render_template('home.html', name=user.username, email=user.email, status='Logged In :)')
    return render_template('home.html', name='logged out', email='logged out', status='Logged Out :(')

@app.route('/login/callback')
def login():
    if 'google_token' in session:
                return render_template('home.html', status='Log Out First :)')
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return jsonify({'error': 'Access denied'}), 400

    session['google_token'] = (response['access_token'], '')
    userinfo = google.get('userinfo')

    user_data = userinfo.data
    user = Users.query.filter_by(google_id=user_data['id']).first()
    
    if user:
        # User already exists, log them in
        user.username = user_data['name']
        user.email = user_data['email']
    else:
        # Check for existing username and email, since it is gmail.
        existing_user = Users.query.filter((Users.username == user_data['name']) & (Users.email == user_data['email'])).first()
        if existing_user:
            # Update the google_id for the existing user and log them in
            existing_user.google_id = user_data['id']
            user = existing_user
        else:
            # Create new user
            user = Users(
                username=user_data['name'],
                email=user_data['email'],
                google_id=user_data['id']
            )
            db.session.add(user)
    
    db.session.commit()
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

#### PRODUCTS ####
# view all products created by the user
@app.route('/products', methods=['GET'])
def view_products():
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            products = Products.query.filter_by(user_id=user.id).all()
            products_list = [{
                'id': product.id,
                'code': product.code,
                'name': product.name,
                'quantity': product.quantity,
                'price': product.price
            } for product in products]
    # TODO proper redirect, url_for link to pages.
            return jsonify(products_list), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

# view one product of choice
@app.route('/product/<int:product_id>', methods=['GET'])
def view_product(product_id):
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            product = Products.query.filter_by(id=product_id, user_id=user.id).first()
            if product:
                product_data = {
                    'id': product.id,
                    'code': product.code,
                    'name': product.name,
                    'quantity': product.quantity,
                    'price': product.price
                }
                return jsonify(product_data), 200
            else:
                return jsonify({'error': 'Product not found'}), 404
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

# logged in user creates a product
@app.route('/product/create', methods=['POST'])
def create_product():
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            product_data = request.json
            new_product = Products(
                code=product_data['code'],
                name=product_data['name'],
                quantity=product_data['quantity'],
                price=product_data['price'],
                user_id=user.id  # Associating product with the user
            )
            db.session.add(new_product)
            db.session.commit()
    # TODO proper redirect, url_for link to pages.
            return jsonify({'message': 'Product created successfully'}), 201
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'Unauthorized'}), 401        

@app.route('/product/edit/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            product = Products.query.filter_by(id=product_id, user_id=user.id).first()
            if product:
                product_data = request.json
                product.code = product_data.get('code', product.code)
                product.name = product_data.get('name', product.name)
                product.quantity = product_data.get('quantity', product.quantity)
                product.price = product_data.get('price', product.price)
                db.session.commit()
    # TODO proper redirect, url_for link to pages.
                return jsonify({'message': 'Product updated successfully'}), 200
            else:
                return jsonify({'error': 'Product not found'}), 404
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/product/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            product = Products.query.filter_by(id=product_id, user_id=user.id).first()
            if product:
                db.session.delete(product)
                db.session.commit()
# TODO proper redirect, url_for link to pages.
                return jsonify({'message': 'Product deleted successfully'}), 200
            else:
                return jsonify({'error': 'Product not found'}), 404
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

#### SALES ####

# logged in user creates sales, everytime something is purchased
@app.route('/sale/create', methods=['POST'])
def create_sale():
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            sale_data = request.json
            new_sale = Sales(
                product_id=sale_data['product_id'],
                customer_id=sale_data.get('customer_id'),
                user_id=user.id,  # Associating sale with the user
                quantity=sale_data['quantity'],
                price=sale_data['price'],
                date_sold=sale_data['date_sold']
            )
            db.session.add(new_sale)
            db.session.commit()
# TODO proper redirect, url_for link to pages.
            return jsonify({'message': 'Sale created successfully'}), 201
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

# view all sales
@app.route('/sales', methods=['GET'])
def view_sales():
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            sales = Sales.query.filter_by(user_id=user.id).all()
            sales_list = [{
                'id': sale.id,
                'product_id': sale.product_id,
                'customer_id': sale.customer_id,
                'quantity': sale.quantity,
                'price': sale.price,
                'date_sold': sale.date_sold
            } for sale in sales]
# TODO proper redirect, url_for link to pages.
            return jsonify(sales_list), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

# view one sale
@app.route('/sale/<int:sale_id>', methods=['GET'])
def view_sale(sale_id):
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            sale = Sales.query.filter_by(id=sale_id, user_id=user.id).first()
            if sale:
                sale_data = {
                    'id': sale.id,
                    'product_id': sale.product_id,
                    'customer_id': sale.customer_id,
                    'quantity': sale.quantity,
                    'price': sale.price,
                    'date_sold': sale.date_sold
                }
# TODO proper redirect, url_for link to pages.
                return jsonify(sale_data), 200
            else:
                return jsonify({'error': 'Sale not found'}), 404
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

# create an inventory log to track a product
@app.route('/inventory_log/create', methods=['POST'])
def create_inventory_log():
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            log_data = request.json
            new_log = InventoryLogs(
                product_id=log_data['product_id'],
                user_id=user.id,  # Associating log with the user
                quantity=log_data['quantity'],
                action=log_data['action'],
                date=log_data['date']
            )
            db.session.add(new_log)
            db.session.commit()
# TODO proper redirect, url_for link to pages.
        
            return jsonify({'message': 'Inventory log created successfully'}), 201
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401


#### INVENTORY LOGS ####  TODO track product changes and update them in actions, track quantity from number of products.
# view all inventory logs
@app.route('/inventory_logs', methods=['GET'])
def view_inventory_logs():
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            logs = InventoryLogs.query.filter_by(user_id=user.id).all()
            logs_list = [{
                'id': log.id,
                'product_id': log.product_id,
                'quantity': log.quantity,
                'action': log.action,
                'date': log.date
            } for log in logs]
# TODO proper redirect, url_for link to pages.
            return jsonify(logs_list), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

# view one inventory log
@app.route('/inventory_log/<int:log_id>', methods=['GET'])
def view_inventory_log(log_id):
    if 'google_token' in session:
        userinfo = google.get('userinfo')
        user_data = userinfo.data
        user = Users.query.filter_by(google_id=user_data['id']).first()
        
        if user:
            log = InventoryLogs.query.filter_by(id=log_id, user_id=user.id).first()
            if log:
                log_data = {
                    'id': log.id,
                    'product_id': log.product_id,
                    'quantity': log.quantity,
                    'action': log.action,
                    'date': log.date
                }
# TODO proper redirect, url_for link to pages.            
                return jsonify(log_data), 200
            else:
                return jsonify({'error': 'Inventory log not found'}), 404
        else:
            return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

#### CUSTOMERS ####
# i dont think there is need for this right now.
if __name__ == '__main__':
    app.run(debug=True)