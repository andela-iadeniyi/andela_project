from flask import Flask
from models import db
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

app.secret_key = 'development key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/development'

db.init_app(app)

import flaskweb.routes

