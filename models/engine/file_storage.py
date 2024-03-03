#!/usr/bin/python3
"""
Handling all presentables of JSON for storage of all class instances"""

import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """ensuring a longer storage term of class instances
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
    """CNC - the cnc variable is a dictionary with, Class Names
    values: Class types
    """
    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """this returns private attribute"""
        if cls:
            obj_dict = {}
            for class_id, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    obj_dict[class_id] = obj
            return obj_dict
        return FileStorage.__objects

    def new(self, obj):
        """chamges or updates in __objects the obj with key"""
        base_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[base_id] = obj

    def get(self, cls, id):
        """ this obtains a specific object
        :param: class
        :param: the id of instance
        :return: the object or None"""
        all_class = self.all(cls)

        for objs in all_class.values():
            if id == str(objs.id):
                return objs
        return None

    def count(self, cls=None):
        """ this counts of instances available
        :param: class
        :return: the number of instances available"""

        return len(self.all(cls))

    def save(self):
        """making serialization of the __objects to the JSON file"""
        filnme = FileStorage.__file_path
        de = {}
        for base_id, base_obj in FileStorage.__objects.items():
            de[base_id] = base_obj.to_json()
        with open(filnme, mode='w+', encoding='utf-8') as f_io:
            json.dump(de, f_io)

    def reload(self):
        """so when file exists, there is deserializes JSON
        file to __objects, else nothing
        """
        filnme = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                nw_objs = json.load(f_io)
        except:
            return
        for old_id, de in nw_objs.items():
            k_cls = de['__class__']
            de.pop("__class__", None)
            de["created_at"] = datetime.strptime(de["created_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            de["updated_at"] = datetime.strptime(de["updated_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            FileStorage.__objects[old_id] = FileStorage.CNC[k_cls](**de)

    def delete(self, obj=None):
        """
        this deletes obj when is present
        """
        if obj is None:
            return
        for k in list(FileStorage.__objects.keys()):
            if obj.id == k.split(".")[1] and k.split(".")[0] in str(obj):
                FileStorage.__objects.pop(k, None)
                self.save()

    def close(self):
        """the reload() method deserialization from the JSON
        within the close call"""
        self.reload()
