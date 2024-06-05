#!/usr/bin/python3
""" This module defines the FileStorage class. """
import json
from datetime import datetime

time_format = "%Y-%m-%dT%H:%M:%S.%f"


class FileStorage:
    """
       This class serializes instances to a JSON file and
       deserializes JSON file to instances.
    """
    __file_path = "file.json"
    __objects = {}
    class_dict = {
        "BaseModel": "models.base_model",
        "User": "models.user",
        "State": "models.state",
        "City": "models.city",
        "Amenity": "models.amenity",
        "Place": "models.place",
        "Review": "models.review",
            }

    def all(self):
        """ This method returns the dictionary __objects. """
        return FileStorage.__objects

    def new(self, obj):
        """
           This method sets in __objects the obj with the
           key <obj class name>.id.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
           This method serializes __objects to the JSON file
           (path: __file_path).
        """
        serialized_objects = {}
        objects = FileStorage.__objects
        for key, obj in objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
           This method deserializes the JSON file to __objects
           (only if the JSON file (__file_path) exists ; otherwise, do nothing.
           If the file doesn’t exist, no exception should be raised).
        """
        try:
            with open(FileStorage.__file_path, "r") as file:
                loaded_objects = json.load(file)
                for key, value in loaded_objects.items():
                    class_name = value["__class__"]
                    value['created_at'] = datetime.strptime(
                        value['created_at'], time_format)
                    value['updated_at'] = datetime.strptime(
                        value['updated_at'], time_format)
                    for key_2, value_2 in FileStorage.class_dict.items():
                        if class_name == key_2:
                            module_name = value_2
                    module = __import__(module_name, fromlist=[class_name])
                    cls = getattr(module, class_name)
                    if cls:
                        obj = cls(**value)
                        self.new(obj)
#                        FileStorage.__objects[key] = obj
        except FileNotFoundError:
            FileStorage.__objects = {}
