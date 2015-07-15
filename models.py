from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
	account_type = db.Column(db.Integer)

	def __init__(self, firstname, lastname, email, password, account):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)
		self.account_type = account

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)


class Account(db.Model):
	__tablename__ = 'account_type'
	uid = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	# group_id = SelectField(u'Group', coerce=int)

	def __ini__(self, uid):
		self.uid = uid

class Deposit(db.Model):
	__tablename__ = 'deposit'
	uid = db.Column(db.Integer, primary_key = True)
	to = db.Column(db.String(100))
	by = db.Column(db.String(100))
	amount = db.Column(db.Integer)
	date = db.Column(db.String(54))

	def __init__(self, to, by, amount, date=None):
		#uid = db.Column(db.Integer, primary_key = True)
		self.to = to.lower()
		self.by = by.lower()
		self.amount = amount
		self.date = datetime.now()


'''
  def edit_user(request, id):
      user = User.query.get(id)
      form = UserDetails(request.POST, obj=user)
      form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
'''