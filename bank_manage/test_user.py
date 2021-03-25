from bank_logic import app
import jwt
import json
from unittest.mock import patch

token = None

def test_createUser_positive():
    test = app.test_client()
    response = test.post('/createCustomer',
                         json={"cust_id":"532","name": "XYZA",
                               "username": "aayz", "password": "xym123",
                               "address": "Chennai", "state": "Tamilnadu",
                               "country": "Ïndia", "email": "xmz@gmal.com",
                               "pan": "12163635", "dob": "12031345",
                               "accountType": "savings", "contactNo": "1203456787"})

    status = response.status_code
    assert status == 200
    data = response.get_data(as_text=True)
    assert data == '{"Message":"Successfully registered."}\n'


def test_createUser_with_error():
    test = app.test_client()
    response = test.post('/createCustomer',
                         json={"cust_id":"",
                               "name": "",
                               "username": "", "password": "yamin",
                               "address": "8,ahsj", "state": "Tamilnadu",
                               "country": "Ïndia", "email": "abcd@gmail.com",
                               "pan": "121636231", "dob": "12-34-3451",
                               "accountType": "savings", "contactNo": "4567819"})
    status = response.status_code
    assert status == 400

#@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
def test_login():
    test = app.test_client()
    response = test.post('/login', json={"email": "abcd@gmal.com",
                                         "password": "yamin"})
    status = response.status_code
    global token
    token = json.loads(response.get_data(as_text=True))
    print (token)
    assert status == 200


#@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
def test_update_details_contactNo():
    test = app.test_client()
    response = test.put('/updateSingleField/529/contactNo',
                        headers={"token": token},
                        json={"contactNo": "1234560987"})
    status = response.status_code
    error = response.get_data(as_text=True)
    assert error == '{"Message":"Successfully updated."}\n'
    assert status == 200


def test_update_details_id_notexist():
    test = app.test_client()
    response = test.put('/updateSingleField/2555/contactNo',
                        headers={"token": token},
                        json={"contactNo": "1234560987"})
    status = response.status_code
    error = response.get_data(as_text=True)
    assert error == '{"Message":"Customer does not exist"}\n'
    assert status == 400



def test_update_details_state():
    test = app.test_client()
    response = test.put('/updateSingleField/529/state',
                        headers={"token": token},
                        json={"state": "Kerala"})
    status = response.status_code
    error = response.get_data(as_text=True)
    assert error == '{"Message":"Successfully updated."}\n'
    assert status == 200



def test_update_details_username():
    test = app.test_client()
    response = test.put('/updateSingleField/529/username',
                        headers={"token": token},
                        json={"username": "yamu123"})
    status = response.status_code
    error = response.get_data(as_text=True)
    assert error == '{"Message":"Successfully updated."}\n'
    assert status == 200
