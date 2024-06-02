from app import app, google
from models import db, Users, Products, Sales, Customers, InventoryLogs
from flask import jsonify, session, url_for


##### USER ROUTES #####
@app.route('/api/smabuz', methods=['GET'])
def smabuz():
    return jsonify({'message':'Welcome to Smabuz!'})

@app.route('/api/')
def index():
    if 'google_token' in session:
        user = Users.query.filter_by(google_id=session['google_token'][0]).first()
        return jsonify({
            'username': user.username,
            'email': user.email,
        })
    return jsonify({'message': 'User not logged in'}), 401

@app.route('/api/login/callback')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/api/logout')
def logout():
    session.pop('google_token', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return jsonify({'error': 'Access denied'}), 400
    
    session['google_token'] = (response['access_token'], '')
    userinfo = google.get('userinfo')
    
    user_data = userinfo.data
    user = Users.query.filter_by(google_id=user_data['id']).first()
    
    if not user:
        user = Users(
            username=user_data['name'],
            email=user_data['email'],
        )
        db.session.add(user)
        db.session.commit()
    
    return jsonify({
        'username': user.username,
        'email': user.email,
    })

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)