#!/usr/bin/python3
""" This module defines the class: Amenity.  """
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Representation of Amenity """
    name = ""

    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        super().__init__(*args, **kwargs)
