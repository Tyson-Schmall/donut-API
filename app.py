from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Admin(db.Model):
    __tablename__ = "Inventory"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(16), nullable=False)


    def __init__(self, email, password):
        self.email = email
        self.password = password


class Donut(db.Model):
    __tablename__ = "Donuts"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(144), nullable=False)
    quantity = db.Column(db.String(8), nullable=False)

    def __init__(self, category, name, description, quantity):
        self.category = category
        self.name = name
        self.description = description
        self.quantity = quantity


class AdminSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password")


class DonutSchema(ma.Schema):
    class Meta:
        fields = ("id", "category", "name", "description", "quantity")


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

donut_schema = DonutSchema()
donuts_schema = DonutSchema(many=True)

@app.route("/", methods=["GET"])
def greeting():
    return "<h2>Welcome, to your local Donut Shop!</h2>"


# Add ADMIN USER and add donut
@app.route("/create_user", methods=["POST"])
def create_user():
    email = request.json['email']
    password = request.json['password']
    
    new_admin = Admin("email", "password")

    db.session.add(new_admin)
    db.session.commit()

    admin = Admin.query.get(new_admin.id)
    return admin_schema.jsonify(admin)


# Add one donut as an ADMIN USER
@app.route("/add_donut", methods=["POST"])
def add_donut():
    category = request.json['category']
    name = request.json['name']
    description = request.json['description']
    quantity = request.json['quantity']

    new_donut = Donut("category", "name", "description", "quantity")

    db.session.add(new_donut)
    db.session.commit()

    donut = Donut.query.get(new_donut.id)
    return donut_schema.jsonify(donut)

# GET route for ALL DONUTS
@app.route("/all_donuts", methods=["GET"])
def many_donuts():
    all_donuts = Donut.query.all()
    result = donuts_schema.dump(all_donuts)
    return jsonify(result)


# GET route for ONE DONUT
@app.route("/donut/<id>", methods=["GET"])
def one_donut(id):
    donut = Donut.query.get(id)
    
    result = donut_schema.dump(donut)
    return jsonify(result)


# Route for MODIFYING a POST
@app.route("/add_donut/<id>", methods=["PATCH"])
def patch_donut(id):
    donut = Donut.query.get(id)
    
    new_category = request.json["category"]
    new_name = request.json["name"]
    new_description = request.json["description"]
    new_quantity = request.json["quantity"]

    donut.category = new_category
    donut.name = new_name
    donut.description = new_description
    donut.quantity = new_quantity

    db.session.commit()
    return donut_schema.jsonify(donut)


# Route for DELETING a DONUT
@app.route('/remove_donut/<id>', methods=["DELETE"])
def delete_donut(id):
    record = Donut.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("The selected donut has been deleted, it is no longer in the database.")


if __name__ == "__main__":
    app.run(debug = True)
    app.run()




# class User(db.Model):
#     __tablename__ = "Review"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(32), nullable=False)
#     password = db.Column(db.String(16), nullable=False)
#     rating = db.Column(db.String(24), nullable=False)
#     title = db.Column(db.String(24), nullable=False)
#     description = db.Column(db.String(144), nullable=False)

#     def __init__(self, email, password, rating, title, description):
#         self.email = email
#         self.password = password
#         self.rating = rating
#         self.title = title
#         self.description = description



# class UserSchema(ma.Schema):
    # class Meta:
    #     fields = ("id", "email", "password", "rating", "title", "description")



# user_schema = UserSchema()
# users_schema = UserSchema(many=True)



    
    
