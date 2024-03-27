#!/usr/bin/python3
""" This module defines the class: City.  """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id', ondelete='CASCADE'), nullable=False)
    # Define the relationship with the State class
    state = relationship("State", back_populates="cities")
    # Define the relationship with the Place class
    places = relationship('Place', back_populates='city', cascade='all, delete')

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        self.state_id = kwargs.get('state_id', "")
        super().__init__(*args, **kwargs)
