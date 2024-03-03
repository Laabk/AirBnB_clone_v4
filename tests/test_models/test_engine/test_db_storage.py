#!/usr/bin/python3
"""
Unit Test for BaseModel Clas
"""
import unittest
from models.engine.db_storage import DBStorage
from datetime import datetime
from models import *
import os
from models.base_model import Base



storage_type = os.environ.get('HBNB_TYPE_STORAGE')


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestDBStorageDocs(unittest.TestCase):
    """this class for testing BaseModel docs
    """

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """ a complete documentation for the file
        """
        expected = ' Database engine '
        actual = db_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """ the actual documentation for the class
        """
        expected = 'handles long term storage of all class instances'
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """a complete documentation for all function
        """
        expected = ' returns a dictionary of all objects '
        actual = DBStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """a complete documentation for new function"""
        expected = ' adds objects to current database session '
        actual = DBStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """ this is a completedocumentation for save function
        """
        expected = ' commits all changes of current database session '
        actual = DBStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """
        a complete documentation for reload function"""
        expected = ' creates all tables in database & session from engine '
        actual = DBStorage.reload.__doc__
        self.assertEqual(expected, actual)

    def test_doc_delete(self):
        """a complete documentation for delete function"""
        expected = ' deletes obj from current database session if not None '
        actual = DBStorage.delete.__doc__
        self.assertEqual(expected, actual)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStateDBInstances(unittest.TestCase):
    """this is testing class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('......... Testing DBStorage .;.......')
        print('........ For State Class ........')
        print('.................................\n\n')

    def setUp(self):
        """this will initializes new BaseModel object for testing"""
        self.state = State()
        self.state.name = 'California'
        self.state.save()

    def test_state_all(self):
        """this will checks if all() function returns
        newly created instance
        """
        all_objs = storage.all()
        all_state_objs = storage.all('State')

        exist_in_all = False
        for k in all_objs.keys():
            if self.state.id in k:
                exist_in_all = True
        exist_in_all_states = False
        for k in all_state_objs.keys():
            if self.state.id in k:
                exist_in_all_states = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_state_delete(self):
        state_id = self.state.id
        storage.delete(self.state)
        self.state = None
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if state_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestUserDBInstances(unittest.TestCase):
    """the testing method for class instances
    """

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """this will initializes new user for testing
        """
        self.user = User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()

    def test_user_all(self):
        """
        this checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_user_objs = storage.all('User')

        exist_in_all = False
        for k in all_objs.keys():
            if self.user.id in k:
                exist_in_all = True
        exist_in_all_users = False
        for k in all_user_objs.keys():
            if self.user.id in k:
                exist_in_all_users = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_users)

    def test_user_delete(self):
        user_id = self.user.id
        storage.delete(self.user)
        self.user = None
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if user_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestCityDBInstances(unittest.TestCase):
    """this is for testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... City  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """this initializes new user for testing the test class
        """
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'Fremont'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_all(self):
        """ this will checks if all() function returns
        newly created instance"""
        all_objs = storage.all()
        all_city_objs = storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestCityDBInstancesUnderscore(unittest.TestCase):
    """this is testing for class instances
    """

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... City Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """ this initializes new user for testing
        """
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Francisco'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_underscore_all(self):
        """this will checks if all() function returns newly created instance
        """
        all_objs = storage.all()
        all_city_objs = storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestPlaceDBInstances(unittest.TestCase):
    """this is testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """ithis initializes new user
        for testing
        """
        self.user = User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city = City()
        self.city.name = 'San_Mateo'
        self.city.state_id = self.state.id
        self.city.save()
        self.place = Place()
        self.place.city_id = self.city.id
        self.place.user_id = self.user.id
        self.place.name = 'test_place'
        self.place.description = 'test_description'
        self.place.number_rooms = 2
        self.place.number_bathrooms = 1
        self.place.max_guest = 4
        self.place.price_by_night = 100
        self.place.latitude = 120.12
        self.place.longitude = 101.4
        self.place.save()

    def test_place_all(self):
        """ this will checks if all() function returns
        newly created instance"""
        all_objs = storage.all()
        all_place_objs = storage.all('Place')

        exist_in_all = False
        for k in all_objs.keys():
            if self.place.id in k:
                exist_in_all = True
        exist_in_all_place = False
        for k in all_place_objs.keys():
            if self.place.id in k:
                exist_in_all_place = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_place)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStorageGet(unittest.TestCase):
    """ this Test `get()` method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """this setup tests for class"""
        print('\n\n.................................')
        print('...... Testing Get() Method ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """
        this setup method for test
        """
        self.state = State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """this test get() method
        :return: if true if pass"""
        resu = storage.get(cls="State", id=self.state.id)
        self.assertIsInstance(resu, State)

    def test_get_method_return(self):
        """test get() method for id match
        :return: if true if pass"""
        resu = storage.get(cls="State", id=str(self.state.id))

        self.assertEqual(self.state.id, resu.id)

    def test_get_method_none(self):
        """ this test get() method for None return
        :return: if true if pass"""
        resu = storage.get(cls="State", id="doesnotexist")

        self.assertIsNone(resu)


@unittest.skipIf(storage_type != 'db', 'skip if environ is not db')
class TestStorageCount(unittest.TestCase):
    """the tests count() method used in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """ the test setup tests for class
        """
        print('\n\n.................................')
        print('...... Testing Get() Method ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setup(self):
        """
        the setup method for the test of subclass"""
        self.state1 = State(name="California")
        self.state1.save()
        self.state2 = State(name="Colorado")
        self.state2.save()
        self.state3 = State(name="Wyoming")
        self.state3.save()
        self.state4 = State(name="Virgina")
        self.state4.save()
        self.state5 = State(name="Oregon")
        self.state5.save()
        self.state6 = State(name="New_York")
        self.state6.save()
        self.state7 = State(name="Ohio")
        self.state7.save()

    def test_count_all(self):
        """test counting all instances
        :return: if True if pass
        """
        resu = storage.count()
        self.assertEqual(len(storage.all()), resu)

    def test_count_state(self):
        """this test counting state instances
        :return: if True if pass
        """
        result = storage.count(cls="State")

        self.assertEqual(len(storage.all("State")), result)

    def test_count_city(self):
        """test counting non existent
        :return: is true if pass"""
        result = storage.count(cls="City")

        self.assertEqual(int(0 if len(storage.all("City")) is None else
                             len(storage.all("City"))), result)


if __name__ == '__main__':
    unittest.main
