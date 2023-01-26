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
from models import db, Usuario, Vehiculos, Planetas, Personajes, Favoritos


# ACA ARRIBA IMPORTE LOS DEMAS QUE FALTABAN

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
    


@app.route('/personajes', methods=['GET'])
def handle_personajes():
    allpersonajes = Personajes.query.all()
    results = list(map(lambda item: item.serialize(),allpersonajes))
    print(results)
    return jsonify(results), 200


#obteniendo info de un solo personaje
@app.route('/personajes/<int:user_id>', methods=['GET'])
def get_info_personajes(personajes_id):
    
    personajes = Personajes.query.filter_by(id=personajes_id).first()
    return jsonify(personajes.serialize()), 200



# ___________


@app.route('/planetas', methods=['GET'])
def handle_planetas():
    allplanetas = Planetas.query.all()
    results = list(map(lambda item: item.serialize(),allplanetas))
    print(results)
    return jsonify(results), 200


#obteniendo info de un solo planeta
@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def get_info_planetas(planetas_id):
    
    planetas = Planetas.query.filter_by(id=planetas_id).first()
    return jsonify(planetas.serialize()), 200

# _____________



@app.route('/usuario', methods=['GET'])
def handle_usuario():
    allusuario = Usuario.query.all()
    results = list(map(lambda item: item.serialize(),allusuario))
    print(results)
    return jsonify(results), 200


#obteniendo info de un solo usuario
@app.route('/usurio/<int:user_id>', methods=['GET'])
def get_info_user(usuario_id):
    
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    return jsonify(usuario.serialize()), 200




@app.route('/usuario/favoritos', methods=['GET'])
def handle_usuario_favoritos():
    allusuario = Usuario.query.all()
    results = list(map(lambda item: item.serialize(),allusuario_favoritos))
    print(results)
    return jsonify(results), 200


#obteniendo favs de un usuario

@app.route('/usuario/<int:usuario_id>/favoritos/', methods=['GET'])
def get_favoritos_usuario(usuario_id):
    
    usuario_favoritos = Favoritos.query.filter_by(usuario_id=usuario_id).all()
    results = list(map(lambda item: item.serialize(),usuario_favoritos))
    print(results)
    return jsonify(results), 200


# POST:

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_todo(usuario_id,planetas_id):
    añadir_planetas_a_favoritos = Favoritos.query.filter_by(planetas_id=planetas_id).first().all()
    results = list(map(lambda item: item.serialize(),añadir_planetas_a_favoritos))
    return jsonify(results)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
