from wikiapp import app
from wikiapp.models import Continent, db
from flask import abort


def get_all_continents():
    continents_list = []
    continents = Continent.query.all()
    print(continents)
    print(type(continents))
    for continent in continents:
        continent_json_data = {
            'id': continent.id,
            'name': continent.name,
            'population': continent.population,
            'area': continent.area_in_sq_meters
        }
        continents_list.append(continent_json_data)
    return continents_list


def get_a_continent_data(continent_id):
    continent = Continent.query.filter_by(id=continent_id).one_or_none()
    print(continent_id)
    if continent is None:
        app.logger.warning(f'User provided continent-ID: {continent_id} does not exists to fetch data')
        abort(404)
    return continent


def add_a_new_continent(request_body):
    name = request_body.get('name')
    if name is None:
        app.logger.warning('User not provided mandatory field: name')
        abort(404)
    population = request_body.get('population')
    if population is None:
        app.logger.warning('User not provided mandatory field: population')
        abort(404)
    area = request_body.get('area')
    if area is None:
        app.logger.warning('User not provided mandatory field: area')
        abort(404)
    continent = Continent(name=name, population=population, area_in_sq_meters=area)
    try:
        continent.insert()
        app.logger.info(f'continent {name} added successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return name


def update_a_continent_data(request_body, continent_id):
    name = request_body.get('name')
    population = request_body.get('population')
    area = request_body.get('area')
    continent = Continent.query.filter_by(id=continent_id).one_or_none()
    if continent is None:
        app.logger.warning(f'User provided continent-ID: {continent_id} does not exists')
        abort(404)

    if name is not None:
        continent.name = name
    if population is not None:
        continent.population = population
    if area is not None:
        continent.area_in_sq_meters = area
    # continent.updated_at = datetime.datetime.utcnow
    try:
        continent.update()
        app.logger.info(f'continent-ID:{continent_id} updated successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return continent_id


def delete_a_continent_data(continent_id):
    continent = Continent.query.filter_by(id=continent_id).one_or_none()
    if continent is None:
        app.logger.warning(f'User provided Continent-ID: {continent_id} does not exists')
        abort(404)
    try:
        continent.delete()
        app.logger.info(f'Continent-ID: {continent_id} deleted')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return continent_id
