#!/usr/bin/python3
""" This module defines the class: State.  """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'  # Add the table name
    name = Column(String(128), nullable=False) # For DBStorage
    cities = relationship('City', backref='state', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        """
        This class method that serves as the constructor for the class.
        It is automatically called when an instance of the class is created,
        and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)

    # For FileStorage
    @property
    def cities(self):
        """Getter attribute for cities in FileStorage"""
        from models import storage
        city_list = []
        for city in storage.all('City').values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
