from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Initialize app
app = Flask(__name__)
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/brand'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)

# Initialize Database
db = SQLAlchemy(app)
# initialize Marshmallow
ma = Marshmallow(app)


# table
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(200),
                      index=False,
                      unique=True,
                      nullable=False)
    description = db.Column(db.String(200),
                            index=False,
                            unique=True,
                            nullable=False)
    created_by = db.Column(db.String(200),
                           index=False,
                           unique=True,
                           nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, brand, description, created_by, created_at):
        self.brand = brand
        self.description = description
        self.created_by = created_by
        self.created_at = created_at


# Marshmallow Schema
class BrandSchema(ma.Schema):
    class Meta:
        fields = ('id', 'brand', 'description', 'created_by')


# Initialize schema
brand_schema = BrandSchema()
brands_schema = BrandSchema(many=True)


@app.route("/")
def index():
    return render_template("brand_form.html")


# Create a brand
@app.route('/brand', methods=['POST'])
def add_brand():
    # get data from request
    brand = request.form['brand']
    description = request.form['description']
    created_by = request.form['created_by']
    created_at = datetime.now()
    # Instantiate new brand
    new_brand = Brand(brand, description, created_by, created_at)
    db.session.add(new_brand)  # Adds new brand record to database
    db.session.commit()  # Commits all changes
    return brand_schema.jsonify(new_brand)


# get all brands
@app.route('/brands', methods=['GET'])
def get_brands():
    brands = Brand.query.all()
    result = brands_schema.dump(brands)
    return jsonify(result)


# Put and Delete a specific brand. (you can do this like you done for post and get request but here i am doing to
# show you how to handle multiple methods)
@app.route('/brand/<int:id>', methods=['PUT', 'DELETE'])
def put_delete(id):
    if request.method == 'PUT':
        brand = Brand.query.get(id)
        brand.brand = request.json['brand']
        brand.description = request.json['description']
        brand.created_by = request.json['created_by']
        return {'message': 'data updated'}

    if request.method == 'DELETE':
        brand = Brand.query.get(id)
        db.session.delete(brand)
        db.session.commit()
        return {'message': 'data deleted successfully'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
