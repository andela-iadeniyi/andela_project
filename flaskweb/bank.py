from models import db, User, Deposit, Account
from flask import session
import random

class Banks(object): 

	def totaldeposit(self):
		deptotal = 'select * from `deposit` where `to` ='+str(session['uid'])
		result = db.engine.execute(deptotal)
		totalDeposit = 0
		for row in result:
		    totalDeposit += row[3]
		return totalDeposit

	def deposithistory(self):
		depall = 'select * from `deposit` where `to` ='+str(session['uid'])
		depo = db.engine.execute(depall)
		showdep = {}
		for row in depo:
		    showdep[row[4]] = row[3]
		return showdep
	
	def withdraw(self):
		deptotal = 'select * from `withdrawal` where `actno` ='+str(session['uid'])
		result = db.engine.execute(deptotal)
		withdraw = 0
		for row in result:
		    withdraw += row[2]
		return withdraw

	def witdrawhistory(self):
		depall = 'select * from `withdrawal` where `actno` ='+str(session['uid'])
		depo = db.engine.execute(depall)
		showdep = {}
		for row in depo:
		    showdep[row[3]] = row[2]
		return showdep

	def selectpin(self):
		depall = 'select * from `account_pin` where `actno` ='+str(session['uid'])
		depo = db.engine.execute(depall)
		dip = {}
		for r in depo:
			dip = r[2] 
		return dip
	
	def balance(self): 
		return self.totaldeposit() - self.withdraw()

	def randomNum(self):
		first = random.randint(1,9)
		first = str(first)
		n = 5
		nrs = [str(random.randrange(10)) for i in range(n-1)]
		for i in range(len(nrs)):
			first += str(nrs[i])
		return str(first)