#!/usr/bin/python3
"""the moduke for the User Class
"""

from models.base_model import BaseModel, Base
import os
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
from hashlib import md5
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """all the applications handles for the User class
    """
    if storage_type == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', backref='user', cascade='delete')
        reviews = relationship('Review', backref='user', cascade='delete')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """ this willl initialize User Model, inherits from BaseModel
        """
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """ this seach and takes the password
        """
        return self.__dict__.get("password")

    @password.setter
    def password(self, password):
        """
        the Password used involved, with md5 hasing
        :return: void ornothing
        """
        self.__dict__["password"] = md5(password)
