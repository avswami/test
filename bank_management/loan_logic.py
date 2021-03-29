from flask import Flask
from flask import request, jsonify, make_response
import jwt
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from model_schema import LoanSchema, db, app
from model_schema import Customer, Loan, CustomerSchema
import logging



app.config['SECRET_KEY'] = 'AV'
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

customer_schema = CustomerSchema()
loan_schema = LoanSchema()

@app.route('/login', methods=['POST'])
def login():
	app.logger.info('Inside login method')
	email = request.json["email"]
	password = request.json["password"]

	if not email or not password:
		app.logger.error('Wrong username or password')
		return make_response(jsonify({'Message' : 'Enter the username and password'}), 401)
	try:
		cust = Customer.query.filter_by(email=email).first()
		if not cust:
			app.logger.error('username does not exist')
			return make_response(jsonify({'Message' : 'User does not exist'}), 400)

		if check_password_hash(cust.password, password):
			app.logger.info('Generating token')
			# generates the JWT Token
			token = jwt.encode({'username': cust.username, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
			return make_response(jsonify({'token' : token.decode('UTF-8')}), 200)
	except Exception:
		return make_response(jsonify({'Message' : 'Incorrect password'}), 400)


# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		app.logger.info('Verifying token')
		token = None
		# jwt is passed in the request header
		if 'token' in request.headers:
			token = request.headers['token']
		# return 401 if token is not passed
		if not token:
			app.logger.warning('Token is missing')
			return jsonify({'message': 'Token is missing !!'}), 402

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
			current_user = Customer.query.filter_by(username=data['username']).first()
			app.logger.info('token valid')
			print("token valid")
		except Exception:
			return jsonify({'message' : 'Token is invalid !!'}),403
		# returns the current logged in users contex to the routes
		return f(current_user, *args, **kwargs)

	return decorated

@app.route("/applyLoan", methods=["POST"])
@token_required
def applyLoan(current_user):
	app.logger.info('Inside apply loan method')
	errors =loan_schema.validate(request.json)
	if errors:
		return make_response(str(errors),400)

	loan_id = request.json["loan_id"] 
	loanType=request.json["loanType"]
	loanAmount=request.json["loanAmount"]
	date=request.json["date"]
	interest=request.json["interest"]
	duration=request.json["duration"]
	customer_id=current_user.cust_id

	try:
		loan=Loan(loan_id,loanType,loanAmount,date,interest,duration,customer_id)
		db.create_all()
		db.session.add(loan)
		db.session.commit()
		return make_response(jsonify({'Message' : 'Loan applied Successfully'}), 200)
	except IntegrityError:
		return make_response(jsonify({'Message' : 'Error in Unique constraint '}), 400)
	
	

@app.route("/viewLoan/<loan_id>", methods=["GET"])
@token_required
def viewLoan(current_user,loan_id):
	app.logger.info('Inside view loan method')
	try:
		loan1 = Loan.query.filter_by(loan_id=loan_id).first()
		print (loan1)
		if not loan1:
			return make_response("Loan id not exist", 400)
		elif(loan1.customer_id==current_user.cust_id):
			return loan_schema.dump(loan1)
		else:
			return make_response(jsonify({'Message' : 'Check your Loan ID'}), 400)
	except Exception:
		return make_response(jsonify({'Message' : 'Bad Request'}), 400)



if __name__ == "__main__": 
	app.run(debug = True) 
