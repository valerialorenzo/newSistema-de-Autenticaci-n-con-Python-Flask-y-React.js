from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "mail": self.email,
            # do not serialize the password, its a security breach
        # }

# Modificamos nuestras tablas en base al ejemplo que nos dan:

# TABLA USUARIO:
class Usuario(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    constraseña= db.Column (db.String (20))
    mail= db.Column (db.String (100))
    favoritos_usuario = db.relationship('Favoritos', backref='usuario', lazy=True)


    def __repr__(self):
        return '<Usuario %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "mail": self.mail,

            # "contraseña": self.constraseña,
            # do not serialize the password, its a security breach
        }

# TABLA PERSONAJES:
    
class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    genero = db.Column(db.String(250))
    altura = db.Column(db.String(250))
    favoritos_personajes = db.relationship('Favoritos', backref='personajes', lazy=True)


    def __repr__(self):
        return '<Personajes %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "genero": self.genero,
            "altura": self.altura,
            # do not serialize the password, its a security breach
        }
# TABLA VEHICULOS:

class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    capacidad = db.Column(db.String(250))
    creacion = db.Column(db.String(250))
    modelo = db.Column(db.String(250))
    favoritos_vehiculos = db.relationship('Favoritos', backref='vehiculos', lazy=True)


    def __repr__(self):
        return '<Vehiculos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre":self.nombre,
            "capacidad": self.capacidad,
            "creacion": self.creacion,

            # do not serialize the password, its a security breach
        }
# TABLA PLANETAS:
class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    poblacion = db.Column(db.String(250))
    terreno = db.Column(db.String(250))
    favoritos_planetas = db.relationship('Favoritos', backref='planetas', lazy=True)

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre":self.nombre,
            "poblacion": self.poblacion,
            "terreno": self.terreno,

            # do not serialize the password, its a security breach
        }
# TABLA FAVORITOS:
class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    usuario_id = db.Column (db.Integer, db.ForeignKey('usuario.id'))
    personajes_id = db.Column (db.Integer, db.ForeignKey('personajes.id'))
    vehiculos_id = db.Column (db.Integer, db.ForeignKey('vehiculos.id'))
    planetas_id = db.Column (db.Integer, db.ForeignKey('planetas.id'))
    # planetas_id = db.Column (db.Integer, ForeignKey('planetas.id'))
    # planetas = relationship (Planetas)
    # vehiculos_id = db.Column (db.Integer, ForeignKey('vehiculos.id'))
    # personajes_id = db.Column (db.Integer, ForeignKey('personajes.id'))
    # vehiculos = relationship (Vehiculos)
    # personajes = relationship (Personajes)
    # usuario = relationship (Usuario)

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
    
            # do not serialize the password, its a security breach
        }