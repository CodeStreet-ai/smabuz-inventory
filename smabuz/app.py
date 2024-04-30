from flask import Flask
from flask_restful import Api
from config import conn

app = Flask(__name__)
api = Api(app) # RESTful instance.

app.config['SQLALCHEMY_DATABASE_URI'] = conn()

@app.route('/')
def smabuz():
    return {"message": "smabuz v2.0"}


if __name__ == '__main__':
    app.run(debug=True)

