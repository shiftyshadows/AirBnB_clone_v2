#!/usr/bin/python3
""" This module defines the class: Place.  """
import os
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Define the association table for the Many-to-Many relationship
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel,Base):
    """Representation of Place """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # Define the back-reference from Place to User
    user = relationship('User', back_populates='places')
    # Define the back-reference from Place to City
    city = relationship('City', back_populates='places')
    # Define the back-reference from Review to Place
    reviews = relationship('Review', back_populates='place', cascade='all, delete-orphan')
    # FileStorage Relationships (Getter and Setter)
    amenity_ids = []
    # Define the Many-to-Many relationship with the Amenity class
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            viewonly=False,
            backref='place_amenities'
        )
    else:
        @property
        def amenities(self):
            """Returns the amenities of this Place"""
            from models import storage
            amenities_of_place = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    amenities_of_place.append(value)
            return amenities_of_place

        @amenities.setter
        def amenities(self, value):
            """Adds an amenity to this Place"""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)

        @property
        def reviews(self):
            """Returns the reviews of this Place"""
            from models import storage
            reviews_of_place = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    reviews_of_place.append(value)
            return reviews_of_place

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)
