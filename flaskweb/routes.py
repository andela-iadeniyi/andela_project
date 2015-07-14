from flaskweb import app
from flask import render_template, request, session, url_for, redirect
from models import db, User, generate_password_hash
from form import SignupForm, SigninForm
'''
@app.route('/testdb')
def testdb()
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works.'
	else:
		return 'Something is broken.'
'''
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
   
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			session['email'] = newuser.email
			return redirect(url_for('profile'))

			return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	if request.method == 'POST':
		if form.validate() == False:
			return "false"
		else:
			session['email'] = form.email.data
			return "true" #redirect(url_for('profile'))	     
	elif request.method == 'GET':
		return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('home'))