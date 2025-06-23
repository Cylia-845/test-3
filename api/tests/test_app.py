import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_addition(client):
    response = client.get('/add?a=5&b=3')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['result'] == 8.0

def test_missing_parameters(client):
    response = client.get('/add')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['result'] == 0.0

def test_invalid_input(client):
    response = client.get('/add?a=abc&b=2')
    json_data = response.get_json()
    assert response.status_code == 400
    assert 'error' in json_data
