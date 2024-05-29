import sys
import os
import pytest
from flask import Flask

# Proje kök dizinini sys.path'e ekleyin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, suggest, get_page_id, geosearch, get_page_url

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Wikipedia API' in response.data

def test_suggest(client):
    response = client.post('/suggest', data={'query': 'Python'})
    assert response.status_code == 200
    assert b'Python' in response.data

def test_suggest_case_insensitive(client):
    response = client.post('/suggest', data={'query': 'python'})
    assert response.status_code == 200
    assert b'Python' in response.data

def test_suggest_partial_match(client):
    response = client.post('/suggest', data={'query': 'Pyth'})
    assert response.status_code == 200
    assert b'Python' in response.data

def test_suggest_no_result(client):
    response = client.post('/suggest', data={'query': 'asldkfjalsdkfj'})
    assert response.status_code == 200
    assert b'None' in response.data

def test_page_id(client):
    response = client.post('/page_id', data={'title': 'Python (programming language)'})
    assert response.status_code == 200
    assert b'pageid' in response.data

def test_page_id_case_insensitive(client):
    response = client.post('/page_id', data={'title': 'python (programming language)'})
    assert response.status_code == 200
    assert b'pageid' in response.data

def test_page_id_special_chars(client):
    response = client.post('/page_id', data={'title': 'C++'})
    assert response.status_code == 200
    assert b'pageid' in response.data

def test_page_id_invalid_title(client):
    response = client.post('/page_id', data={'title': 'asldkfjalsdkfj'})
    assert response.status_code == 200
    assert b'-1' in response.data

def test_geosearch(client):
    response = client.post('/geosearch', data={'lat': '37.7749', 'lon': '-122.4194'})
    assert response.status_code == 200
    assert b'title' in response.data

def test_geosearch_invalid_coords(client):
    response = client.post('/geosearch', data={'lat': '0', 'lon': '0'})
    assert response.status_code == 200
    assert b'[]' in response.data

def test_geosearch_special_coords(client):
    response = client.post('/geosearch', data={'lat': '90', 'lon': '0'})
    assert response.status_code == 200
    assert b'[]' in response.data

def test_page_url(client):
    page = get_page_id('Python (programming language)')
    pageid = page['pageid']
    response = client.post('/page_url', data={'pageid': str(pageid)})
    assert response.status_code == 200
    assert b'wikipedia.org' in response.data

def test_page_url_invalid_id(client):
    response = client.post('/page_url', data={'pageid': '-1'})
    assert response.status_code == 200
    assert b'Page not found' in response.data

def test_page_url_invalid_id_format(client):
    response = client.post('/page_url', data={'pageid': 'invalid'})
    assert response.status_code == 400
    assert b'Invalid pageid' in response.data

def test_page_url_no_id(client):
    response = client.post('/page_url', data={'pageid': ''})
    assert response.status_code == 400
    assert b'Invalid pageid' in response.data

def test_suggest_empty_query(client):
    response = client.post('/suggest', data={'query': ''})
    assert response.status_code == 200
    assert b'None' in response.data

def test_page_id_empty_title(client):
    response = client.post('/page_id', data={'title': ''})
    assert response.status_code == 200
    assert b'-1' in response.data

def test_geosearch_empty_coords(client):
    response = client.post('/geosearch', data={'lat': '', 'lon': ''})
    assert response.status_code == 400  # Adjust based on your actual response for invalid inputs

def test_geosearch_missing_lat(client):
    response = client.post('/geosearch', data={'lat': '', 'lon': '-122.4194'})
    assert response.status_code == 400  # Adjust based on your actual response for invalid inputs

def test_geosearch_missing_lon(client):
    response = client.post('/geosearch', data={'lat': '37.7749', 'lon': ''})
    assert response.status_code == 400  # Adjust based on your actual response for invalid inputs
