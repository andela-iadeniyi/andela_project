from flask.ext.wtf import Form
from wtforms import TextField,TextAreaField, SubmitField, validators, ValidationError, PasswordField, BooleanField, SelectField
from wtforms.validators import Required
from models import db, User, Account, Deposit
from flask import session

class SignupForm(Form):

  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  account = SelectField('Account Type', choices=[('0', 'Select Account Type'), ('1', 'Savings'), ('2', 'Current'), ('3', 'Fixed')])
  submit = SubmitField("Sign Up")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class DepositForm(Form):
  accountno = TextField("Account Number", [validators.Required("Enter the account number.")])
  depositor = TextField("Deposit's Name", [validators.Required("Enter Depositors' name.")])
  amount = TextField("Amount Deposited", [validators.Required("Enter amount to Deposit")])
  submit = SubmitField("  Submit  ")

  def __init__(self, *arg, **kwargs):
    Form.__init__(self, *arg, **kwargs)

class WithdrawalForm(Form):
  amount = TextField("Amount to Withdraw", [validators.Required("Enter the the exact Amount you want to withdraw.")])
  withdrawpin = TextField("Transaction PIN", [validators.Required("Enter Transaction PIN.")])
  submit = SubmitField("  Submit  ")

  def __init__(self, *arg, **kwargs):
    Form.__init__(self, *arg, **kwargs)


class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      session['uid'] = user.uid
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False