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

if __name__ == '__main__':
    app.run(debug=True)