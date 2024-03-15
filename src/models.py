from flask_sqlalchemy import SQLAlchemy

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