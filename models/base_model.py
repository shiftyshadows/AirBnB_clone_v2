#!/usr/bin/python3
""" This module defines the base class that other classes inherit from.  """
import uuid
from datetime import datetime
from models import storage

time_format = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """ This class defines all common attributes/methods for other classes. """
    def __init__(self, *args, **kwargs):
        """
           This class method that serves as the constructor for the class.
           It is automatically called when an instance of the class is created,
           and its purpose is to initialize the attributes of the object.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if hasattr(self, "created_at") and type(self.created_at) is str:
                self.created_at = datetime.strptime(
                    kwargs["created_at"], time_format)
            if hasattr(self, "updated_at") and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"], time_format)
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        storage.new(self)
        storage.save()

    def __str__(self):
        """
           This class method defines how an object should be represented
           as a string when it is converted using the built-in str() function
           or when it is used in string formatting.
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """
           This class method updates the public instance
           attribute updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
           This method returns a dictionary containing all
           keys/values of __dict__ of the instance.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
#        if "created_at" in obj_dict:
#            obj_dict["created_at"] = self.created_at.strftime(time_format)
#        if "updated_at" in obj_dict:
#            obj_dict["updated_at"] = self.updated_at.strftime(time_format)
        if "created_at" in obj_dict:
            obj_dict["created_at"] = obj_dict["created_at"].\
                strftime(time_format)
        if "updated_at" in obj_dict:
            obj_dict["updated_at"] = obj_dict["updated_at"].\
                strftime(time_format)
        return obj_dict
