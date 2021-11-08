from flask import abort

from wikiapp import app
from wikiapp.models import Country, City


def city_population_is_valid(country_population, cities, current_city_population):
    cities_total_population = 0
    for city in cities:
        cities_total_population += city.population
    total_population_count = cities_total_population + current_city_population
    return total_population_count < country_population


def city_area_is_valid(country_population, cities, current_city_area):
    cities_total_area = 0
    for city in cities:
        cities_total_area += city.area
    total_area_count = cities_total_area + current_city_area
    return total_area_count < country_population


def population_and_area_are_valid(country_id, current_city_population, current_city_area):
    country = Country.query.filter_by(id=country_id).first()
    country_population = country.population
    country_area = country.area_in_sq_meters
    cities = City.query.filter_by(country_id=country_id).all()
    if city_population_is_valid(country_population, cities, current_city_population):
        if city_area_is_valid(country_area, cities, current_city_area):
            return True
        else:
            app.logger.warning(f'city area exceeds total country: {country_id} area')
            abort(410)
    else:
        app.logger.warning(f'city population exceeds total country: {country_id} population')
        abort(411)


