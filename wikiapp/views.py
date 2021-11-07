import datetime
import sys

from flask import jsonify, request, abort

from wikiapp import app, error_handler
from wikiapp.models import Continent, setup_db, db

setup_db(app)


@app.route('/api/wiki/continents', methods=['GET'])
def get_continents():
    continents_list = []
    continents = Continent.query.all()
    for continent in continents:
        continent_json_data = {
            "id": continent.id,
            "name": continent.name,
            "population": continent.population,
            "area": continent.area_in_sq_meters
        }
        continents_list.append(continent_json_data)
    return jsonify({
        "status_code": 200,
        "continents": continents_list,
    })


@app.route('/api/wiki/continents', methods=['POST'])
def create_a_continent():
    body = request.get_json()
    name = body.get("name")
    population = body.get("population")
    print(population)
    area = body.get("area")
    continent = Continent(name=name, population=population, area_in_sq_meters=area)
    continent.insert()
    return jsonify({
        "status_code": 200,
        "message": f"{name} continent created."
    })


@app.route('/api/wiki/continents/<int:id>', methods=['PUT'])
def update_a_continent(id):
    body = request.get_json()
    name = body.get("name")
    population = body.get("population")
    area = body.get("area")
    # continent = Continent.query.get(id)
    continent = Continent.query.filter(Continent.id == id).one_or_none()
    if continent is None:
        print(f'{id} not exists')
        abort(404)

    if name is not None and name != continent.name:
        continent.name = name
    if population is not None and population != continent.population:
        continent.population = population
    if area is not None and area != continent.area_in_sq_meters:
        continent.area_in_sq_meters = area
    # continent.updated_at = datetime.datetime.utcnow
    try:
        continent.update()
    except :
        db.session.rollback()
        print('Error occured')
        abort(404)
    finally:
        db.session.close()
    return jsonify({
        "status_code": 200,
        "message": f'{id} is updated'
    })


@app.route('/api/wiki/continents/<int:id>', methods=['DELETE'])
def delete_a_continent(id):
    continent = Continent.query.get(id)
    if continent is None:
        abort(404)
    try:
        continent.delete()
    except Exception as e:
        db.session.rollback()
        print('Error', str(e))
        abort(404)
    finally:
        db.session.close()
    return jsonify({
        "status_code": 200,
        "message": f'{id} is deleted'
    })
