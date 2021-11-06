# fabio-tests-nisargatman
## Low Level Approach:
###Tables:
**continents**:
    id*, name, population, area, createdAt, updatedAt
    
**countries**:
    id*, name, population, area, number_of_hospitals,number_national_parks,continent_id**, createdAt, updatedAt

**cities**:
    id*, name, population, area, number_of_roads,number_of_trees,country_id**, createdAt, updatedAt

###APIs:
- [GET] /api/wiki/continents:
    - Fetch the data from Continents table and return to client in json format.

- [POST] /api/wiki/continents:
    - All the continents data (name, population & area) should be saved in continents table with CreatedTimeStamp.
    - Making all these fields mandatory as this data is required for Country level validation(Area & Population)
    
- [PUT] /api/wiki/continents/<<int:id>>:
    - Update the changes of data corresponding to given continent ID in Continent table.
    
- [DELETE] /api/wiki/continents/<<int:id>>:
    - If ID exists then delete the continent along with corresponding countries and cities[Assumed this way]
    - Else through an exception.

- [GET] /api/wiki/continents/<<int:id>>/countries:
    - Fetch the data from Countries table corresponds to specific given continent ID and return to client in json format.

- [POST] /api/wiki/continents/<<int:id>>/countries:
    - All the countries data (name, population, area, no.hospitals & no.national parks) should be saved in countries table with CreatedTimeStamp.
    - Making no.hospitals & no.national parks are optional as there is no dependency.
    
- [PUT] /api/wiki/continents/<<int:id>>:
    - Validate the data if data which is related to population and area. This should not exceed continent data.
    - Update the changes of data corresponding to given country ID in countries table.
    
- [DELETE] /api/wiki/continents/<<int:id>>:
    - If ID exists then delete the country along with corresponding cities[Assumed this way]
    - Else through an exception.
    
- [GET] /api/wiki/continents/<<int:id>>/countries/<<int:id>>/cities:
    - Fetch the data from Cities table corresponds to specific given Country ID and return to client in json format.

- [POST] /api/wiki/continents/<<int:id>>/countries/<<int:id>>/cities:
    - All the Cities data (name, population, area, no.roads & no.trees) should be saved in Cities table with CreatedTimeStamp but area and population should be validated (less or equal) against corresponding country data(area & population).
    - Making no.trees & no.roads are optional as there is no dependency.
    
- [PUT] /api/wiki/continents/<<int:id>>/<<int:id>>/cities/<<int:id>>:
    - Validate the data if data which is related to population and area. This should not exceed corresponding country data(area & population).
    - Update the changes of data corresponding to given country ID in countries table.
    
- [DELETE] /api/wiki/continents/<<int:id>>/<<int:id>>/cities/<<int:id>>:
    - If ID exists then delete the City
    - Else through an exception.