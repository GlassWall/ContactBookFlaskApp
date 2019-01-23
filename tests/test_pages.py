# project/test_basic.py


import os
import unittest

from api import app

TEST_DB = 'test1.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)


    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_search_name(self):
        response = self.app.get('/searchByName')
        self.assertEqual(response.status_code, 200)

    def test_search_email(self):
        response = self.app.get('/searchByEmail')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()