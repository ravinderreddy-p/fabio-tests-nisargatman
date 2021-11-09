from wikiapp import app
from wikiapp.country_data_validation import country_population_and_area_are_valid, \
    country_population_is_valid_for_update, country_area_is_valid_for_update
from wikiapp.models import Country, db
from flask import abort


def get_all_countries(continent_id):
    countries = Country.query.filter_by(continent_id=continent_id).all()
    countries_list = []
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
    return countries_list


def get_a_country_data(country_id):
    country = Country.query.filter_by(id=country_id).one_or_none()
    if country is None:
        app.logger.warning(f'User provided country-ID: {country_id} does not exists to fetch data')
        abort(400)
    return country


def add_a_new_country(request_body, continent_id):
    name = request_body.get("name")
    if name is None:
        app.logger.warning(f'User not provided Country name under continent-ID: {continent_id}')
        abort(400)
    population = request_body.get("population")
    if population is None:
        app.logger.warning(f'User not provided Country Population under continent-ID: {continent_id}')
        abort(400)
    area = request_body.get("area")
    if area is None:
        app.logger.warning(f'User not provided Country Area under continent-ID: {continent_id}')
        abort(400)
    number_of_hospitals = request_body.get("number_of_hospitals")
    number_of_national_parks = request_body.get("number_of_parks")

    if country_population_and_area_are_valid(continent_id, population, area):
        country = Country(name=name, population=population, area=area,
                          number_of_hospitals=number_of_hospitals,
                          number_of_national_parks=number_of_national_parks,
                          continent_id=continent_id)
        try:
            country.insert()
            app.logger.info(f'Country: {name} added successfully under continent-ID: {continent_id}')
        except Exception as error:
            db.session.rollback()
            app.logger.error(error)
            abort(502)
        finally:
            db.session.close()
    return name


def update_a_country_data(request_body, country_id, continent_id):
    name = request_body.get("name")
    population = request_body.get("population")
    area = request_body.get("area")
    number_of_hospitals = request_body.get("number_of_hospitals")
    number_of_national_parks = request_body.get("number_of_parks")
    country = Country.query.filter_by(id=country_id).one_or_none()
    if country is None:
        app.logger.warning(f'User provided Country-Id: {country_id} does not exists')
        abort(400)
    if name is not None:
        country.name = name
    if population is not None:
        # Data Validations to be done before updating the data
        if country_population_is_valid_for_update(continent_id, country_id, population):
            country.population = population
        else:
            app.logger.warning(f'Country-ID:{country_id} population exceeds total continent: {continent_id} population')
            abort(400)
    if area is not None:
        # Data Validations to be done before updating the data
        if country_area_is_valid_for_update(continent_id, country_id, area):
            country.area_in_sq_meters = population
        else:
            app.logger.warning(f'Country-ID:{country_id} area exceeds total continent: {continent_id} area')
            abort(400)

    if number_of_hospitals is not None:
        country.number_of_hospitals = number_of_hospitals
    if number_of_national_parks is not None:
        country.number_of_national_parks = number_of_national_parks
    try:
        country.update()
        app.logger.info(f'Country-ID: {country_id} updated successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return country_id


def delete_a_country_data(country_id):
    country = Country.query.filter_by(id=country_id).one_or_none()
    if country is None:
        app.logger.warning(f'User provided Country-ID: {country_id} does not exists')
        abort(400)
    try:
        country.delete()
        app.logger.info(f'Country-ID:{country_id} deleted.')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return country_id

