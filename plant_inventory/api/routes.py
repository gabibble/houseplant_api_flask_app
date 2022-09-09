from flask import Blueprint, request, jsonify 
from plant_inventory.helpers import token_required
from plant_inventory.models import User, db, Plant, plant_schema, plants_schema


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata():
    return{'some': 'value'}


#CREARE PLANT ENDPOINT
@api.route('/plants', methods = ['POST'])
@token_required
def create_plant(current_user_token):
    commom_name = request.json['common_name']
    species_name = request.json['species_name']
    size = request.json['size']
    origin = request.json['origin']
    light = request.json['light']
    shade = request.json['shade']
    soil = request.json['soil']
    fertilize = request.json['fertilize']
    user_token = current_user_token.token
    
    print(current_user_token.token)

    plant = Plant(commom_name, species_name, size, origin, light, shade, soil, fertilize, user_token=user_token)

    db.session.add(plant)
    db.session.commit()

    response = plant_schema.dump(plant)
    return jsonify(response) 

@api.route('/plants/<id>', methods = ['GET'])
@token_required
def get_plant(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        plant = Plant.query.get(id)
        response = plant_schema.dump(plant)
        return jsonify(response)
    else: 
        return jsonify({'message': 'Token is Missining!'}), 401


@api.route('/plants', methods = ['GET'])
@token_required
def get_plants(current_user_token):
    owner = current_user_token.token
    plants = Plant.query.filter_by(user_token = owner).all()
    response = plants_schema.dump(plants)
    return jsonify(response)


@api.route('/plants/<id>', methods = ['POST', 'PUT'])
@token_required
def update_plant(current_user_token, id):

    plant = Plant.query.get(id)

    plant.commom_name = request.json['common_name']
    plant.species_name = request.json['species_name']
    plant.size = request.json['size']
    plant.origin = request.json['origin']
    plant.light = request.json['light']
    plant.shade = request.json['shade']
    plant.soil = request.json['soil']
    plant.fertilize = request.json['fertilize']
    plant.user_token = current_user_token.token

    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)


@api.route('/plants/<id>', methods = ['DELETE'])
@token_required
def delete_plant(current_user_token, id):
    plant = Plant.query.get(id)
    db.session.delete(plant)
    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)