import unittest
from unittest.mock import patch, MagicMock
from weaving_analyser.velocity_handler import VelocityHandler
from weaving_analyser.camera_handler import CameraHandler
from weaving_analyser.api import APIhandler

class TestWeavingAnalyser(unittest.TestCase):
    def setUp(self):
        self.velocity_handler = VelocityHandler()
        self.camera_handler = CameraHandler()

    @patch.object(VelocityHandler, '__call__')
    def test_velocity_handler_call(self, mock_call):
        self.velocity_handler()
        mock_call.assert_called_once()

    @patch.object(CameraHandler, '__call__')
    def test_camera_handler_call(self, mock_call):
        self.camera_handler(10, 20)
        mock_call.assert_called_once_with(10, 20)