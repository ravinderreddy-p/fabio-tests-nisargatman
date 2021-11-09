from flask import abort
from sqlalchemy import func

from wikiapp import app
from wikiapp.models import Country, Continent

'''
Validate country data against continent data
'''


def continent_count_is_higher_than_countries_count(continent_count, existing_countries_total_count, new_country_count):
    cities_total_count = existing_countries_total_count + new_country_count
    return cities_total_count < continent_count


def country_population_and_area_are_valid(continent_id, new_country_population, new_country_area):
    continent = Continent.query.filter_by(id=continent_id).one_or_none()
    if continent is None:
        app.logger.warning(f'continent-ID: {continent_id} does not exist. ')
        abort(400)
    continent_population = continent.population
    continent_area = continent.area_in_sq_meters

    existing_countries_population = Country.query.with_entities(func.sum(Country.population).label("sum")) \
        .filter(continent_id == continent_id).first()

    existing_countries_area = Country.query.with_entities(func.sum(Country.area_in_sq_meters).label("sum")) \
        .filter(continent_id == continent_id).first()

    if continent_count_is_higher_than_countries_count(continent_population, existing_countries_population.sum,
                                                      new_country_population):
        if continent_count_is_higher_than_countries_count(continent_area, existing_countries_area.sum,
                                                          new_country_area):
            return True
        else:
            app.logger.warning(f'Country area exceeds total Continent-ID: {continent_id} area')
            abort(400)
    else:
        app.logger.warning(f'Country population exceeds total Continent-ID: {continent_id} population')
        abort(400)


def country_population_is_valid_for_update(continent_id, country_id, population):
    continent_population = Continent.query.filter_by(id=continent_id).first().population
    current_country_population = Country.query.filter_by(id=country_id).first().population
    countries_population = Country.query.with_entities(func.sum(Country.population).label("sum")) \
        .filter(continent_id == continent_id).first()
    updated_countries_population = countries_population.sum - current_country_population
    updated_countries_population = updated_countries_population + population
    return updated_countries_population < continent_population


def country_area_is_valid_for_update(continent_id, country_id, area):
    continent_area = Continent.query.filter_by(id=continent_id).first().area_in_sq_meters
    current_country_area = Country.query.filter_by(id=country_id).first().area_in_sq_meters
    countries_area = Country.query.with_entities(func.sum(Country.population).label("sum")) \
        .filter(continent_id == continent_id).first()
    updated_countries_area = countries_area.sum - current_country_area
    updated_countries_area = updated_countries_area + area
    return updated_countries_area < continent_area
