#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base

class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities' 
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        This class method that serves as the constructor for the class.
        It is automatically called when an instance of the class is created,
        and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)
