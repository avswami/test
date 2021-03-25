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


@app.route('/createCustomer', methods=['POST'])
def signup():
    app.logger.info('Inside create  customer method')
    errors = customer_schema.validate(request.json)
    if errors:
        return make_response(str(errors), 400)
    cust_id = request.json["cust_id"]    
    name = request.json["name"]
    username = request.json["username"]
    password = request.json["password"]
    address = request.json["address"]
    state = request.json["state"]
    country = request.json["country"]
    email = request.json["email"]
    pan = request.json["pan"]
    dob = request.json["dob"]
    accountType = request.json["accountType"]
    contactNo = request.json["contactNo"]
    try:
        cust = Customer.query.filter_by(email=email).first()
        if not cust:
            hash_pass = generate_password_hash(password, method='sha256')
            cust = Customer(cust_id, name, username, hash_pass, address, state, country, email, pan, dob, accountType, contactNo)
            db.create_all()
            db.session.add(cust)
            db.session.commit()
            app.logger.info('Successfully registered')
            return make_response(jsonify({'Message' : 'Successfully registered.'}), 200)
        else:
            app.logger.info('Customer already exists')
            return make_response(jsonify({'Message' : 'Customer already exists.Please Log in.'}), 400)
    except IntegrityError:
        return make_response(jsonify({'Message' : 'Error in Unique constraint '}), 400)


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
            return make_response(jsonify({'token' : token.encode().decode('UTF-8')}), 200)
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


@app.route("/viewCustomer/<int:cust_id>", methods=["GET"])
@token_required
def viewuser(current_user,cust_id):
    try:
        app.logger.info('Inside view customer method')
        cust1 = Customer.query.filter_by(cust_id=cust_id).first()
        if not cust1:
            return make_response("Customer does not exist",400)
        if(cust_id==current_user.cust_id):
            return customer_schema.dump(cust1)
        else:
            return make_response(jsonify({'Message' : 'Check customer id'}),400)
    except Exception:
        return make_response(jsonify({'Message' : 'Bad Request'}), 400)


@app.route("/updateSingleField/<int:cust_id>/<field>", methods=["PUT"])
@token_required
def updateuser(current_user,cust_id,field):
    try:
        app.logger.info('Inside update customer method where single filed gets updated')
        cust1 = Customer.query.filter_by(cust_id=cust_id).first()
        if not cust1:
            return make_response(jsonify({'Message' : "Customer does not exist"}),400)
        if(cust_id==current_user.cust_id):
            if(request.json[field] is not None):
                if field == "password":
                    password=request.json["password"]
                    cust1.password=generate_password_hash(password, method='sha256')
                elif field == "username":
                    cust1.username=request.json["username"]
                elif field == "name":
                    cust1.name=request.json["name"]
                elif field =="address":
                    cust1.address=request.json["address"]
                elif field =="state":
                    cust1.state=request.json["state"]
                elif field =="country":
                    cust1.country=request.json["country"]
                elif field =="pan":
                    cust1.pan=request.json["pan"]
                elif field =="email":
                    cust1.email=request.json["email"]
                elif field =="contactNo":
                    cust1.contactNo=request.json["contactNo"]
                elif field =="dob":
                    cust1.dob=request.json["dob"]
                elif field =="accountType":
                    cust1.accountType=request.json["accountType"]
            db.session.commit()
            return make_response(jsonify({'Message' : 'Successfully updated.'}), 200)
        else:
            return make_response(jsonify({'Message' : 'Check the customer ID'}),400)
    except IntegrityError:
        return make_response(jsonify({'Message' : 'Unique constraint error'}),400)
    except KeyError:
        return make_response(jsonify({'Message' : 'Enter the field name correctly'}),400)

@app.route("/updateMultipleFields/<int:cust_id>", methods=["PUT"])
@token_required
def updateuser1(current_user,cust_id):
    try:
        app.logger.info('Inside update customer method where multiple fields get updated')
        cust_count= Customer.query.filter_by(cust_id=cust_id).count()
        cust1 = Customer.query.filter_by(cust_id=cust_id).first()
        if not cust1:
            return make_response(jsonify({'Message' : 'Customer does not exist'}),400)
        if (cust_id==current_user.cust_id):
            cust1.cust_id=request.json["cust_id"]
            cust1.name=request.json["name"]
            cust1.username=request.json["username"]
            password=request.json["password"]
            cust1.password=generate_password_hash(password, method='sha256')
            cust1.address=request.json["address"]
            cust1.state=request.json["state"]
            cust1.country=request.json["country"]
            cust1.email=request.json["email"]
            cust1.pan=request.json["pan"]
            cust1.dob=request.json["dob"]
            cust1.accountType=request.json["accountType"]
            cust1.contactNo=request.json["contactNo"]
            db.session.commit()
            return make_response(jsonify({'Message' : 'Successfully updated.'}), 200)
        else :
            return make_response(jsonify({'Message' : 'Check the customer ID'}),400)
    except IntegrityError:
        return make_response(jsonify({'Message' : 'Unique constraint error'}),400)
	



@app.route("/applyLoan", methods=["POST"])
@token_required
def applyLoan(current_user):
    app.logger.info('Inside apply loan method')
    errors =loan_schema.validate(request.json)
    if errors:
        return make_response(str(errors),400)
    
    loanType=request.json["loanType"]
    loanAmount=request.json["loanAmount"]
    date=request.json["date"]
    interest=request.json["interest"]
    duration=request.json["duration"]
    customer_id=current_user.cust_id

    try:
        loan=Loan(loanType,loanAmount,date,interest,duration,customer_id)
        db.create_all()
        db.session.add(loan)
        db.session.commit()
        return make_response(jsonify({'Message' : 'Loan applied Successfully'}), 200)
    except IntegrityError:
        return make_response(jsonify({'Message' : 'Error in Unique constraint '}), 400)
    
    

@app.route("/viewLoan/<cust_id>", methods=["GET"])
@token_required
def viewLoan(current_user,cust_id):
    app.logger.info('Inside view loan method')
    try:
        loan1 = Loan.query.filter_by(customer_id=cust_id).first()
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
