import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

SECRET = 'TestSecret'
TOKEN_EXECUTIVE_PRODUCER = os.environ['EXECUTIVE_PRODUCER']
TOKEN_CASTING_DIRECTOR = os.environ['CASTING_DIRECTOR']
TOKEN_CASTING_ASSISTANT = os.environ['CASTING_ASSISTANT']


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    Successful actors retrieval
    '''

    def test_get_actors_success(self):
        headers = {'Authorization': f'bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.get('/actors', headers=headers)
        assert response.status_code in [200, 404]

    '''
    Gets UnAuthorised error without Authorisation Bearer 
    '''

    def test_get_actors_not_authorised(self):
        response = self.client.get('/actors')
        assert response.status_code == 401

    '''
    Test Successful Actor creation
    '''

    def test_post_actors_success(self):
        body = {'name': 'Rajini',
                'age': 40,
                'gender': 'Male'}
        headers = {'Authorization': f'bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.post('/actors',
                                    data=json.dumps(body),
                                    content_type='application/json',
                                    headers=headers)
        assert response.status_code == 200

    '''
    Test actor creation not allowed
    '''

    def test_post_actor_casting_assistant_not_allowed(self):
        body = {'name': 'Rajini',
                'age': 40,
                'gender': 'M'}
        headers = {'Authorization': f'Bearer {TOKEN_CASTING_ASSISTANT}'}
        response = self.client.post('/actors',
                                    data=json.dumps(body),
                                    content_type='application/json',
                                    headers=headers)
        assert response.status_code == 401

    '''
    Gets successful actor data update
    '''

    def test_update_actors_success(self):
        body = {'name': 'Kamal',
                'age': 40,
                'gender': 'M'}
        headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.patch('/actors/2',
                                     data=json.dumps(body),
                                     content_type='application/json',
                                     headers=headers)
        assert response.status_code == 200

    '''
    Test error while updating actor
    '''

    def test_update_actors_error(self):
        body = {'name': 'Rajini',
                'age': 25,
                'gender': 'Male'}
        headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.patch('/actors/500',
                                     data=json.dumps(body),
                                     content_type='application/json',
                                     headers=headers)
        assert response.status_code == 404

    '''
    Test actor deletion error
    '''

    def test_delete_actors_error(self):
        headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.delete('/actors/1000', headers=headers)
        assert response.status_code == 404

    '''
    Test successful movie creation
    '''

    def test_get_movies_success(self):
        headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.get('/movies', headers=headers)
        assert response.status_code in [200, 404]

    '''
    Test Gte movies error without Auth header
    '''

    def test_get_movies_error(self):
        response = self.client.get('/movies')
        assert response.status_code == 401

    '''
    Test successful creation of movie
    '''

    def test_post_movies_success(self):
        body = {'title': 'DEVIL',
                'release_date': '2019-12-11'}
        headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.post('/movies',
                                    data=json.dumps(body),
                                    content_type='application/json',
                                    headers=headers)
        assert response.status_code == 200
        assert response.json['movies']['title'] == 'DEVIL'

    '''
    Test Auth error for Casting director role to create a Movie record
    '''

    def test_post_movies_casting_director_error(self):
        body = {'title': 'EVIL',
                'release_date': '2019-12-11'}
        headers = {'Authorization': f'Bearer {TOKEN_CASTING_ASSISTANT}'}
        response = self.client.post('/movies',
                                    data=json.dumps(body),
                                    content_type='application/json',
                                    headers=headers)
        assert response.status_code == 401

    '''
    Test Successfully update movie details
    '''

    def test_update_movies_success(self):
        body = {'title': 'ET',
                'release_date': '2019-11-11'}
        headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.patch('/movies/2',
                                     data=json.dumps(body),
                                     content_type='application/json',
                                     headers=headers)
        assert response.status_code == 200

    '''
    Test Error when tries to update movie details
    '''

    def test_update_movies_error(self):
        body = {'a': 'DEVIL',
                'b': '2019-11-11'}
        headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.patch('/movies/500',
                                     data=json.dumps(body),
                                     content_type='application/json',
                                     headers=headers)
        assert response.status_code == 404

    '''
    Test error while deleting movie
    '''

    def test_delete_movies_error(self):
        headers = {'Authorization': f'bearer {TOKEN_EXECUTIVE_PRODUCER}'}
        response = self.client.delete('/movies/500', headers=headers)
        assert response.status_code == 404


# Make the tests conveniently executable

if __name__ == "__main__":
    unittest.main()
