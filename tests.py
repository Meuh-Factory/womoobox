from django.test import TestCase, Client
from womoobox.models import *
from womoobox.settings import *
import json


class ApiKeyTestCase(TestCase):
    def setUp(self):
        self.apikey1 = ApiKey.objects.create(user_agent="Mozilla/5.0")
        self.apikey2 = ApiKey.objects.create(user_agent="Mozilla/5.0")
        self.client  = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_apikay_have_default_username(self):
        """ Test that newly created ApiKey have a default username """
        expected_username = "User_" + str(self.apikey1 .id)
        self.assertEqual(self.apikey1.user_name, expected_username)

    def test_apikay_have_default_key(self):
        """ Test that newly created ApiKey have a default random key """
        self.assertIsNotNone(self.apikey2.key)

    def test_gen_key_with_GET(self):
        """ Test that we can generate a key instance by using GET HTTP request """
        response = self.client.get('/api/key/add/')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['result'], 'succeed')
        
    def test_rename_key(self):
        """ Test that we can rename a key username """
        response = self.client.post('/api/key/rename/', {
            'key': self.apikey1.key,
            'old_username': self.apikey1.user_name,
            'new_username': 'test123'
        })
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['result'], 'succeed')
        self.assertEqual(response_json['user_name'], 'test123')

    def test_rename_key_error_101(self):
        """ Test error case for code 101: invalid inputs """
        response = self.client.post('/api/key/rename/', {
            'key': '', # volontary error
            'old_username': self.apikey1.user_name,
            'new_username': 'test123'
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 101)

    def test_rename_key_error_105(self):
        """ Test error case for code 105: invalid username """
        response = self.client.post('/api/key/rename/', {
            'key': self.apikey1.key,
            'old_username': 'plop', # volontary error
            'new_username': '123test'
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 105)

    def test_rename_key_error_106(self):
        """ Test error case for code 106: invalid username """
        response = self.client.post('/api/key/rename/', {
            'key': self.apikey1.key,
            'old_username': self.apikey1.user_name,
            'new_username': self.apikey2.user_name, # volontary error
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 106)


class MooTestCase(TestCase):
    def setUp(self):
        self.apikey = ApiKey.objects.create(user_agent="Mozilla/5.0")
        self.moo1 = Moo.objects.create(key=self.apikey,
                                       latitude=12.98765,
                                       longitude=-23.29930,
                                       animal_type='cow')
        self.moo2 = Moo.objects.create(key=self.apikey,
                                       latitude=0.2334,
                                       longitude=48.23440001,
                                       animal_type='donkey')
        self.client  = Client()

    def test_moo_add(self):
        """ Test that you can create a moo with a post request """
        response = self.client.post('/api/moo/add/', {
            'key': self.apikey.key,
            'latitude': 27.0993,
            'longitude': -1,
            'animal': 'frog'
        })
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['result'], 'succeed')

    def test_moo_get(self):
        """ Test that you can get list of recent moo """
        response = self.client.get('/api/moo/get_lasts/')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_json['moos']), 2)

    def test_moo_get_from_id(self):
        """ Test that you can get list of recent moo """
        new_moo = Moo.objects.create(key=self.apikey,
                                    latitude=-12.98765,
                                    longitude=23.29930,
                                    animal_type='owl')
        response = self.client.get('/api/moo/get_lasts/', {'id': 1})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_json['moos']), 2)

    def test_moo_count(self):
        """ Test that you can get count of moo """
        response = self.client.get('/api/moo/count/')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['nb_moos'], 
                         Moo.objects.all().count())

    def test_moo_add_error_101(self):
        """ Test error case for code 101: invalid inputs """
        response = self.client.post('/api/moo/add/', {
            'key': self.apikey.key,
            'latitude': None, # volontary error
            'longitude': -1,
            'animal': 'dog'
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 101)

    def test_moo_add_error_102(self):
        """ Test error case for code 102: invalid coords value(s) """
        response = self.client.post('/api/moo/add/', {
            'key': self.apikey.key,
            'latitude': 500, # volontary error
            'longitude': -1,
            'animal': 'duck'
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 102)

    def test_moo_add_error_103(self):
        """ Test error case for code 103: too many moo in a too short time """
        self.client.post('/api/moo/add/', {
            'key': self.apikey.key,
            'latitude': 10,
            'longitude': -10,
            'animal': 'fly'
        })
        response = self.client.post('/api/moo/add/', {
            'key': self.apikey.key,
            'latitude': -10,
            'longitude': 10,
            'animal': 'fly'
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 103)

    def test_moo_add_error_201(self):
        """ Test error case for code 201: API key is invalid """
        response = self.client.post('/api/moo/add/', {
            'key': ''.join(['z' for n in range(KEY_LENGTH)]), # volontary error
            'latitude': 10,
            'longitude': -10,
            'animal': 'cat'
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 201)

    def test_moo_add_error_202(self):
        """ Test error case for code 202: API key is blacklisted """
        self.apikey.blacklisted=True # volontary error
        self.apikey.save()
        response = self.client.post('/api/moo/add/', {
            'key': self.apikey.key,
            'latitude': -10,
            'longitude': -10,
            'animal': 'sheep'
        })
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 202)
        self.apikey.blacklisted=False
        self.apikey.save()

    def test_moo_get_from_id_error_104(self):
        """ Test error case for code 104: invalid ID """
        response = self.client.get('/api/moo/get_lasts/', {'id': 99}) # volontary error
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_json['error_code'], 104)