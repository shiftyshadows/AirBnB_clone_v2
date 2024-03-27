#!/usr/bin/python3
""" This module defines the class: City.  """
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id', ondelete='CASCADE'), nullable=False)
    # Define the relationship with the State class
    state = relationship("State", back_populates="cities")
    # Define the relationship with the Place class
    places = relationship('Place', back_populates='city', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        self.state_id = kwargs.get('state_id', "")
        super().__init__(*args, **kwargs)
