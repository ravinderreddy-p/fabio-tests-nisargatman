from flask import jsonify, request, abort

from wikiapp import app, error_handler
from wikiapp.cities import get_all_cities, add_a_new_city, update_a_city_data, delete_a_city_data
from wikiapp.continents import get_all_continents, add_a_new_continent, update_a_continent_data, \
    delete_a_continent_data
from wikiapp.countries import get_all_countries, add_a_new_country, update_a_country_data, delete_a_country_data
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
        'continents': continents_list
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


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities', methods=['POST'])
def create_a_city(continent_id, country_id):
    body = request.get_json()
    city_name = add_a_new_city(body, country_id)
    # Data Validations to be done before posting the data
    # if validate_population(country_id, population):
    #     if validate_area(country_id, area):
    #         city = City(name=name, population=population, area=area,
    #                     number_of_roads=number_of_roads,
    #                     number_of_trees=number_of_trees,
    #                     country_id=country_id)
    #         try:
    #             city.insert()
    #             app.logger.info(f'City {name} added successfully')
    #         except Exception as error:
    #             db.session.rollback()
    #             app.logger.error(error)
    #             abort(404)
    #         finally:
    #             db.session.close()
    #     else:
    #         app.logger.warning('Area is invalid')
    #         abort(404)
    # else:
    #     app.logger.warning('Population is invalid')
    #     abort(404)
    return jsonify({
        "status_code": 200,
        "message": f"{city_name} city created."
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities/<int:city_id>', methods=['PUT'])
def update_a_city(continent_id, country_id, city_id):
    body = request.get_json()
    city_id = update_a_city_data(body, city_id)
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
