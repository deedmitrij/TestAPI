import json
import pytest
import random
import requests

from app.logger import logger
from config import TEST_DATA_PATH


def generate_valid_test_data_for_parametrizing() -> list[tuple[str, str]]:
    """
    Generate valid test data to parametrize the tests.

    :return: list of tuples with endpoint and valid data ID
    """
    with open(TEST_DATA_PATH, 'r') as file:
        data = json.load(file)
    data_to_parametrize = []
    for endpoint, ids in data.items():
        data_to_parametrize.append((endpoint, random.choice(list(ids.keys()))))
    return data_to_parametrize


def generate_invalid_test_data_for_parametrizing() -> list[tuple[str, int]]:
    """
    Generate invalid test data to parametrize the tests.

    :return: list of tuples with endpoint and invalid data ID
    """
    with open(TEST_DATA_PATH, 'r') as file:
        data = json.load(file)
    data_to_parametrize = []
    for endpoint in data:
        ids = [int(key) for key in data[endpoint].keys()]
        invalid_id = max(ids) + 1
        data_to_parametrize.append((endpoint, invalid_id))
    return data_to_parametrize


@pytest.mark.parametrize('endpoint, data_id', generate_valid_test_data_for_parametrizing())
def test_get_data_happy_path(fake_server, test_data, endpoint, data_id):
    """Check getting data from all endpoints with existing ID."""
    # Send a GET request to the server
    logger.info('Getting existing data from the server...')
    response = requests.get(f'{fake_server.address}/{endpoint}/{data_id}/')

    # Validate the response status code and body
    assert response.status_code == 200, 'Wrong response status code'
    assert response.json() == test_data[endpoint][data_id], 'Wrong response body'


@pytest.mark.parametrize('endpoint, invalid_id', generate_invalid_test_data_for_parametrizing())
def test_get_data_not_found(fake_server, endpoint, invalid_id):
    """Check getting data from all endpoints with invalid ID."""
    # Send a GET request to the server
    logger.info('Getting non-existent data from the server...')
    response = requests.get(f'{fake_server.address}/{endpoint}/{invalid_id}/')

    # Validate the response status code and body
    error_body = {"error": "ID not found"}
    assert response.status_code == 404, 'Wrong response status code'
    assert response.json() == error_body, 'Wrong response body'
