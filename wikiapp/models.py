from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

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
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    population = Column(Integer, unique=False, nullable=False)
    area_in_sq_meters = Column(Float, unique=False, nullable=False)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=False)
    country = relationship('Country', backref='continents', lazy='dynamic')

    def __init__(self, name):
        self.name = name

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
    hospitals_count = Column(Integer, unique=False, nullable=True)
    national_parks_count = Column(Integer, unique=False, nullable=True)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=False)
    continent_id = Column(Integer, ForeignKey('continents.id'))
    city = relationship('City', backref='countries', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
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
    roads_count = Column(Integer, unique=False, nullable=True)
    trees_count = Column(Integer, unique=False, nullable=True)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'))

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()