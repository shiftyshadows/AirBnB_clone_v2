#!/usr/bin/python3
""" This module defines the class: State.  """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    # Define relationship to City
    cities = relationship("City", back_populates="state", cascade="all, delete-orphan")


    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)
        engine = create_engine("mysql://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db", echo=True)
        Base.metadata.create_all(engine)
