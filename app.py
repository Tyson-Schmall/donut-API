from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import os







app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


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


class Donut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(144), nullable=False)
    quantity = db.Column(db.String(8), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)


    def __init__(self, category, name, description, quantity,img_url):
        self.category = category
        self.name = name
        self.description = description
        self.quantity = quantity
        self.img_url = img_url

class DonutSchema(ma.Schema):
    class Meta:
        fields = ("id","category", "name", "description", "quantity", "img_url")

donut_schema = DonutSchema()
donuts_schema = DonutSchema(many=True)




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
    quantity = request.json['quantity']


# Add one donut as an ADMIN USER
@app.route("/add_donut", methods=["POST"])
def add_donut():
    category = request.json['category']
    name = request.json['name']
    description = request.json['description']
    quantity = request.json['quantity']
    img_url = request.json['img_url']

    new_donut = Donut(category, name, description, quantity, img_url)

    db.session.add(new_donut)
    db.session.commit()

    donut = Donut.query.get(new_donut.id)
    return donut_schema.jsonify(donut)


# # Add multiple donuts as an ADMIN USER
# @app.route("/add_donuts", methods=["POST"])
# def add_donuts():
#     category


@app.route("/donut/<id>", methods=["GET"])
def one_donut():
    donut = Donut.query.get(id)
    
    result = donut_schema.dump(display)
    return jsonify(result)



@app.route("/all_donuts", methods=["GET"])
def many_donuts():
    all_donuts = Donut.query.all()
    result = donuts_schema.dump(all_donuts)
    return jsonify(result)



# @app.route("/create_user", methods=["PATCH"])
# def patch_post():



@app.route('/display/<id>', methods=['DELETE'])
def delete_donut(id):
    record = Admin.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('The selected donut has been deleted, you will need to create a new post if you wish to have it display again.')

@app.route('/donut/<id>', methods=["PATCH"])
def update_img(id):
    donut = Donut.query.get(id)

    new_img = request.json['img_url']

    donut.img_url = new_img

    db.session.commit()
    return donut_schema.jsonify(donut)


if __name__ == "__main__":
    app.debug = True
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



    
    
# https://scontent-den4-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/p750x750/22221334_120961335268425_8160340611455516672_n.jpg?_nc_ht=scontent-den4-1.cdninstagram.com&_nc_cat=109&_nc_ohc=oqWosOnkQ6kAX8yrvIb&oh=9549ec6c107f1d25a69471b7959d918d&oe=5ECBDB0B