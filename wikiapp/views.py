from flask import jsonify, request, abort

from wikiapp import app, error_handler
from wikiapp.models import Continent, setup_db, db, Country

setup_db(app)

'''
Continent APIs
'''


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
    app.logger.info('Responded with all continents data')
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
    try:
        continent.insert()
        app.logger.info(f'continent {name} added successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(404)
    finally:
        db.session.close()

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
        app.logger.warning(f'User provided Continent ID does not exists')
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
        app.logger.info(f'continent {name} updated successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
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
        app.logger.warning(f'User provided Continent ID does not exists')
        abort(404)
    try:
        continent.delete()
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(404)
    finally:
        db.session.close()
    return jsonify({
        "status_code": 200,
        "message": f'{id} is deleted'
    })


'''
Countries
'''


@app.route('/api/wiki/continents/<int:continent_id>/countries', methods=['GET'])
def get_countries(continent_id):
    countries_list = []
    countries = Country.query.all()
    for country in countries:
        country_json_data = {
            "id": country.id,
            "name": country.name,
            "population": country.population,
            "area": country.area_in_sq_meters,
            "number_of_hospitals": country.number_of_hospitals,
            "number_of_national_parks": country.number_of_national_parks
        }
        countries_list.append(country_json_data)
    app.logger.info('Responded with all countries data')
    return jsonify({
        "status_code": 200,
        "countries": countries_list,
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries', methods=['POST'])
def create_a_country(continent_id):
    body = request.get_json()
    name = body.get("name")
    population = body.get("population")
    area = body.get("area")
    number_of_hospitals = body.get("number_of_hospitals")
    number_of_national_parks = body.get("number_of_parks")
    country = Country(name=name, population=population, area=area,
                      number_of_hospitals=number_of_hospitals,
                      number_of_national_parks=number_of_national_parks,
                      continent_id=continent_id)
    try:
        country.insert()
        app.logger.info(f'Country {name} added successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(404)
    finally:
        db.session.close()

    return jsonify({
        "status_code": 200,
        "message": f"{name} country created."
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>', methods=['PUT'])
def update_a_country(continent_id, country_id):
    body = request.get_json()
    name = body.get("name")
    population = body.get("population")
    area = body.get("area")
    number_of_hospitals = body.get("number_of_hospitals")
    number_of_national_parks = body.get("number_of_parks")

    country = Country.query.filter(Country.id == country_id).one_or_none()
    if country is None:
        app.logger.warning(f'User provided Country ID does not exists')
        abort(404)

    if name is not None and name != country.name:
        country.name = name
    if population is not None and population != country.population:
        country.population = population
    if area is not None and area != country.area_in_sq_meters:
        country.area_in_sq_meters = area
    if number_of_hospitals is not None and number_of_hospitals != country.number_of_hospitals:
        country.number_of_hospitals = number_of_hospitals
    if number_of_national_parks is not None and number_of_national_parks != country.number_of_national_parks:
        country.number_of_national_parks = number_of_national_parks

    try:
        country.update()
        app.logger.info(f'country {name} updated successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(404)
    finally:
        db.session.close()
    return jsonify({
        "status_code": 200,
        "message": f'{country_id} is updated'
    })


@app.route('/api/wiki/continents/<int:continent_id>/countries/<int:country_id>', methods=['DELETE'])
def delete_a_country(continent_id, country_id):
    # country = Country.query.get(country_id)
    country = Country.query.filter(Country.id == country_id).one_or_none()
    if country is None:
        app.logger.warning(f'User provided Country ID does not exists')
        abort(404)
    try:
        country.delete()
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(404)
    finally:
        db.session.close()
    return jsonify({
        "status_code": 200,
        "message": f'{country_id} is deleted'
    })