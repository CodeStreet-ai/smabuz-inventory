from flask import Flask
from config import conn
from flask_oauthlib.client import OAuth
from flask_cors import CORS
from utils.auth import GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID
from decouple import config
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# flask app configurations 
app.config['SQLALCHEMY_DATABASE_URI'] = conn()
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

#
oauth = OAuth(app)
jwt = JWTManager(app)

google = oauth.remote_app('google',
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET,
    request_token_params={
        'scope': 'email profile', # basic google email and user info.
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)