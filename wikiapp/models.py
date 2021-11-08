import sys
from datetime import datetime

from flask import flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.functions import current_timestamp, func

database_path = 'postgresql://pravinderreddy@localhost:5432/wiki-db'
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db)
    # db.create_all()


'''
Continent
'''


class Continent(db.Model):
    __tablename__ = "continents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, unique=False, nullable=False)
    area_in_sq_meters = Column(Float, unique=False, nullable=False)
    created_at = Column(DateTime, unique=False, nullable=True)
    updated_at = Column(DateTime, unique=False, nullable=True)
    country = relationship('Country', backref='continents', cascade="all, delete", passive_deletes=True)

    def __init__(self, name, population, area_in_sq_meters):
        self.name = name
        self.population = population
        self.area_in_sq_meters = area_in_sq_meters
        self.created_at = datetime.utcnow()

    '''
    insert()
        inserts a new record into a model in database
        EXAMPLE
            continent = Continent(name=req_name, area=req_area, population=req_population)
            continent.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
       update()
           updates a existing record from a model in a database
           EXAMPLE
               continent = Continent.query.filter(Continent.id == id).one_or_none()
               continent.area = 10000
               continent.update()
       '''

    def update(self):
        self.updated_at = datetime.utcnow()
        db.session.commit()

    '''
       delete()
           delete a record from a model in database
           EXAMPLE
               continent = Continent(id=req_id)
               continent.delete()
       '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
Country
'''


class Country(db.Model):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, unique=False, nullable=False)
    area_in_sq_meters = Column(Float, unique=False, nullable=False)
    number_of_hospitals = Column(Integer, unique=False, nullable=True)
    number_of_national_parks = Column(Integer, unique=False, nullable=True)
    created_at = Column(DateTime, unique=False, nullable=True)
    updated_at = Column(DateTime, unique=False, nullable=True)
    continent_id = Column(Integer, ForeignKey('continents.id', ondelete="CASCADE"))
    city = relationship('City', backref='countries', cascade="all, delete", passive_deletes=True)

    def __init__(self, name, population, area, number_of_hospitals, number_of_national_parks, continent_id):
        self.name = name
        self.population = population
        self.area_in_sq_meters = area
        self.number_of_hospitals = number_of_hospitals
        self.number_of_national_parks = number_of_national_parks
        self.continent_id = continent_id
        self.created_at = datetime.utcnow()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
City
'''


class City(db.Model):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, unique=False, nullable=True)
    area_in_sq_meters = Column(Float, unique=False, nullable=True)
    number_of_roads = Column(Integer, unique=False, nullable=True)
    number_of_trees = Column(Integer, unique=False, nullable=True)
    created_at = Column(DateTime, unique=False, nullable=True)
    updated_at = Column(DateTime, unique=False, nullable=True)
    country_id = Column(Integer, ForeignKey('countries.id', ondelete="CASCADE"))

    def __init__(self, name, population, area, number_of_roads, number_of_trees, country_id):
        self.name = name
        self.population = population
        self.area_in_sq_meters = area
        self.number_of_roads = number_of_roads
        self.number_of_trees = number_of_trees
        self.country_id = country_id
        self.created_at = datetime.utcnow()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
