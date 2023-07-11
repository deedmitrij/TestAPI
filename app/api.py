import json
import random
import threading
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
from app.logger import logger
from config import TEST_DATA_PATH


class FakeAPIHandler(BaseHTTPRequestHandler):
    """Fake API handler."""

    delay = False

    @classmethod
    def set_delay(cls, delay):
        """
        Set the delay.

        :param delay: bool, True to incur a delay per request, False otherwise
        """
        cls.delay = delay

    def _set_headers(self, response_code=200):
        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        logger.info(f"Received GET request - URL: {self.path}")

        path_components = self.path.strip('/').split('/')
        if len(path_components) == 2:
            category, item_id = path_components
            # Load the data from the file
            with open(TEST_DATA_PATH, 'r') as f:
                data = json.load(f)
            if category in data and item_id in data[category]:
                self._set_headers()
                if self.delay:
                    # Incur a random delay (between 0.5 and 1.5 seconds)
                    time.sleep(random.uniform(0.5, 1.5))
                self.wfile.write(json.dumps(data[category][item_id]).encode())
            else:
                logger.warning(f"ID not found - URL: {self.path}")
                self._set_headers(404)
                error_response = {
                    "error": "ID not found"
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            logger.warning(f"Invalid URL format - URL: {self.path}")
            self._set_headers(404)
            error_response = {
                "error": "Invalid URL format"
            }
            self.wfile.write(json.dumps(error_response).encode())


class FakeAPIServer:
    """Fake API server."""
    def __init__(self, handler):
        host = 'localhost'
        port = 8000
        self.handler = handler
        self.server = HTTPServer((host, port), self.handler)
        self.address = f'http://{host}:{port}'
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def start(self):
        """Start the server."""
        self.thread.start()

    def stop(self):
        """Stop the server."""
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
