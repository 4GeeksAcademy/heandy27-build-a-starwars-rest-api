from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return 'Usuario con email: {}'.format(self.email)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    planet_id_relationship = db.relationship("FavoritePlanets", cascade="all, delete-orphan", backref="planet")

    def __repr__(self):
        return f"Planeta {self.id} {self.name} con una población de {self.population}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population
        }
    
class Characters(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    character_id_relationship = db.relationship("FavoriteCharacters", cascade="all, delete-orphan", backref="character")


    def __repr__(self):
        return f"Character {self.name} {self.height} {self.gender}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender
        }
    
class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), unique=True, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    starship_id_relationship = db.relationship("FavoriteStarships", cascade="all, delete-orphan", backref="starship")

    
    def __repr__(self):
        return f"Starships {self.model} {self.passengers}"
    
    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "passengers": self.passengers
        }
    
class FavoritePlanets(db.Model):
    __tablename__ = "favorite_planets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_relationship = db.relationship("User", foreign_keys=[user_id])
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
   

    def __repr__(self):
        return f"Al usuario {self.user_id} le gusta el planeta {self.planet_id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
    
class FavoriteCharacters(db.Model):
    __tablename__ = "favorite_characters"
    id = db.Column(db.Integer, primary_key=True)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_relationship_2 = db.relationship("User", foreign_keys=[user_id_2])
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    def __repr__(self):
        return f"Al usuario {self.user_id_2} le gusta el personaje {self.character_id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id_2": self.user_id_2,
            "character_id": self.character_id
        }

class FavoriteStarships(db.Model):
    __tablename__ = "favorite_starships"
    id = db.Column(db.Integer, primary_key=True)
    user_id_3 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_relationship_3 = db.relationship("User", foreign_keys=[user_id_3])
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.id'), nullable=False)

    def __repr__(self):
        return f"Al usuario {self.user_id_3} le gusta la nave {self.starship_id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id_3": self.user_id_3,
            "starship_id": self.starship_id
        }


 