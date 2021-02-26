from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
#from marshmallow_sqlalchemy import a


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Grocery_list(db.Model):
    Grocery_id = db.Column(db.Integer, primary_key=True)
    veggy_name = db.Column(db.String(80), unique=True, nullable=False)
    veggy_qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Grocery %r>' % self.veggy_name

class GrocerySchema(ma.Schema):
   class Meta:
      fields=("Grocery_id","veggy_name","veggy_qty")
      #load_instance = True
    
   #Grocery_id = ma.auto_field()
   #veggy_name = ma.auto_field()
   #veggy_qty = ma.auto_field()

db.create_all()
grocery_schema = GrocerySchema()
obj1 = Grocery_list(veggy_name = "Potato", veggy_qty = 10)
obj2 = Grocery_list(veggy_name = "Tomato", veggy_qty = 20)
result=Grocery_list.query.filter_by(veggy_name=obj1.veggy_name).first()

if result:
   print("item already present")  
else:
   db.session.add(obj1)
   db.session.add(obj2)
   db.session.commit()

dump1=grocery_schema.dump(obj1)
print(result)
print(dump1)
print(grocery_schema.dump(obj2))
print(Grocery_list.query.all())