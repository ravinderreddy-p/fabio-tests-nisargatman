from flask import jsonify, request, abort

from wikiapp import app, error_handler
from wikiapp.continents import get_all_continents_data, add_a_new_continent, update_a_continent_data, \
    delete_a_continent_data
from wikiapp.countries import get_all_countries_data, add_a_new_country, update_a_country_data, delete_a_country_data
from wikiapp.data_validation import validate_population, validate_area
from wikiapp.models import Continent, setup_db, db, Country, City

setup_db(app)

'''
Continent APIs
'''


@app.route('/api/wiki/continents', methods=['GET'])
def get_continents():
    continents_list = get_all_continents_data()
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
    countries_list = get_all_countries_data()
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
    cities_list = []
    cities = City.query.all()
    for city in cities:
        city_json_data = {
            "id": city.id,
            "name": city.name,
            "population": city.population,
            "area": city.area_in_sq_meters,
            "number_of_roads": city.number_of_roads,
            "number_of_trees": city.number_of_trees
        }
        cities_list.append(city_json_data)
    app.logger.info('Responded with all cities data')
    return jsonify({
        "status_code": 200,
        "cities": cities_list,
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities', methods=['POST'])
def create_a_city(continent_id, country_id):
    body = request.get_json()
    name = body.get("name")
    population = body.get("population")
    area = body.get("area")
    number_of_roads = body.get("number_of_roads")
    number_of_trees = body.get("number_of_trees")
    # Data Validations to be done before posting the data
    if validate_population(country_id, population):
        if validate_area(country_id, area):
            city = City(name=name, population=population, area=area,
                        number_of_roads=number_of_roads,
                        number_of_trees=number_of_trees,
                        country_id=country_id)
            try:
                city.insert()
                app.logger.info(f'City {name} added successfully')
            except Exception as error:
                db.session.rollback()
                app.logger.error(error)
                abort(404)
            finally:
                db.session.close()
        else:
            app.logger.warning('Area is invalid')
            abort(404)
    else:
        app.logger.warning('Population is invalid')
        abort(404)

    return jsonify({
        "status_code": 200,
        "message": f"{name} city created."
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities/<int:city_id>', methods=['PUT'])
def update_a_city(continent_id, country_id, city_id):
    body = request.get_json()
    name = body.get("name")
    population = body.get("population")
    area = body.get("area")
    number_of_roads = body.get("number_of_roads")
    number_of_trees = body.get("number_of_trees")

    city = City.query.filter(City.id == city_id).one_or_none()
    if city is None:
        app.logger.warning(f'User provided City ID does not exists')
        abort(404)

    if name is not None and name != city.name:
        city.name = name
    if population is not None and population != city.population:
        # Data Validations to be done before posting the data
        if city.population > population:
            print(f'validate population {population} {city.population}')
            temp_population = population - city.population
        else:
            print(f'validate population {population} {city.population}')
            temp_population = city.population - population

        if validate_population(country_id, temp_population):
            print("after validation check")
            city.population = population
        else:
            app.logger.warning('Population is invalid')
            abort(404)
    if area is not None and area != city.area_in_sq_meters:
        # Data Validations to be done before posting the data
        if city.area > area:
            temp_area = area - city.area
        else:
            temp_area = city.area - area
        if validate_area(country_id, temp_area):
            city.area = area
        else:
            app.logger.warning('Area is invalid')
            abort(404)

    if number_of_roads is not None and number_of_roads != city.number_of_roads:
        city.number_of_roads = number_of_roads

    if number_of_trees is not None and number_of_trees != city.number_of_trees:
        city.number_of_trees = number_of_trees

    try:
        city.update()
        app.logger.info(f'city ID {city_id} updated successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(404)
    finally:
        db.session.close()
    return jsonify({
        "status_code": 200,
        "message": f'City {city_id} is updated'
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>/cities/<int:city_id>', methods=['DELETE'])
def delete_a_city(continent_id, country_id, city_id):
    # country = Country.query.get(country_id)
    city = City.query.filter(City.id == city_id).one_or_none()
    if city is None:
        app.logger.warning(f'User provided City ID does not exists')
        abort(404)
    try:
        city.delete()
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(404)
    finally:
        db.session.close()
    return jsonify({
        "status_code": 200,
        "message": f'{city_id} is deleted'
    })
