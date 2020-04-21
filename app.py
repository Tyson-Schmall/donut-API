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
    category = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(144), nullable=False)
    quantity = db.Column(db.String(8), nullable=False)

    def __init__(self, email, password, category, name, description, quantity):
        self.email = email
        self.password = password
        self.category = category
        self.name = name
        self.description = description
        self.quantity = quantity


class AdminSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "category", "name", "description", "quantity")


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

@app.route("/")
def greeting():
    return "<h2>Welcome, to your local Donut Shop!</h2>"


# Add ADMIN USER and add donut
@app.route("/create_user", methods=["POST"])
def create_user():
    email = request.json['email']
    password = request.json['password']
    category = request.json['category']
    name = request.json['name']
    description = request.json['description']
    quanity = request.json['quantity']


# Add one donut as an ADMIN USER
@app.route("/add_donut", methods=["POST"])
def add_donut():
    category = request.json['category']
    name = request.json['name']
    description = request.json['description']
    quanity = request.json['quantity']

    new_donut = Admin("category", "name", "description", "quantity")

    db.session.add(new_donut)
    db.session.commit()

    donut = Admin.query.get(new_donut.id)
    return profile_schema.jsonify(profile)


# Add multiple donuts as an ADMIN USER
@app.route("/add_donuts", methods=["POST"])
def add_donuts():
    category


@app.route("/donut/<id>". methods=["GET"])
def one_donut():
    donut = Admin.query.get(id)
    
    result = admin_schema.dump(display)
    return jsonify(result)



@app.route("/all_donuts". methods=["GET"])
def many_donuts():
    all_donuts = Admin.query.all()
    result = admins_schema.dump(all_donuts)
    return jsonify(result)



@app.route("/create_user", methods=["PATCH"])
def patch_post():



@app.route('/display/<id>', methods=['DELETE'])
def delete_donut(id):
    record = Admin.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('The selected donut has been deleted, you will need to create a new post if you wish to have it display again.')




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



    
    
