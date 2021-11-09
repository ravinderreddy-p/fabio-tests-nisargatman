from flask import jsonify, request, abort, make_response, json

from wikiapp import app, error_handler
from wikiapp.cities import get_all_cities, add_a_new_city, update_a_city_data, delete_a_city_data, get_a_city_data
from wikiapp.continents import get_all_continents, add_a_new_continent, update_a_continent_data, \
    delete_a_continent_data, get_a_continent_data
from wikiapp.countries import get_all_countries, add_a_new_country, update_a_country_data, delete_a_country_data, \
    get_a_country_data
from wikiapp.models import Continent, setup_db, db, Country, City

setup_db(app)

'''
Continent APIs
'''


@app.route('/api/wiki/continents', methods=['GET'])
def get_continents():
    continents_list = get_all_continents()
    return jsonify({
        'status_code': 200,
        'continents_list': continents_list
    })


@app.route('/api/wiki/continents/<int:id>', methods=['GET'])
def get_a_continent(id):
    continent = get_a_continent_data(id)
    continent_data_in_json = {
        "id": continent.id,
        "name": continent.name,
        "population": continent.population,
        "area": continent.area_in_sq_meters,
        "countries_link": f'http://127.0.0.1:5000/api/wiki/continents/{id}/countries'
    }

    return jsonify({
        'status_code': 200,
        'continent': continent_data_in_json,
    })


@app.route('/api/wiki/continents', methods=['POST'])
def add_a_continent():
    body = request.get_json()
    continent_name = add_a_new_continent(body)
    return jsonify({
        'status_code': 200,
        'message': f'Continent: {continent_name} successfully created.'
    })


@app.route('/api/wiki/continents/<int:id>', methods=['PUT'])
def update_a_continent(id):
    body = request.get_json()
    continent_id = update_a_continent_data(body, id)
    return jsonify({
        'status_code': 200,
        "message": f'Continent-ID: {continent_id} successfully updated'
    })


@app.route('/api/wiki/continents/<int:id>', methods=['DELETE'])
def delete_a_continent(id):
    continent_id = delete_a_continent_data(id)
    return jsonify({
        'status_code': 200,
        'message': f'Continent-ID: {continent_id} deleted'
    })


'''
Countries
'''


@app.route('/api/wiki/continents/<int:continent_id>/countries', methods=['GET'])
def get_countries(continent_id):
    countries_list = get_all_countries(continent_id)
    return jsonify({
        'status_code': 200,
        'countries': countries_list,
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>', methods=['GET'])
def get_a_country(continent_id, country_id):
    country = get_a_country_data(country_id)
    country_data_in_json = {
        "id": country.id,
        "name": country.name,
        "population": country.population,
        "area": country.area_in_sq_meters,
        "number_of_hospitals": country.number_of_hospitals,
        "number_of_national_parks": country.number_of_national_parks,
        "cities_link": f'http://127.0.0.1:5000/api/wiki/continents/{continent_id}/countries/{country_id}/cities'
    }

    return jsonify({
        'status_code': 200,
        'continent': country_data_in_json,
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries', methods=['POST'])
def add_a_country(continent_id):
    body = request.get_json()
    country_name = add_a_new_country(body, continent_id)
    return jsonify({
        'status_code': 200,
        'message': f'Country: {country_name} created.'
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>', methods=['PUT'])
def update_a_country(continent_id, country_id):
    body = request.get_json()
    country_id = update_a_country_data(body, country_id)
    return jsonify({
        'status_code': 200,
        'message': f'{country_id} is updated'
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>', methods=['DELETE'])
def delete_a_country(continent_id, country_id):
    country_id = delete_a_country_data(country_id)
    return jsonify({
        "status_code": 200,
        "message": f'{country_id} is deleted'
    })


'''
Cities
'''


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities', methods=['GET'])
def get_cities(continent_id, country_id):
    cities_list = get_all_cities(country_id)
    return jsonify({
        "status_code": 200,
        "cities": cities_list,
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities/<int:city_id>', methods=['GET'])
def get_a_city(continent_id, country_id, city_id):
    city = get_a_city_data(city_id)
    city_data_in_json = {
        "id": city.id,
        "name": city.name,
        "population": city.population,
        "area": city.area_in_sq_meters,
        "number_of_roads": city.number_of_roads,
        "number_of_trees": city.number_of_trees
    }

    return jsonify({
        'status_code': 200,
        'continent': city_data_in_json,
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities', methods=['POST'])
def create_a_city(continent_id, country_id):
    body = request.get_json()
    city_name = add_a_new_city(body, country_id)
    return jsonify({
        "status_code": 200,
        "message": f"{city_name} city created."
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities/<int:city_id>', methods=['PUT'])
def update_a_city(continent_id, country_id, city_id):
    body = request.get_json()
    city_id = update_a_city_data(body, city_id, country_id)
    return jsonify({
        "status_code": 200,
        "message": f'City {city_id} is updated'
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities/<int:city_id>', methods=['DELETE'])
def delete_a_city(continent_id, country_id, city_id):
    city_id = delete_a_city_data(city_id)
    return jsonify({
        "status_code": 200,
        "message": f'{city_id} is deleted'
    })
