from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
	
app = Flask(__name__)

app.config['SECRET_KEY'] = '66373fff253d434877c542c6715f678f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///election.db'

db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

from election_system import routes