#!/usr/bin/python3
""" This module defines the class: Place.  """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Define the association table for the Many-to-Many relationship
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id', String(60), ForeignKey(
            'places.id'), primary_key=True, nullable=False),
    Column(
        'amenity_id', String(60), ForeignKey(
            'amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """Representation of Place """
    __tablename__ = 'places'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    city_id = Column(String(60), ForeignKey(
        'cities.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # Define the back-reference from Place to City
    city = relationship('City', back_populates='places')
    # Define the back-reference from Place to User
    user = relationship('User', back_populates='places')
    # Define the back-reference from Review to Place
    reviews = relationship(
        'Review', back_populates='place', cascade='all, delete-orphan')
    # Define the Many-to-Many relationship with the Amenity class
    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        viewonly=False)
    # FileStorage Relationships (Getter and Setter)
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        self.city_id = kwargs.get('city_id', "")
        super().__init__(*args, **kwargs)

    @property
    def amenities(self):
        """Getter attribute for amenities in FileStorage"""
        # Assuming that amenities is a list of Amenity instances
        return [Amenity(id=amenity_id) for amenity_id in self.amenity_ids]

    @amenities.setter
    def amenities(self, amenity):
        """Setter attribute for amenities in FileStorage"""
        # Accept only Amenity objects
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
