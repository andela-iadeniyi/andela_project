from flaskweb import app, auth
from flask import render_template, request, session, make_response, url_for, redirect, jsonify
from models import db, User, Deposit, Account, Withdraw, Account_Pin, generate_password_hash
from form import SignupForm, SigninForm, DepositForm, WithdrawalForm
from bank import Banks


dpo = Banks()

@auth.get_password
def get_password(username):
    if username == 'ibonly':
        return 'python'
    return None
@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
@app.route('/ibrbank/api/v1.0/value/', methods=['GET'])
# @auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/ibrbank/api/v1.0/value/<int:task_id>', methods=['GET'])
# @auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})


@app.route('/ibrbank/api/v1.0/value', methods=['POST'])
# @auth.login_required
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201
'''

@app.route('/ibrbank/api/v1.0/value/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and \
            not isinstance(request.json['title'], six.string_types):
        abort(400)
    if 'description' in request.json and \
            not isinstance(request.json['description'], six.string_types):
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description',
                                              task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})

@app.route('/ibrbank/api/v1.0/value/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})





@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
   
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data, form.account.data)
			db.session.add(newuser)
			db.session.commit()
			session['email'] = newuser.email

			pin = Account_Pin(newuser.uid, dpo.randomNum())
			db.session.add(pin)
			db.session.commit()
			return render_template('welcome.html', fname=newuser.firstname, lname=newuser.lastname, actnumber=newuser.uid, actpin=pin.pin)

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
		session['fname'] = user.firstname
		session['lname'] = user.lastname
		return render_template('profile.html')

@app.route('/deopsit', methods=['GET', 'POST'])
def deposit():
	if 'email' not in session:
		return redirect(url_for('signin'))
	form = DepositForm()
   
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('deposit.html', form=form)
		else:
			deposit = Deposit(form.accountno.data, form.depositor.data, form.amount.data)
			db.session.add(deposit)
			db.session.commit()
			return "True"

			return "False"

	elif request.method == 'GET':
		return render_template('deposit.html', form=form)

@app.route('/accountinfo')
def accountinfo():
	if 'email' not in session:
		return redirect(url_for('signin'))

	return render_template('accountinfo.html', TotalDeposit=dpo.totaldeposit(), ShowDep=dpo.deposithistory(), TotalWithdrawal=dpo.withdraw(), AccountBalance=dpo.balance())

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
	if 'email' not in session:
		return redirect(url_for('signin'))
	else:
		form = WithdrawalForm()

		if request.method == 'POST':
			if form.validate() == False:
				return render_template('withdraw.html', form=form)
			else:
				if form.amount.data.isdigit():
					if int(form.amount.data) < 0 or int(form.amount.data) > int(dpo.balance()):
						return "NOO"
					else:
						if int(dpo.selectpin()) == int(form.withdrawpin.data):
							withd =  Withdraw(session['uid'], form.amount.data)
							db.session.add(withd)
							db.session.commit()
							return "True"
						return "pin"
				else:
					return "NOO"
		elif request.method == 'GET':
			return render_template('withdraw.html', spin=dpo.selectpin(), withdrawhistory=dpo.witdrawhistory(), form=form)


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
	session.clear()
	return redirect(url_for('home'))