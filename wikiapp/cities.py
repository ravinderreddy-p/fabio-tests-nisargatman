from wikiapp import app
from wikiapp.data_validation import population_is_valid, population_and_area_are_valid
from wikiapp.models import City, db, Country
from flask import abort


def get_all_cities(country_id):
    cities_list = []
    cities = City.query.filter_by(country_id=country_id).all()
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
    return cities_list


def add_a_new_city(request_body, country_id):
    name = request_body.get("name")
    if name is None:
        app.logger.warning(f'User not provided City name under continent-Id: {country_id}')
        abort(404)
    population = request_body.get("population")
    if population is None:
        app.logger.warning(f'User not provided City Population under continent-Id: {country_id}')
        abort(404)
    area = request_body.get("area")
    if area is None:
        app.logger.warning(f'User not provided City Area under continent-Id: {country_id}')
        abort(404)
    number_of_roads = request_body.get("number_of_roads")
    number_of_trees = request_body.get("number_of_trees")
    # Data Validations to be done before posting the data
    # if population_is_valid(country_id, population):
    if population_and_area_are_valid(country_id, population, area):
        city = City(name=name, population=population, area=area,
                    number_of_roads=number_of_roads,
                    number_of_trees=number_of_trees,
                    country_id=country_id)
        try:
            city.insert()
            app.logger.info(f'City: {name} added successfully')
        except Exception as error:
            db.session.rollback()
            app.logger.error(error)
            abort(502)
        finally:
            db.session.close()
    return name


def update_a_city_data(request_body, city_id):
    name = request_body.get("name")
    population = request_body.get("population")
    area = request_body.get("area")
    number_of_roads = request_body.get("number_of_roads")
    number_of_trees = request_body.get("number_of_trees")

    city = City.query.filter_by(id=city_id).one_or_none()
    if city is None:
        app.logger.warning(f'User provided City-ID: {city_id} does not exists')
        abort(404)
    if name is not None:
        city.name = name
    if population is not None:
        # Data Validations to be done before posting the data
        city.population = population
    if area is not None:
        # Data Validations to be done before posting the data
        city.area_in_sq_meters = area
    if number_of_roads is not None:
        city.number_of_roads = number_of_roads
    if number_of_trees is not None:
        city.number_of_trees = number_of_trees
    try:
        city.update()
        app.logger.info(f'city-ID: {city_id} updated successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return city_id


def delete_a_city_data(city_id):
    city = City.query.filter_by(id=city_id).one_or_none()
    if city is None:
        app.logger.warning(f'User provided City-ID: {city_id} does not exists')
        abort(404)
    try:
        city.delete()
        app.logger.info(f'City-ID: {city_id} deleted successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return city_id
