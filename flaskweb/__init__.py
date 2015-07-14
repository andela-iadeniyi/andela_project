from flask import Flask
from models import db

app = Flask(__name__)

app.secret_key = 'development key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/development'

db.init_app(app)

import flaskweb.routes

