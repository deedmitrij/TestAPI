import json
import pytest

from app.api import FakeAPIHandler, FakeAPIServer
from app.logger import setup_logging
from config import TEST_DATA_PATH


@pytest.fixture(scope='session', autouse=True)
def _setup_logger():
    """Setup logging configuration."""
    setup_logging()


@pytest.fixture(scope='session')
def fake_server():
    """Setup Fake API server for testing."""
    # Start the fake server before tests are run
    fake_server = FakeAPIServer(FakeAPIHandler)
    fake_server.start()

    # Run the tests
    yield fake_server

    # Tear down the server after tests are finished
    fake_server.stop()


@pytest.fixture(scope="session")
def test_data():
    """Test data for the Fake API server."""
    # Load the test data from the file
    with open(TEST_DATA_PATH, 'r') as f:
        data = json.load(f)
        return data
