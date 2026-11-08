from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db= SQLAlchemy(app)

# Create a database model (table) named Drink
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.name} - {self.description}"
    

# GET API: Retrieve all drink records from the database
@app.route('/drinks')
def get_drinks():
    drinks= Drink.query.all()

    output= []
    for drink in drinks:
        drink_data = {'name':drink.name, 
                      'description':drink.description}

        output.append(drink_data)
    return {"drinks":output}


# GET API: Retrieve a specific drink using its ID
@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {'name':drink.name ,
                    'dscription':drink.description}


# POST API: Add a new drink to the database
@app.route('/drinks', methods=['POST'])
def add_drink():
    drink= Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}


# PUT API: update a drink using its ID
@app.route('/drinks/<int:id>', methods=['PUT'])
def put_drink(id):

    drink = Drink.query.get_or_404(id)

    data = request.get_json()

    drink.name = data['name']
    drink.description = data['description']

    db.session.commit()

    return {
        'message': 'Drink updated successfully',
        'id': drink.id,
        'name': drink.name,
        'description': drink.description
    }, 200

# PATCH API: update a drink using its ID
@app.route('/drinks/<int:id>', methods=['PATCH'])
def patch_drink(id):

    drink = Drink.query.get_or_404(id)

    data = request.get_json()

    drink.name = data['name']
    drink.description = data['description']

    db.session.commit()

    return {
        'message': 'Drink updated successfully',
        'id': drink.id,
        'name': drink.name,
        'description': drink.description
    }, 200


# GET API: Retrieve all drinks along with their IDs
@app.route('/')
def index():
    drinks = Drink.query.all()

    output=[]
    for drink in drinks:
        drink_data= {
            'id':drink.id,
            'name':drink.name,
            'description':drink.description
        }

        output.append(drink_data)

    return{'drinks':output}