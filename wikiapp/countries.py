from wikiapp import app
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


def add_a_new_country(request_body, continent_id):
    name = request_body.get("name")
    if name is None:
        app.logger.warning(f'User not provided Country name')
        abort(404)
    population = request_body.get("population")
    if population is None:
        app.logger.warning(f'User not provided Country Population')
        abort(404)
    area = request_body.get("area")
    if area is None:
        app.logger.warning(f'User not provided Country Area')
        abort(404)
    number_of_hospitals = request_body.get("number_of_hospitals")
    number_of_national_parks = request_body.get("number_of_parks")
    # Data Validations to be done before posting the data
    country = Country(name=name, population=population, area=area,
                      number_of_hospitals=number_of_hospitals,
                      number_of_national_parks=number_of_national_parks,
                      continent_id=continent_id)
    try:
        country.insert()
        app.logger.info(f'Country: {name} added successfully')
    except Exception as error:
        db.session.rollback()
        app.logger.error(error)
        abort(502)
    finally:
        db.session.close()
    return name


def update_a_country_data(request_body, country_id):
    name = request_body.get("name")
    population = request_body.get("population")
    area = request_body.get("area")
    number_of_hospitals = request_body.get("number_of_hospitals")
    number_of_national_parks = request_body.get("number_of_parks")
    country = Country.query.filter_by(id=country_id).one_or_none()
    if country is None:
        app.logger.warning(f'User provided Country-Id: {country_id} does not exists')
        abort(404)
    if name is not None:
        country.name = name
    if population is not None:
        # Data Validations to be done before updating the data
        country.population = population
    if area is not None:
        # Data Validations to be done before updating the data
        country.area_in_sq_meters = area
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
        abort(404)
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

