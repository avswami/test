from flask import Flask,jsonify,request,render_template
app = Flask(__name__)
table={'Veg1':'10','Veg2':'8','Veg3':'54','Veg4':'5'}

@app.route('/')
def main():
    name='Avarthana'
    return render_template('index.html',name=name)

@app.route('/groceries',methods=['GET','POST'])
def displaygroceries():
    if request.method=='GET':
        return jsonify(table)
    else:        
        table['veg']=100
        return jsonify(table) 

@app.route('/groceries/<string:name>',methods=['GET','DELETE'])
def findgrocery(name):
    if request.method=='GET':
        if name in table.keys():
            return table[name]
        else:
            return 'Grocery is not found', 404
    else:
        if name in table.keys(): #delete the item
            del table[name]
            return jsonify(table)
        else:
            return 'Grocery is not found for delete', 404
if __name__ == "__main__":
    app.run()