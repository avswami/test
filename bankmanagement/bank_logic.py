from flask import Flask
from flask import request, jsonify, make_response
import jwt
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from model_schema import LoanSchema, db, app
from model_schema import Customer, Loan, CustomerSchema




app.config['SECRET_KEY'] = 'AV'

customer_schema = CustomerSchema()
loan_schema = LoanSchema()


@app.route('/createCustomer', methods=['POST'])
def signup():
    errors = customer_schema.validate(request.json)
    if errors:
        return make_response(str(errors), 400)
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
            cust = Customer(name, username, hash_pass, address, state, country, email, pan, dob, accountType, contactNo)
            db.create_all()
            db.session.add(cust)
            db.session.commit()
            return make_response('Successfully registered.', 201)
        else:
            return make_response('Customer already exists.Please Log in.', 202)
    except IntegrityError:
        return make_response("Error in Unique constraint ", 400)


@app.route('/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]

    if not email or not password:
        return make_response('Enter the username and password', 401)

    cust = Customer.query.filter_by(email=email).first()
    if not cust:
        return make_response('User does not exist', 402)

    if check_password_hash(cust.password, password):
        # generates the JWT Token
        token = jwt.encode({'username': cust.username, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return make_response(jsonify(token.decode('UTF-8')), 201)

    return make_response('Incorrect password', 403)


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'token' in request.headers:
            token = request.headers['token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 402

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = Customer.query.filter_by(username=data['username']).first()
            print("token valid")
        except Exception:
            return jsonify({'message' : 'Token is invalid !!'}),403
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/viewCustomer/<int:id>", methods=["GET"])
@token_required
def viewuser(current_user,id):
    cust1 = Customer.query.get(id)
    if not cust1:
        return make_response("Customer not exist",400)
    if(id==current_user.id):
        return customer_schema.dump(cust1)
    else:
        return make_response("Check customer id",401)


@app.route("/updateCustomer/<int:id>/<field>", methods=["PUT"])
@token_required
def updateuser(current_user,id,field):
    try:
        cust1 = Customer.query.get(id)
        if not cust1:
            return make_response("Customer not exist",400)
        if(id==current_user.id):
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
            return "Updated Successfully"
        else:
            return make_response("Check the customer ID",401)
    except IntegrityError:
        return make_response("Unique constraint error",400)
    except KeyError:
        return make_response("Enter the field name correctly",403)


@app.route("/applyLoan", methods=["POST"])
@token_required
def applyLoan(current_user):
    errors =loan_schema.validate(request.json)
    if errors:
        return make_response(str(errors),400)
    loanType=request.json["loanType"]
    loanAmount=request.json["loanAmount"]
    date=request.json["date"]
    interest=request.json["interest"]
    duration=request.json["duration"]
    customer_id=current_user.id

    loan=Loan(loanType,loanAmount,date,interest,duration,customer_id)
    db.create_all()
    db.session.add(loan)
    db.session.commit()
    return "Loan applied Successfully"


@app.route("/viewLoan/<id>", methods=["GET"])
@token_required
def viewLoan(current_user,id):
    loan1 = Loan.query.get(id)
    if not loan1:
        return make_response("Loan id not exist", 400)
    elif(loan1.customer_id==current_user.id):
        return loan_schema.dump(loan1)
    else:
        return make_response("Check your Loan ID", 401)


db.create_all()
if __name__ == "__main__": 
	app.run(debug = True) 
