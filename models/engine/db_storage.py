#!/usr/bin/python3
"""This module defines the DBStorage Engine. """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place

Base = declarative_base()


class DBStorage:
    """
       This class defines DBStrorage.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
           The __init__ method creates the SQLAlchemy engine, linking it to the
           MySQL database using environment variables. It also drops all tables
           if the environment variable HBNB_ENV is equal to 'test'.
        """

        dialect = 'mysql'
        driver = 'mysqldb'
        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB')
        ppp = True
        env = os.environ.get('HBNB_ENV')

        connection_string = "{}+{}://{}:{}@{}/{}".format(
            dialect, driver, user, password, host, database)
        self.__engine = create_engine(connection_string, pool_pre_ping=ppp)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session (self.__session)
           all objects depending on the class name (argument cls).

           If cls is None, query all types of objects.
           (User, State, City, Amenity, Place, and Review).

           Returns:
            dict: Dictionary with key-value pairs where
                key = <class-name>.<object-id>
                value = object
        """
        result = {}
        classes_to_query = [State, City, User, Place] if cls is None else [cls]

        for model_class in classes_to_query:
            model_name = model_class.__name__
            query_result = self.__session.query(model_class).all()
            for obj in query_result:
                key = f"{model_name}.{obj.id}"
                result[key] = obj

        return result

    def get_session(self):
        """ This method returns a session using the engine."""
        if self.__session is None:
            self.__session = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        return self.__session()

    def new(self, obj):
        """Add the object to the current database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            print(f"Error during commit: {e}")
        finally:
            self.__session.close()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
           Create all tables in the database and create the current
           database session.
        """
        Base.metadata.create_all(self.__engine)
        sesh_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sesh_factory)

    def close(self):
        """Close the current database session."""
        if self.__session:
            self.__session.close()
