#!/usr/bin/python3
""" This module defines the class: City.  """
from models.base_model import BaseModel


class City(BaseModel):
    """Representation of city """

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)
        self.state_id = kwargs.get('state_id', "")
        self.name = kwargs.get('name', "")
