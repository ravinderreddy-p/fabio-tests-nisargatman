from sqlalchemy import func

from wikiapp.models import Country, City


def validate_population(country_id, current_city_population):
    print(f"current city population {current_city_population}")
    if current_city_population is None:
        print("current population?? ")
        return True
    country_population = Country.query.filter_by(id=country_id).first().population
    print(f"country population: {country_population}")
    total_population_of_existing_cities = 0
    cities = City.query.filter_by(country_id=country_id)
    for city in cities:
        total_population_of_existing_cities += city.population
    print(f"total existing cities population {total_population_of_existing_cities}")
    total_cities_population = total_population_of_existing_cities + current_city_population
    if total_cities_population < country_population:
        print("True")
    else:
        print("False")
    return total_cities_population < country_population


def validate_area(country_id, current_city_area):
    if current_city_area is None:
        return True
    country_area = Country.query.filter_by(id=country_id).first().area_in_sq_meters
    total_area_of_existing_cities = 0
    cities = City.query.filter_by(country_id=country_id)
    for city in cities:
        total_area_of_existing_cities += city.area
    total_cities_area = total_area_of_existing_cities + current_city_area
    return total_cities_area < country_area
