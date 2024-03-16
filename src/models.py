from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"Usuario con id {self.id} y email {self.email}"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    population = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "Planeta {} de nombre {} ".format(self.id, self.name)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
        }

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)

    def __repr__(self):
        return f"Persona con id {self.id}, nombre {self.name}, altura {self.height} y peso {self.height}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass
        }
    
class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(30))

    def __repr__(self):
        return f"Nave con id {self.id}, nombre {self.name} y modelo {self.model}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model
        }
    
class FavoriteCharacters(db.Model):
    __tablename__ = "favorite-characters"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relationship = relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    character_relationship = relationship(People)

    def __repr__(self):
        return f"Personaje favorito con id {self.id} y nombre {self.character_relationship.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.character_relationship.name,
        }
    
class FavoritePlanets(db.Model):
    __tablename__ = "favorite-planets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relationship = relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    planet_relationship = relationship(Planets)

    def __repr__(self):
        return f"Planeta favorito con id {self.id} y nombre {self.planet_relationship.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.planet_relationship.name,
        }

class FavoriteStarships(db.Model):
    __tablename__ = "favorite-starships"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relationship = relationship(User)
    starship_id = db.Column(db.Integer, db.ForeignKey("starships.id"))
    starship_relationship = relationship(Starships)

    def __repr__(self):
        return f"Nave favorita con id {self.id} y nombre {self.starship_relationship.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.starship_relationship.name,
        }

class UserFavorites(db.Model):
    __tablename__ = "user-favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    favorite_starship_id = db.Column(db.Integer, db.ForeignKey("favorite-starships.id"))
    favorite_starship_relationship = relationship("FavoriteStarships")
    favorite_planet_id = db.Column(db.Integer, db.ForeignKey("favorite-planets.id"))
    favorite_planet_relationship = relationship("FavoritePlanets")
    favorite_character_id = db.Column(db.Integer, db.ForeignKey("favorite-characters.id"))
    favorite_character_relationship = relationship("FavoriteCharacters")

    def __repr__(self):
        return f"Usuario con id {self.id}"

    def serialize(self):
        return {
            "id": self.id,
        }
    