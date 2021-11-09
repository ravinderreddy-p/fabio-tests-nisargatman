from flask import abort
from sqlalchemy import func

from wikiapp import app
from wikiapp.models import Country, City


def country_count_is_higher_than_cities_count(country_count, existing_cities_total_count, new_city_count):
    cities_total_count = existing_cities_total_count + new_city_count
    return cities_total_count < country_count


def population_and_area_are_valid(country_id, new_city_population, new_city_area):
    country = Country.query.filter_by(id=country_id).first()
    country_population = country.population
    country_area = country.area_in_sq_meters

    existing_cities_population = City.query.with_entities(func.sum(City.population).label("sum")) \
        .filter(country_id == country_id).first()

    existing_cities_area = City.query.with_entities(func.sum(City.area_in_sq_meters).label("sum")) \
        .filter(country_id == country_id).first()

    if country_count_is_higher_than_cities_count(country_population, existing_cities_population.sum,
                                                 new_city_population):
        if country_count_is_higher_than_cities_count(country_area, existing_cities_area.sum, new_city_area):
            return True
        else:
            app.logger.warning(f'city area exceeds total country: {country_id} area')
            abort(410)
    else:
        app.logger.warning(f'city population exceeds total country: {country_id} population')
        abort(411)


def population_is_valid_for_update(country_id, city_id, population):
    country_population = Country.query.filter_by(id=country_id).first().population
    current_city_population = City.query.filter_by(id=city_id).first().population
    cities_population = City.query.with_entities(func.sum(City.population).label("sum")) \
        .filter(country_id == country_id).first()
    updated_cities_population = cities_population.sum - current_city_population
    updated_cities_population = updated_cities_population + population
    return updated_cities_population < country_population


def area_is_valid_for_update(country_id, city_id, area):
    country_area = Country.query.filter_by(id=country_id).first().area_in_sq_meters
    current_city_area = City.query.filter_by(id=city_id).first().area_in_sq_meters
    cities_area = City.query.with_entities(func.sum(City.population).label("sum")) \
        .filter(country_id == country_id).first()
    updated_cities_area = cities_area.sum - current_city_area
    updated_cities_area = updated_cities_area + area
    return updated_cities_area < country_area

