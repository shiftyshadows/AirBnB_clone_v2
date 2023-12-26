#!/usr/bin/python3
"""This module defines the DBStorage Engine. """
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, class_mapper
from sqlalchemy.ext.declarative import declarative_base
import os

Base=declarative_base()
#os.environ["HBNB_MYSQL_USER"] = "hbnb_dev"
#os.environ["HBNB_MYSQL_PWD"] = "hbnb_dev_pwd"
#os.environ["HBNB_MYSQL_HOST"] = "localhost"
#os.environ["HBNB_MYSQL_DB"] = "hbnb_dev_db"
#os.environ["HBNB_TYPE_STORAGE"] = "db"

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """
           The __init__ method creates the SQLAlchemy engine, linking it to the
           MySQL database using environment variables. It also drops all tables
           if the environment variable HBNB_ENV is equal to 'test'.
        """


        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB')

        dialect = 'mysql'
        driver = 'mysqldb'
        pool_pre_ping = True if os.environ.get('HBNB_ENV') == 'test' else False

        connection_string = f'{dialect}+{driver}://{user}:{password}@{host}/{database}'
        self.__engine = create_engine(connection_string, pool_pre_ping=pool_pre_ping)
        if os.environ.get('HBNB_ENV') == 'test':
            meta = MetaData(self.__engine)
            meta.reflect()
            meta.drop_all()

    def all(self, cls=None):
        """Query on the current database session (self.__session) all objects
        depending on the class name (argument cls).

        If cls is None, query all types of objects (User, State, City, Amenity, Place, and Review).

        Returns:
            dict: Dictionary with key-value pairs where
                key = <class-name>.<object-id>
                value = object
        """
        from models.base_model import BaseModel
        from models.state import State
        from models.city import City

        result = {}
        classes_to_query = [State, City] if cls is None else [cls]

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
            self.__session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        return self.__session()

    def new(self, obj):
        """Add the object to the current database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current database session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the current database session."""
        if self.__session:
            self.__session.remove()
