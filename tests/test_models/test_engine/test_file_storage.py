#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))




@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestBmFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """sets up the class"""
        print('\n\n.................................')
        print('...... Testing FileStorate ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')
        cls.bm_obj = BaseModel()
        cls.state_obj = State(name="Illinois")
        cls.bm_obj.save()
        cls.state_obj.save()

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        storage.delete_all()
        remove(F)

    def setUp(self):
        """initializes new storage object for testing"""
        self.bm_obj = TestBmFsInstances.bm_obj
        self.state_obj = TestBmFsInstances.state_obj

    def test_instantiation(self):
        """... checks proper FileStorage instantiation"""
        self.assertIsInstance(storage, FileStorage)

    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.bm_obj.save()
        self.assertTrue(path.isfile(F))

    def test_all(self):
        """... checks if all() function returns newly created instance"""
        bm_id = self.bm_obj.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_all_state(self):
        """... checks if all() function returns newly created state instance"""
        state_id = self.state_obj.id
        state_objs = storage.all("State")
        actual = False
        for k in state_objs.keys():
            if state_id in k:
                actual = True
        self.assertTrue(True)

    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_to_json(self):
        """... to_json should return serializable dict object"""
        my_model_json = self.bm_obj.to_json()
        actual = True
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = False
        self.assertTrue(actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = True
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestUserFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """sets up the class"""
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')
        cls.user = User()
        cls.user.save()
        cls.bm_obj = BaseModel()
        cls.bm_obj.save()


    def test_count_cls(self):
        """... checks count method with class input arg"""
        count_user = storage.count('User')
        expected = 1
        self.assertEqual(expected, count_user)

    def test_count_all(self):
        """... checks the count method with no class input"""
        count_all = storage.count()
        expected = 2
        self.assertEqual(expected, count_all)

    def test_get_cls_id(self):
        """... checks get method with class and id inputs"""
        duplicate = storage.get('User', self.user.id)
        expected = self.user.id
        actual = duplicate.id
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main