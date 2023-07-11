import pytest
import random
import requests
import statistics
import time

from app.logger import logger


@pytest.fixture
def fake_server(fake_server):
    """Add a delay to the server response."""
    # Add a delay to the server response
    fake_server.handler.set_delay(delay=True)

    # Run the tests
    yield fake_server

    # Remove the delay from the server response
    fake_server.handler.set_delay(delay=False)


def test_response_time(fake_server, test_data):
    """Check mean and standard deviation of the server response time."""
    endpoint = random.choice(list(test_data.keys()))
    data_id = random.choice(list(test_data[endpoint].keys()))
    response_times = []
    duration = 60
    logger.info(f'Sending requests to the server for {duration} seconds...')
    start_time = time.time()

    while time.time() - start_time < duration:
        start_request_time = time.time()
        requests.get(f'{fake_server.address}/{endpoint}/{data_id}/')
        end_request_time = time.time()

        response_time = end_request_time - start_request_time
        response_times.append(response_time)

    logger.info('Requests are finished. Calculating statistics...')
    mean_response_time = statistics.mean(response_times)
    std_dev_response_time = statistics.stdev(response_times)
    logger.info(f'Mean response time: {mean_response_time:.4f} seconds')
    logger.info(f'Standard deviation of response time: {std_dev_response_time:.4f} seconds')

    # Since we do not have specific requirements for the mean and standard deviation of the response time,
    # let's assume that for the mean it is no more than 3.5 sec and for the standard deviation no more than 0.35 sec.
    assert mean_response_time < 3.5, 'Mean response time is too high'
    assert std_dev_response_time < 0.35, 'Standard deviation of response time is too high'
