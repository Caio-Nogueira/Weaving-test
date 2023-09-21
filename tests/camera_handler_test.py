import unittest
from unittest.mock import patch, MagicMock
from weaving_analyser.camera_handler import CameraHandler
from hardware_controllers.cameras_controller import LightType

class TestCameraHandler(unittest.TestCase):
    def setUp(self):
        self.camera_handler = CameraHandler()

    @patch('hardware_controllers.cameras_controller.CamerasController')
    def test_trigger_camera(self, mock_cameras_controller):
        self.camera_handler.cameras_controller = mock_cameras_controller
        mock_cameras_controller.collect_pictures.return_value = 'picture'
        self.assertEqual(self.camera_handler.trigger_camera(LightType.GREEN), 'picture')

    @patch('hardware_controllers.cameras_controller.CamerasController')
    @patch('weaving_analyser.camera_handler.APIhandler')
    def test_make_batch(self, mock_cameras_controller, mock_api_handler):
        self.camera_handler.cameras_controller = mock_cameras_controller
        self.camera_handler.api_handler = mock_api_handler
        mock_api_handler.prepare_body.return_value = 'body'
        mock_cameras_controller.collect_pictures.return_value = 'picture'
        self.assertEqual(self.camera_handler.make_batch(10, 10), ['body', 'body'])

    @patch('hardware_controllers.cameras_controller.CamerasController')
    def test_trigger_fail(self, mock_cameras_controller):
        self.camera_handler.cameras_controller = mock_cameras_controller
        mock_cameras_controller.trigger.return_value = False
        self.assertEqual(self.camera_handler.make_batch(10, 10), None)
