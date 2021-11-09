from flask import abort
from sqlalchemy import func

from wikiapp import app
from wikiapp.models import Country, City

'''
Validate country data against continent data
'''


def country_count_is_higher_than_cities_count(country_population_or_area,
                                              existing_cities_total_population_or_area,
                                              new_city_population_or_area):
    cities_total_population_or_area = existing_cities_total_population_or_area + new_city_population_or_area
    return cities_total_population_or_area < country_population_or_area


def city_population_and_area_are_valid(country_id, new_city_population, new_city_area):
    # todo use one_or_None and through None exception if
    country = Country.query.filter_by(id=country_id).one_or_none()
    if country is None:
        app.logger.warning(f'country-ID: {country_id} does not exist. ')
        abort(400)
    country_population = country.population
    country_area = country.area_in_sq_meters

    # At first time, if we add new city, we should validate data with existing country's data only.
    cities_count = City.query.filter_by(country_id=country_id).count()
    if cities_count == 0:
        if country_population > new_city_population and country_area > new_city_area:
            return True
        else:
            app.logger.warning(f'City area or population exceeds total '
                               f'Country-ID: {country_id} area or population')
            abort(400)

    # If already cities exists under Country, then we need to get full count of all cities population or area.
    # If not exceeds new city data, then only add new city else it's a bad request.
    existing_cities_population = City.query.with_entities(func.sum(City.population).label("sum")) \
        .filter_by(country_id=country_id).first()

    existing_cities_area = City.query.with_entities(func.sum(City.area_in_sq_meters).label("sum")) \
        .filter_by(country_id=country_id).first()
    print(country_population)
    print(existing_cities_population.sum)
    print(new_city_population)
    if country_count_is_higher_than_cities_count(country_population, existing_cities_population.sum,
                                                 new_city_population):
        if country_count_is_higher_than_cities_count(country_area, existing_cities_area.sum, new_city_area):
            return True
        else:
            app.logger.warning(f'city area exceeds total country: {country_id} area')
            abort(400)
    else:
        app.logger.warning(f'city population exceeds total country: {country_id} population')
        abort(400)


def city_population_is_valid_for_update(country_id, city_id, population):
    country_population = Country.query.filter_by(id=country_id).first().population
    current_city_population = City.query.filter_by(id=city_id).first().population
    cities_population = City.query.with_entities(func.sum(City.population).label("sum")) \
        .filter_by(country_id=country_id).first()
    updated_cities_population = cities_population.sum - current_city_population
    updated_cities_population = updated_cities_population + population
    return updated_cities_population < country_population


def city_area_is_valid_for_update(country_id, city_id, area):
    country_area = Country.query.filter_by(id=country_id).first().area_in_sq_meters
    current_city_area = City.query.filter_by(id=city_id).first().area_in_sq_meters
    cities_area = City.query.with_entities(func.sum(City.population).label("sum")) \
        .filter_by(country_id=country_id).first()
    updated_cities_area = cities_area.sum - current_city_area
    updated_cities_area = updated_cities_area + area
    return updated_cities_area < country_area
