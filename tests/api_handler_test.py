import unittest
from unittest.mock import patch, MagicMock
from weaving_analyser.api import APIhandler

class TestAPIhandler(unittest.TestCase):
    def setUp(self):
        self.api_handler = APIhandler()

    @patch('requests.get')
    def test_ping(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertEqual(self.api_handler.ping().status_code, 200)

    @patch('requests.post')
    def test_send_pictures_batch(self, mock_post):
        mock_post.return_value.status_code = 200
        self.assertEqual(self.api_handler.send_pictures_batch('pictures_batch').status_code, 200)

    @patch('requests.post')
    def test_send_surface_movement(self, mock_post):
        mock_post.return_value.status_code = 200
        self.assertEqual(self.api_handler.send_surface_movement(10, 20).status_code, 200)