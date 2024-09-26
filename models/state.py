#!/usr/bin/python3
""" This module defines the class: State.  """
from datetime import datetime
from models.base_model import BaseModel
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.base_model import Base
else:
    Base = object


class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", back_populates="state", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
               Getter for the cities attribute.
               Returns:
                   List of City instances related to the current State.
            """
            from models import storage
            all_cities = storage.all("City")
            state_cities = []
            for city in all_cities.values():
                if city.state_id == self.id:
                    state_cities.append(city)
            return state_cities

# engine = create_engine(
#    "mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db", echo=False)
# Base.metadata.create_all(engine)
