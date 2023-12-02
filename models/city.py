#!/usr/bin/python3
""" This module defines the class: City.  """
from models.base_model import BaseModel


class City(BaseModel):
    """Representation of city """
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        if 'state_id' not in kwargs:
            self.state_id = ""
        else:
            self.state_id = kwargs.pop('state_id')
        super().__init__(*args, **kwargs)
