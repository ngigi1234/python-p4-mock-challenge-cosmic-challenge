from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship('Mission', back_populates='planet') # {Class name of variable}, back_populates={}

    # Add serialization rules
    serialize_rules = ('-missions.planet', )




class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)

    # Add relationship
    missions = db.relationship('Mission', back_populates='scientist') # {Class name of variable}, back_populates={}

    # Add serialization rules
    serialize_rules = ('-missions.scientist', )

    # Add validation
    @validates('name')
    def validate_name(self, key, value):
        if value:
            return value
        raise ValueError("Not valid name")

    @validates('field_of_study')
    def validate_field_of_study(self, key, value):
        if value:
            return value
        raise ValueError("Not valid field_of_study")




class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False) # foreign key is tablename
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"), nullable=False) # foreign key is tablename

    # Add relationships
    planet = db.relationship('Planet', back_populates='missions') # {Class name of variable}, back_populates={}
    scientist = db.relationship('Scientist', back_populates='missions') # {Class name of variable}, back_populates={}

    # Add serialization rules
    serialize_rules = ('-scientist.missions', '-planet.missions')

    # Add validation
    @validates('name')
    def validate_name(self, key, value):
        if value:
            return value
        raise ValueError('Mission must have name.')

    @validates('scientist_id')
    def validate_scientist(self, key, value):
        if value:
            return value
        raise ValueError('Mission must have scientist ID.')

    @validates('planet_id')
    def validate_planet(self, key, value):
        if value:
            return value
        raise ValueError('Mission must have planet ID.')
    

# BACK POPULATES
# x = db.relationship('Planet', back_populates='y') 
# y = db.relationship('Scientist', back_populates='x')


