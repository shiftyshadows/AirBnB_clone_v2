#!/usr/bin/python3
""" This module defines the class: Amenity.  """
from models.base_model import BaseModel, Base
from models.place import place_amenity
from sqlalchemy import create_engine, Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    # Define the Many-to-Many relationship with the Place class
    places = relationship('Place', secondary=place_amenity, viewonly=False)

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)


#engine = create_engine(
#    "mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db", echo=False)
#Base.metadata.create_all(engine)
