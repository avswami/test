from loan_logic import app
import jwt
import json
from unittest.mock import patch

test = app.test_client()
token = None


def test_login():
	#test = app.test_client()
	response = test.post('/login', json={"email": "s9@gmail.com",
										 "password": "swami1234"})
	status = response.status_code
	global token
	token = json.loads(response.data)['token']
	print (token)
	assert status == 200


def test_applyLoan_positive():
	#test = app.test_client()
	response = test.post('/applyLoan',
	                     headers={"token": token},
						 json={ "loan_id": "102",
								 "loanType": "Personal",
								 "loanAmount": "400000",
								 "date": "15022021",
								 "interest": "4",
								 "duration": "2"})

	status = response.status_code
	assert status == 200
	data = response.get_data(as_text=True)
	assert data == '{"Message":"Loan applied Successfully"}\n'


def test_applyLoan_with_error():
	#test = app.test_client()
	response = test.post('/applyLoan',
	                     headers={"token": token},
						 json={"loan_id": "",
								 "loanType": "",
								 "loanAmount": "400000",
								 "date": "15022021",
								 "interest": "4",
								 "duration": "2"})
	status = response.status_code
	assert status == 400

#@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')

#@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
def test_viewLoan():
	#test = app.test_client()
	response = test.get('/viewLoan/101',
						headers={"token": token})
	status = response.status_code
	error = response.get_data(as_text=True)
	assert status == 200

def test_viewLoan_withError():
	#test = app.test_client()
	response = test.get('/viewLoan/1001',
						headers={"token": token})
	status = response.status_code
	error = response.get_data(as_text=True)
	assert status == 400


