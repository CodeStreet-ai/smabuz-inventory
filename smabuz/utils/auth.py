# TODO all things JWT, Authentication and other middleware functionality.
from decouple import config
from oauthlib.oauth2 import WebApplicationClient

GOOGLE_CLIENT_SECRET= config('GOOGLE_CLIENT_SECRET')
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')