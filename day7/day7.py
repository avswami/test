from flask import Flask, jsonify, request
from flask_restful import Api,Resource,abort
import json,ast

app = Flask(__name__)
api = Api(app)
veggies = [
	{ 
	'Veggy' :'potato', 
	'Quantity':12
	},
{ 
	'Veggy' : 'tomato', 
	'Quantity': 18
	}
]

#task_post_args = reqparse.RequestParser()
#task_post_args.add_argument{'Veggy', type=str, help='Veggy is required', required=True}
#task_post_args.add_argument{'Quantity', type=int, help='Quantity is required', required=True}


def abort_if_veg_doesnt_exist(name):
    count=0
    #print("Veggies:" +str(veggies))
    #veggies1 = ast.literal_eval(json.dumps(veggies))
    #print("Veggies:" +str(veggies1))
    for veg in veggies:
        print (name,veg['Veggy'])
        if name in veg['Veggy']:
            count=1
            break
    if count == 0:
        abort(404, message="The Veggy {} does nott exist".format(name))

class Vegetable(Resource):
    def get(self):
        return jsonify(veggies)
    def post(self):
        #args = task_post_args.parse.args()
        dic = {}
        dic['Veggy'] = request.json['Veggy']
        dic['Quantity'] = request.json['Quantity']
        veggies.append(dic)
        #veggies = ast.literal_eval(json.dumps(veggies))
        #print("Veggies:" +jsonify(veggies))
        return veggies
class Vegwitharg(Resource):
    def get(self,name):
        abort_if_veg_doesnt_exist(name)
        for veg in veggies:
            if name == veg['Veggy']:
                print (name,veg['Veggy'])
                
                return veg
    def delete(self,name):
        abort_if_veg_doesnt_exist(name)
        count=0
        for veg in veggies:
            if name == veg['Veggy']:
                veggies.pop(count) 
                break
            count = count+1   
        return veg
    def put(self,name):
        print("Veggies:" +str(veggies))
        veggies1 = ast.literal_eval(json.dumps(veggies))
        print("Veggies:" +str(veggies1))
        abort_if_veg_doesnt_exist(name)
        for veg in veggies:           
            print("Veggies:" +str(veggies1))
            if name == veg["Veggy"]:
                veg['Quantity'] = 25
                break        
        return veg
api.add_resource(Vegetable,'/vegetableslist')
api.add_resource(Vegwitharg,'/vegetableslist/<string:name>')
