## Welcome

Hello. This project serves as a mini Wikipedia. This application provides the features to Create, Read, Update & Delete [CRUD] on continents, countries and cities data.

### Low Level Approach:

<hr>

#### Models:
Three models are required to build this application. Those are:

    1. Continents
        id(pk), name, population, area_in_sq_meters, created_at, updated_at
    2. Countries
        id(pk), name, population, area_in_sq_meters, number_of_hospitals,number_national_parks,continent_id(fk), created_at, updated_at
    3. Cities
        id(pk), name, population, area, number_of_roads, number_of_trees, country_id(fk), created_at, updated_at
    
Established a relation between ```Continents``` to ```Countries``` is ```one to many (1 -> M)``` and ```Countries``` to ```Cities``` is ```One to Many (1 -> M).```

Implemented Cascade delete for the models. ie., if parent record deletes then it's corresponding child records get deleted.

<hr>

#### APIs:
1. ```GET /api/wiki/continents HTTP/1.1```
    - Retrieves all the continents data from Continents model.
   
2. ```GET /api/wiki/continents/1 HTTP/1.1```
    - Retrieves specific continent ID (ex: 1) data from Continents models, also provides ``hyperlink`` to it's countries.

3. ```POST /api/wiki/continents HTTP/1.1```
    - Adds a new continent by providing mandatory fields - ``name, population and area.`` It updates ``created_at`` field whenever new continent added.
    - all these fields mandatory as this data is required for Country level validation(Area & Population)
    
4. ```PUT /api/wiki/continents/1 HTTP/1.1```
    - Updates a specific continent data. It updates ``updated_at`` field whenever any updates applied on existing data. 
    
5. ```DELETE /api/wiki/continents/1 HTTP/1.1```
    - Deletes a specific continent (ex: 1) from ``Continents`` model. Also deletes it's corresponding countries and cities.
    
6. ```GET /api/wiki/continents/1/countries HTTP/1.1```
    - Retrieves all the countries data corresponds to continent 1.
   
7. ```GET /api/wiki/continents/1/countries/1 HTTP/1.1```
    - Retrieves specific country (ex: 1) data from Continent(1), also provides ``hyperlink`` to it's cities.

8. ```POST /api/wiki/continents/1/countries HTTP/1.1```
    - Adds a new country. Client should provide mandatory fields - ``name, population and area.`` It updates ``created_at`` field whenever new country added.
    - Above 3 fields are mandatory as this data is required for City level validation (Area & Population)
    
9. ```PUT /api/wiki/continents/1/countries/1 HTTP/1.1```
    - Updates a specific country(ID: 1) data under continent (1). It updates ``updated_at`` field whenever any updates applied on existing data. 
    
10. ```DELETE /api/wiki/continents/1/countries/1 HTTP/1.1```
    - Deletes a specific country(ID: 1) from it's ``Continents``. Also deletes it's corresponding cities.
     
11. ```GET /api/wiki/continents/1/countries/1/cities HTTP/1.1```
    - Retrieves all the cities data corresponds to country (ID: 1).
   
12. ```GET /api/wiki/continents/1/countries/1/cities/1 HTTP/1.1```
    - Retrieves specific city(ID: 1) data from Country(ID:1).

13. ```POST /api/wiki/continents/1/countries/1/cities HTTP/1.1```
    - Adds a new City. Client should provide mandatory fields - ``name, population and area.`` It updates ``created_at`` field whenever new city added.
    - Above 3 fields are mandatory as this data is required for City level validation.
    
14. ```PUT /api/wiki/continents/1/countries/1/cities/1 HTTP/1.1```
    - Updates a specific city(ID: 1) data under country (1). It updates ``updated_at`` field whenever any updates applied on existing data. 
    
15. ```DELETE /api/wiki/continents/1/countries/1/cities/1 HTTP/1.1```
    - Deletes a specifi city (ID: 1) from it's ``Country.``
      
<hr>

#### Assumptions
1. Name, Population and Area fields are mandatory in data level validations.
2. If parent gets deleted then it's corresponding children should be deleted (Cascade delete).
3. Continent population and area should be ``>=``  all it's cities population and area respectively.
4. Country population and area should be ``>`` all it's cities population and area respectively.

<hr>

### Quick Start

1. Clone repo
    ```
    $ git clone https://github.com/ravinderreddy-p/fabio-tests-nisargatman.git 
    $ cd fabio-tests-nisargatman
    ```

2. Activate a virtual environment

    ```$ source env/bin/activate```

3. Install the dependencies:

    ```$ pip install -r requirements.txt```

4. Run the development server:

    ```$ python main.py```

5. Navigate to [http://localhost:5000/api/wiki/continents](http://localhost:5000/api/wiki/continents)

