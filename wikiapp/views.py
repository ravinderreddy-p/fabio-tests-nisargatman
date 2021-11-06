from flask import jsonify, request

from wikiapp import app
from wikiapp.models import Continent, setup_db

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
    area = body.get("area")
    continent = Continent(name=name, population=population, area_in_sq_meters=area)
    continent.insert()
