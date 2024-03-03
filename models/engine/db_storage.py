#!/usr/bin/python3
""" the engine module for the Database"""

import os
from models.base_model import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models import base_model, amenity, city, place, review, state, user

class DBStorage:
    """
    this handles the longer storage of all class instances
    """
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    """
    this handles storage engine for database
    """
    __engine = None
    __session = None

    def __init__(self):
        """ this creates the engine self.__engine
        """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ a func that return sdictionary of all objects
        """
        obj_dict = {}
        if cls:
            obj_class = self.__session.query(self.CNC.get(cls)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
            return obj_dict
        for clas_nme in self.CNC:
            if clas_nme == 'BaseModel':
                continue
            obj_class = self.__session.query(
                self.CNC.get(clas_nme)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
        return obj_dict

    def new(self, obj):
        """ this will adds objects to current database session
        """
        self.__session.add(obj)

    def get(self, cls, id):
        """ gets a specific object
        :param: a class of object as string
        :param: id of object as string
        :return: any found object or None"""
        all_class = self.all(cls)

        for objs in all_class.values():
            if id == str(objs.id):
                return objs

        return None

    def count(self, cls=None):
        """
        this start to count of how many instances of a class
        :param: class name
        :return: this count of instances of a class"""
        return len(self.all(cls))

    def save(self):
        """
        makes a commits all changes of current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ this will delete an obj from current database
        session if not None
        """
        if objs is not None:
            self.__session.delete(obj)

    def reload(self):
        """ this will creates all tables in database
        & session from engine
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """when the close is called,remove() on private
            session attribute (self.session)
        """
        self.__session.remove()
