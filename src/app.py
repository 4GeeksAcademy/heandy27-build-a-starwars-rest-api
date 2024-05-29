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
from models import db, User, Planets, Characters, Starships, FavoritePlanets, FavoriteCharacters, FavoriteStarships
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

#Metodos para user

@app.route('/user', methods=['GET'])
def handle_hello():

    all_users = User.query.all()
    users_serialized = []
    for user in all_users:
        users_serialized.append(user.serialize())

    print(users_serialized)

    return jsonify({"data": users_serialized}), 200

@app.route('/user', methods=['POST'])
def new_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar información en el body"}), 400
    if "email" not in body:
        return jsonify({"msg": "El campo email es obligatorio"}), 400
    if "password" not in body:
        return jsonify({"msg": "El campo password es obligatrio"}), 400
    if "is_active" not in body:
        return jsonify({"msg": "El campo is_active es obligatrio"}), 400
    
    new_user = User()
    new_user.email = body["email"]
    new_user.password = body["password"]
    new_user.is_active = body["is_active"]
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"data": new_user.serialize()}), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    single_user = User.query.get(id)
   
    if single_user is None:
        return jsonify({"msg": "El usuario con el ID: {} no existe".format(id)}), 400
    return jsonify({"data": single_user.serialize()}), 200

# Metodos para Planetas

@app.route('/planet', methods=['GET'])
def get_all_planets():
    get_planets = Planets.query.all()
    planet_serialized = []
    for planet in get_planets:
        planet_serialized.append(planet.serialize())

    print(planet_serialized)
    return jsonify({"data": planet_serialized}), 200

@app.route('/planet', methods=['POST'])
def new_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Debes enviar información en el body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo name es obligatorio"}), 400
    if "population" not in body:
        return jsonify({"msg": "El campo population es obligatorio"}), 400
    
    new_planet = Planets()
    new_planet.name = body["name"]
    new_planet.population = body["population"]
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "Nuevo planeta creado",
                    "data": new_planet.serialize()}), 201

@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    single_planet = Planets.query.get(id)
    if single_planet is None:
        return jsonify({"msg": "El planeta con el ID: {} no existe".format(id)}), 400
    return jsonify({"data": single_planet.serialize()}), 200

@app.route('/planet/<int:id>', methods=["PUT"])
def update_planet(id):
    update_planet = Planets.query.get(id)
    body = request.get_json()
    if update_planet is None:
        return jsonify({"msg": f"El id {id} planeta no fue encontrado"}), 400
    
    if "name" in body:
        update_planet.name = body["name"]
    if "population" in body:
        update_planet.population = body["population"]
    
    db.session.commit()

    return jsonify({"data": update_planet.serialize()})
    
@app.route('/planet/<int:id>', methods=["DELETE"])
def delete_planet(id):
    delete_planet = Planets.query.get(id)
    if delete_planet is None:
        return jsonify({"msg": f"El id {id} del planeta no existe"}), 400
    
    db.session.delete(delete_planet)
    db.session.commit()

    return jsonify({"msg": "El planeta se ha eliminado con exito"}), 200


# Metodos Characters

@app.route('/character', methods=['GET'])
def get_all_character():
    get_character = Characters.query.all()
    character_serialized = []
    for character in get_character:
        character_serialized.append(character.serialize())
    print(character_serialized)
    return jsonify({"data": character_serialized}), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_single_character(id):
    single_character = Characters.query.get(id)
    if single_character is None:
        return jsonify({"msg": "El character con el ID: {} no existe".format(id)}), 400
    
    return jsonify({"data": single_character.serialize()}), 200

@app.route('/character', methods=["POST"])
def new_character():
    body = request.get_json()
    if body is None:
        return jsonify({"msg": "Debes enviar información al body"}), 400
    if "name" not in body:
        return jsonify({"msg": "El campo name es obligatorio"}), 400
    if "height" not in body:
        return jsonify({"msg": "el campo height es obligatorio"}), 400
    if "gender" not in body:
        return jsonify({"msg": "el campo gender es obligatorio"}), 400
    
    new_character = Characters()
    new_character.name = body["name"]
    new_character.height = body["height"]
    new_character.gender = body["gender"]
    db.session.add(new_character)
    db.session.commit()

    return jsonify({"data": new_character.serialize()}), 201

@app.route('/character/<int:id>', methods=["DELETE"])
def delete_character(id):
    delete_character = Characters.query.get(id)
    if delete_character is None:
        return jsonify({"msg": f"El id {id} del personaje no existe"}), 400
    db.session.delete(delete_character)
    db.session.commit()

    return jsonify({"msg": "El personaje fue eliminado con exito"}), 200

@app.route('/character/<int:id>', methods=['PUT'])
def update_character(id):
    update_character = Characters.query.get(id)
    body = request.get_json()
    if update_character is None:
        return jsonify({"msg": "El character escogido con el id {id} no existe"}), 400
    
    if "name" in body:
        update_character.name = body["name"]
    if "height" in body:
        update_character.height = body["height"]
    if "gender" in body:
        update_character.gender = body["gender"]
    
    db.session.commit()

    return jsonify({"data": update_character.serialize()})

# Metodos Starships

@app.route('/starship', methods=["GET"])
def get_all_starships():
    all_starships = Starships.query.all()
    starships_serialized = []
    for starship in all_starships:
        starships_serialized.append(starship.serialize())

    print(starships_serialized)
    return jsonify({"data": starships_serialized}), 200
    
@app.route('/starship/<int:id>', methods=['GET'])
def get_single_starship(id):
    single_starship = Starships.query.get(id)
    print(single_starship.serialize())
    return jsonify({"data": single_starship.serialize()}), 200


@app.route('/starship', methods=["POST"])
def new_starship():
    body = request.get_json()
    if body is None:
        return jsonify({"msg": "El body es obligatorio"}), 400
    if "model" not in body:
        return jsonify({"msg": "El campo model es obligatorio"}), 400
    if "passengers" not in body:
        return jsonify({"msg": "El campo passengers es obligatorio"}), 400
    new_starship = Starships()
    new_starship.model = body["model"]
    new_starship.passengers = body ["passengers"]
    db.session.add(new_starship)
    db.session.commit()
    return jsonify({"data": new_starship.serialize()}), 201
    
@app.route('/starship/<int:id>', methods=["PUT"])
def update_starship(id):
    starship = Starships.query.get(id)
    body = request.get_json()
    if starship is None:
        return jsonify({"msg": f"El starship id {id} no existe"}), 400
    if "model" in body:
        starship.model = body["model"]
    if "passengers" in body:
        starship.passengers = body["passengers"]
    db.session.commit()

    return jsonify({"data": starship.serialize()}), 200

@app.route('/starship/<int:id>', methods=["DELETE"])
def delete_starship(id):
    delete_starship = Starships.query.get(id)
    if delete_starship is None:
        return jsonify({"msg": f"El starship con el id {id} no existe"}), 400
    
    db.session.delete(delete_starship)
    db.session.commit()
    
    return jsonify({"msg": "El objeto fue eliminado"}), 200
    
# Method get all favorites

@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({"msg": f"el id {id} del usuario no existe"}), 400
    
    favorites_planets = db.session.query(FavoritePlanets, Planets).join(Planets).filter(FavoritePlanets.user_id == id).all()
    favorites_planets_serialized = []
    for favorite_planet, planet in favorites_planets:
        favorites_planets_serialized.append({"favorite_planet_id": favorite_planet.id, "planet": planet.serialize()})
    

    favorite_characters = db.session.query(FavoriteCharacters, Characters).join(Characters).filter(FavoriteCharacters.user_id_2 == id).all()
    favorites_characters_serialized=[]
    for favorite_character, character in favorite_characters:
        favorites_characters_serialized.append({"favorite_character_id": favorite_character.id, "character": character.serialize()})
    
    favorite_starships = db.session.query(FavoriteStarships, Starships).join(Starships).filter(FavoriteStarships.user_id_3 == id).all()
    favorites_starships_serialized = []
    for favorite_starship, starship in favorite_starships:
        favorites_starships_serialized.append({"favorite_starship_id": favorite_starship.id, "starship": starship.serialize()})


    return jsonify({"data_planet": favorites_planets_serialized,
                    "data_character": favorites_characters_serialized,
                    "data_starship": favorites_starships_serialized}), 200

# Add and delete favorites planets

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"msg": f"El usuario con el id {user_id} no existe"}), 400
    
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"msg": f"El planeta con el id {planet_id} no existe"}), 400
    
    new_favorite_planet = FavoritePlanets(
        user_id = user_id,
        planet_id = planet_id
    )

    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify({"data": new_favorite_planet.serialize()}), 201

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    
    delete_planet = FavoritePlanets.query.filter_by(user_id = user_id, planet_id = planet_id).first()

    if delete_planet is None:
        return jsonify({"msg": "El id de user y planet son obligatorios"}), 400

    
    db.session.delete(delete_planet)
    db.session.commit()

    return jsonify({"msg": "El planeta favorito fue eliminado exitosamente"}), 200

# Add and delete favorites characters

@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"El id {user_id} del usuario no existe"}), 400
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({"msg": f"El id {character_id} del personaje no existe"}), 400
    
    new_favorite_character = FavoriteCharacters(user_id_2 = user_id, character_id=character_id)
    db.session.add(new_favorite_character)
    db.session.commit()
    return jsonify({"msg": new_favorite_character.serialize()}), 201

@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    delete_favorite_character = FavoriteCharacters.query.filter_by(user_id_2 = user_id, character_id = character_id).first()
    if delete_favorite_character is None:
        return jsonify({"msg": "El id del usuario o del personaje no existen"}), 400
    
    db.session.delete(delete_favorite_character)
    db.session.commit()

    return jsonify({"msg": "El personaje favorito fue eliminado exitosamente"}), 200

# Add and delete favorites starships

@app.route('/user/<int:user_id>/favorites/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(user_id, starship_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"El id {user_id} del usuario no existe"}), 400
    starship = User.query.get(starship_id)
    if starship is None:
        return jsonify({"msg": f"El id {starship_id} de la nave no existe"}), 400
    new_favorite_starship = FavoriteStarships(user_id_3 = user_id, starship_id = starship_id)
    db.session.add(new_favorite_starship)
    db.session.commit()
    return jsonify({"data": new_favorite_starship.serialize()}), 200

@app.route('/user/<int:user_id>/favorites/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(user_id, starship_id):
    delete_favorite_starship = FavoriteStarships.query.filter_by(user_id_3 = user_id, starship_id = starship_id).first()
    if delete_favorite_starship is None:
        return jsonify({"msg": "El id del usuario o de la nave no existe"}), 400
    
    db.session.delete(delete_favorite_starship)
    db.session.commit()

    return jsonify({"msg": "La nave favorita fue eliminada exitosamente"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
