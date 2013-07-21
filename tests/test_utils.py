from pypackager import utils
from unittest2 import TestCase


class UtilsTests(TestCase):
    def test_recursive_update(self):
        dict1 = {
            'a': {
                'a1': 1,
                'a2': 2
            },
            'b': {
                'b1': 3,
                'b2': 4
            }
        }
        dict2 = {
            'b': {
                'b2': 5
            }
        }

        expected = {
            'a': {
                'a1': 1,
                'a2': 2
            },
            'b': {
                'b1': 3,
                'b2': 5
            }
        }
        new_dict = utils.recursive_update(dict1, dict2)
        self.assertTrue('a' in new_dict)
        self.assertEqual(new_dict, expected)

    def test_clean_dict(self):
        dict1 = {
            'a': 1,
            'b': None,
            'c': {}
        }

        expected = {
            'a': 1
        }
        new_dict = utils.clean_dict(dict1)
        self.assertEqual(new_dict, expected)
