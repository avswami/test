from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow.validate import Length,Range
from flask_marshmallow import Marshmallow

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app) 
ma = Marshmallow(app)


class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cust_id=db.Column(db.Integer, unique=True)
	name = db.Column(db.String(255))
	username = db.Column(db.String(255),unique = True)
	password = db.Column(db.String(255))
	address = db.Column(db.String(255))
	state = db.Column(db.String(255))
	country = db.Column(db.String(255))
	email = db.Column(db.String(255),unique = True)
	pan = db.Column(db.String(255),unique = True)
	dob = db.Column(db.String(255))
	accountType = db.Column(db.String(255))
	contactNo = db.Column(db.String(255),unique = True)

	def __init__(self, cust_id, name, username, password,address,state,country,email,pan,dob,accountType,contactNo):
		self.cust_id = cust_id
		self.name = name
		self.username = username
		self.password = password
		self.address = address
		self.state = state
		self.country = country
		self.email = email
		self.pan = pan
		self.dob = dob
		self.accountType=accountType
		self.contactNo=contactNo


class CustomerSchema(ma.SQLAlchemySchema):

	name = fields.Str(required = True, validate = Length(min=3,max=10))
	cust_id = fields.Integer(required = True, validate = Range(min=3))
	username = fields.Str(required = True, validate = Length(min=3,max=10))
	password = fields.Str(required = True, validate = Length(min=3,max=10))
	address = fields.Str(required = True, validate = Length(min=3,max=10))
	state = fields.Str(required = True, validate = Length(min=3,max=10))
	country = fields.Str(required = True, validate = Length(min=3,max=10))
	email = fields.Email(required=True,validate=Length(min=1))
	pan = fields.Str(required = True, validate = Length(min=5))
	dob = fields.Str(required = True, validate = Length(min=3,max=10))
	accountType = fields.Str(required = True, validate = Length(min=3,max=10))
	contactNo = fields.Str(required = True,validate = Length(min=10))

	class Meta:
		fields = ("id", "cust_id", "name", "password","username","address", "state", "country","email","pan","dob","accountType","contactNo")
		

class CustomerupdateSchema(ma.SQLAlchemySchema):
	password = fields.Str(required = True, validate = Length(min=3,max=10))
	address = fields.Str(required = True, validate = Length(min=3,max=10))
	state = fields.Str(required = True, validate = Length(min=3,max=10))
	country = fields.Str(required = True, validate = Length(min=3,max=10))
	email = fields.Email(required=True,validate=Length(min=1))
	contactNo = fields.Str(required = True,validate = Length(min=10))

	class Meta:
		fields = ("id", "cust_id", "name", "password","username","address", "state", "country","email","pan","dob","accountType","contactNo")


class Loan(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	loan_id=db.Column(db.Integer, unique=True)
	loanType=db.Column(db.String(255))
	loanAmount=db.Column(db.String(255))
	date=db.Column(db.String(255))
	interest=db.Column(db.Integer)
	duration=db.Column(db.String(255))
	customer_id = db.Column(db.Integer, db.ForeignKey("customer.cust_id"))

	def __init__(self, loan_id, loanType, loanAmount,date,interest,duration,customer_id):
		self.loan_id = loan_id
		self.loanType = loanType
		self.loanAmount = loanAmount
		self.date = date
		self.interest = interest
		self.duration = duration
		self.customer_id = customer_id

class LoanSchema(ma.SQLAlchemyAutoSchema):
	loan_id = fields.Integer(required = True, validate = Range(min=3))
	loanType = fields.Str(required = True, validate = Length(min=3,max=10))
	loanAmount = fields.Integer(required = True, validate = Range(min=1))
	date = fields.Str(required = True, validate = Length(min=3,max=10))
	interest = fields.Integer(required = True, validate = Range(min=0,max=100))
	duration = fields.Integer(required=True, validate= Range(min=1))
	class Meta:
		fields = ("id", "loan_id", "loanType", "loanAmount","date", "interest", "duration","customer_id")

db.create_all()