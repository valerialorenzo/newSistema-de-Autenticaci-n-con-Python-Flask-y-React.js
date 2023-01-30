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
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


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

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

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
@app.route('/personajes/<int:usuario_id>', methods=['GET'])
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
@app.route('/usurio/<int:usuario_id>', methods=['GET'])
def get_info_usuario(usuario_id):
    
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

# POSTs
@app.route('/usuario/<int:usuario_id>/favoritos/planetas', methods=['POST'])
def add_new_favourite_planet(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    new_favorito = Favoritos(usuario_id=usuario_id, planetas_id=request_body["planetas_id"])
    db.session.add(new_favorito)
    db.session.commit()
    usuario = Favoritos.query.filter_by(usuario_id=usuario_id).first()
    print(usuario)
    return jsonify(request_body),200

@app.route('/usuario/<int:usuario_id>/favoritos/personajes', methods=['POST'])
def add_new_favourite_personajes(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    new_favorito = Favoritos(usuario_id=usuario_id, personajes_id=request_body["personajes_id"])
    db.session.add(new_favorito)
    db.session.commit()
    usuario = Favoritos.query.filter_by(usuario_id=usuario_id).first()
    print(usuario)
    return jsonify(request_body),200


# DELETEs

@app.route('/usuario/<int:usuario_id>/favoritos/planetas', methods=['DELETE'])
def eliminar_planeta_favorito(usuario_id):
    request_body=request.json
    print(request_body)
    print(usuario_id)
    query= Favoritos.query.filter_by(usuario_id=usuario_id,planetas_id=request_body["planeta_id"]).first()
    print(query)
    if query is None:
        return jsonify({"msg":"No hubo coincidencias, no hay nada para eliminar"}),404
    db.session.delete(query)
    db.session.commit() 
    return jsonify({"msg":"El favorito ha sido eliminado correctamente"}),200
    # segundo delete

@app.route('/usuario/<int:usuario_id>/favoritos/personajes', methods=['DELETE'])
def eliminar_personajes_favorito(usuario_id):
    request_body=request.json
    print(request_body)
    print(usuario_id)
    query= Favoritos.query.filter_by(usuario_id=usuario_id,personajes_id=request_body["personajes_id"]).first()
    print(query)
    if query is None:
        return jsonify({"msg":"No hubo coincidencias, no hay nada para eliminar"}),404
    db.session.delete(query)
    db.session.commit() 
    return jsonify({"msg":"El favorito ha sido eliminado correctamente"}),200


# ________

@app.route('/register', methods=['POST'])
def add_new_user():

    request_body=request.json

    usuario=Usuario.query.filter_by(mail =request_body ["mail"]).first() 

    if usuario is None:
        new_user= Usuario (mail =request_body ["mail"], contraseña= request_body ["contraseña"], nombre= request_body ["nombre"])
        db.session.add(new_user)
        db.session.commit() 

        return jsonify({"usuario":new_user.serialize()}), 200
    return jsonify ("usuario existente"), 400


@app.route("/login", methods=["POST"])
def login():

    mail=request.json.get("mail",None)
    contraseña=request.json.get("contraseña",None)

    usuario= Usuario.query.filter_by(mail=mail).first()
    if usuario is None: 
        return jsonify({"msg":"Usuario inexistente"}), 404
    if contraseña != usuario.contraseña:
        return jsonify({"msg":"Usuario o contraseña incorrecto"}), 401

    access_token = create_access_token(identity=mail)
    return jsonify(access_token=access_token)
    # return jsonify({"msg":"Usuario o contraseña incorrecto"}), 401
    
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
