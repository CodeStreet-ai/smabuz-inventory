from app import app, google
from models import db, Users, Products, Sales, Customers, InventoryLogs
from flask import jsonify, session, url_for, request, redirect
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, get_jwt_identity


##### USER ROUTES #####
@app.route('/api/smabuz', methods=['GET'])
def smabuz():
    return jsonify({'message':'Welcome to Smabuz!'})

@app.route('/api/')
@jwt_required()
def index():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(google_id=session['google_token'][0]).first()
    return jsonify({
        'username': user.username,
        'email': user.email,
    })

@app.route('/api/login/callback')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/api/logout')
@jwt_required()
def logout():
    response = jsonify({'message': 'Logged out successfully'})
    unset_jwt_cookies(response)
    return response

@app.route('/api/login/authorized')
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

    access_token = create_access_token(identity=user.email)
    return redirect(url_for('token', token=access_token))


@app.route('/api/token')
def token():
    token = request.args.get('token')
    return jsonify({'token': token})

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)