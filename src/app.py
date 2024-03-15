"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import db, Planets
from models import db, People
from models import db, Starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all()
    users_serialized_map = list(map(lambda x: x.serialize(), users))
    response_body = {
        "msg": "ok",
        "result": users_serialized_map
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_serialized_map = list(map(lambda x: x.serialize(), planets))
    response_body = {
        "msg": "ok",
        "result": planets_serialized_map
    }
    return jsonify(response_body), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planets(id):
    planet = Planets.query.get(id)
    return jsonify({"msg": "ok", "planet": planet.serialize()}), 200

@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify()
    if "name" not in body:
        return jsonify()
    new_planet = Planets()
    new_planet.name = body["name"]
    new_planet.population = body["population"]
    db.session.add(new_planet)
    db.session.commit()
    return jsonify("Planeta añadido"), 200

@app.route('/people', methods=['POST'])
def add_person():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify()
    if "name" not in body:
        return jsonify()
    new_person = People()
    new_person.name = body["name"]
    new_person.height = body["height"]
    new_person.mass = body["mass"]
    db.session.add(new_person)
    db.session.commit()
    return jsonify("Persona añadida"), 200

@app.route('/starships', methods=['POST'])
def add_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify()
    if "name" not in body:
        return jsonify()
    new_starship = Starships()
    new_starship.name = body["name"]
    new_starship.model = body["model"]
    db.session.add(new_starship)
    db.session.commit()
    return jsonify("Nave añadida"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
