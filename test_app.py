import os
import json
import pytest

from app import app

SECRET = 'TestSecret'
TOKEN_EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNSmVlYWpMWUNaOXhoRkxUdENRcCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhdXRob3Jpc2UuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTcxZGU2MTkwNjI1MGMxNGQ4ZWNiNCIsImF1ZCI6ImNhc3RpbmcgYWdlbmN5IiwiaWF0IjoxNTkxMjk3MzA3LCJleHAiOjE1OTEzMDQ1MDcsImF6cCI6IldUWFVoTkFLZEpLbzJWMjF1eTNWMjdpYnh3ekRlVVJCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.dXbVngsJjY3YekZy8RgyFqe6-fTrGv3lWdQSjZgJMhzcXySRyzP7XNzQen_r_8-sSyaqhYdq29LWI_TbqkIbeX2Db86RrMrRL8Q6X5ywnhXJAWj6m4xzj5dIxrWG3z90I7h4D5GhsjlMLB4xGBJ7uneKO7DAPqRHpb-47brtBe8q9oAD3GENSBkOGh8wr3adpKJa0Av3C7roxicCktzmyJu7AJpdI8IBPseJ_UPZXm6jNCy_CijlX8kySxireMcQL8UPZ5ebsTIMN2pSiLL_Sd6HycYamqoMsZfKVzO6A9V7FXTWUxkH6LwcxS3G1dTTX44pwsc9RBymmCrSd5pdeA'
TOKEN_CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNSmVlYWpMWUNaOXhoRkxUdENRcCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhdXRob3Jpc2UuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYTY2ZDVmMWNjMWFjMGMxNDY5MzlkMSIsImF1ZCI6ImNhc3RpbmcgYWdlbmN5IiwiaWF0IjoxNTkxMjg4Mjc4LCJleHAiOjE1OTEyOTU0NzgsImF6cCI6IldUWFVoTkFLZEpLbzJWMjF1eTNWMjdpYnh3ekRlVVJCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.lTwuQ4VXemJLslNR57NTmFrTq75TEQShHqWUvEBoDizMA7Ho1HbkMAfL2vy5LMraIpaqEFY8lHW4oZQh7zRkPfOaqYHjCaseVzqi3cfA_-PW4JlU9YKzWSEd5e9PtS9oqHvdztgZ8yaQnPP2qCvi12jEI6eFD5OQikJaeokB2Nb3oTTAHVRySm1lOoLwXTXzyuW6LOYbVa0ev81MdeZfYtCAIHZsFiwzqgz7YT86C8GB-_yrWMtBjfucfyCcO8cBDrl3ljWpCyrm2K0yb7dWGXrcakp6uWI_X-O6CurdEumWHsN0IZLuGsAaf_KR6hTXxHO-TJy0tzTv5qIAeS7vlA'
TOKEN_CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNSmVlYWpMWUNaOXhoRkxUdENRcCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhdXRob3Jpc2UuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDdiMzc3NDk4MDRlMGM0YWI3MmNlOCIsImF1ZCI6ImNhc3RpbmcgYWdlbmN5IiwiaWF0IjoxNTkxMjg3NDQ5LCJleHAiOjE1OTEyOTQ2NDksImF6cCI6IldUWFVoTkFLZEpLbzJWMjF1eTNWMjdpYnh3ekRlVVJCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Hh-ZUud1cC2nbL_0Vtvy7lcenxqUF1sxkOhYJQYgWu6ig4upWPs0nuNPF5wPydtzh8EzdbKCUr3oEkFl9fVU4AEJHE5l-1ikLob40cWS7LsvLb2zZVJGbZBNkKZeUT1O0LBhaa8ZZ2xA49xWiiWaE7VdcXNPySAhUVpGWJn0QEiSg9LKtPJ8HZLIN3TsdA9Szbf5nJlhQm57Csp7It_A6yjaR0hP-fnL980i5c2CgXr7RhGJTZ4C0fZ0IXR1c9Od3muQ0JDx6Uzf48J178U1OsXpfY0T7Z1qmhr0foeL6TZhe6jfzC5nkttjIciLasmm2s0ZudzNM1xkLlM4tVxglA'


@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


'''
Successful actors retrieval
'''


def test_get_actors_success(client):
    headers = {'Authorization': f'bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.get('/actors', headers=headers)
    assert response.status_code in [200, 404]


'''
Gets UnAuthorised error without Authorisation Bearer 
'''


def test_get_actors_not_authorised(client):
    response = client.get('/actors')
    assert response.status_code == [401]


# Auth test Test for Casting Assistant to get actors list
def test_get_actors_casting_assistant_error(client):
    headers = {'Authorization': f'bearer {TOKEN_CASTING_ASSISTANT}'}
    response = client.get('/actors', headers=headers)
    assert response.status_code in [401]


'''
Test Successful Actor creation
'''


def test_post_actors_success(client):
    body = {'name': 'Rajini',
            'age': 40,
            'gender': 'Male'}
    headers = {'Authorization': f'bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.post('/actors',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == [200]
    assert response.json['actors']['name'] == 'Rajini'


'''
Test actor creation not allowed
'''


def test_post_actor_casting_assistant_not_allowed(client):
    body = {'name': 'Rajini',
            'age': 40,
            'gender': 'M'}
    headers = {'Authorization': f'Bearer {TOKEN_CASTING_ASSISTANT}'}
    response = client.post('/actors',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == [401]


'''
Gets successful actor data update
'''


def test_update_actors_success(client):
    body = {'name': 'Kamal',
            'age': 40,
            'gender': 'M'}
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.patch('/actors/1',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == [200]
    assert response.json['actors']['name'] == 'Kamal'


'''
Test error while updating actor
'''


def test_update_actors_error(client):
    body = {'name': 'Rajini',
            'age': 25,
            'gender': 'Male'}
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.patch('/actors/500',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == [422]


'''
Test Successful actor delete
'''


def test_delete_actors_success(client):
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.delete('/actors/1', headers=headers)
    assert response.status_code == [200, 404]


'''
Test actor deletion error
'''


def test_delete_actors_error(client):
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.delete('/actors/1000', headers=headers)
    assert response.status_code == [404]


'''
Test successful movie creation
'''


def test_get_movies_success(client):
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.get('/movies', headers=headers)
    assert response.status_code in [200, 404]


'''
Test Gte movies error without Auth header
'''


def test_get_movies_error(client):
    response = client.get('/movies')
    assert response.status_code == 401


'''
Test successful creation of movie
'''


def test_post_movies_success(client):
    body = {'title': 'DEVIL',
            'release_date': '2019-12-11'}
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.post('/movies',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 200
    assert response.json['movies']['title'] == 'DEVIL'


'''
Test Auth error for Casting director role to create a Movie record
'''


def test_post_movies_casting_director_error(client):
    body = {'title': 'EVIL',
            'release_date': '2019-12-11'}
    headers = {'Authorization': f'Bearer {TOKEN_CASTING_DIRECTOR}'}
    response = client.post('/movies',
                           data=json.dumps(body),
                           content_type='application/json',
                           headers=headers)
    assert response.status_code == 401


'''
Test Successfully update movie details
'''


def test_update_movies_success(client):
    body = {'title': 'ET',
            'release_date': '2019-11-11'}
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.patch('/movies/1',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == 200
    assert response.json['movies']['title'] == 'ET'


'''
Test Error when tries to update movie details
'''


def test_update_movies_error(client):
    body = {'a': 'DEVIL',
            'b': '2019-11-11'}
    headers = {'Authorization': f'Bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.patch('/movies/500',
                            data=json.dumps(body),
                            content_type='application/json',
                            headers=headers)
    assert response.status_code == 400


'''
Test successful deletion of movie
'''


def test_delete_movies_success(client):
    headers = {'Authorization': f'bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.delete('/movies/1', headers=headers)
    assert response.status_code == 200


'''
Test error while deleting movie
'''


def test_delete_movies_error(client):
    headers = {'Authorization': f'bearer {TOKEN_EXECUTIVE_PRODUCER}'}
    response = client.delete('/movies/500', headers=headers)
    assert response.status_code == 404
