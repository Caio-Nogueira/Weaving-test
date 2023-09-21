import unittest
from unittest.mock import patch, MagicMock
from weaving_analyser.velocity_handler import VelocityHandler

class TestVelocityHandler(unittest.TestCase):
    def setUp(self):
        self.velocity_handler = VelocityHandler()

    def test_handle_velocity(self):
        self.assertEqual(self.velocity_handler.handle_velocity(10), 10)

    def test_get_displacement(self):
        self.velocity_handler.velocity = 10
        self.assertEqual(self.velocity_handler.get_displacement(), 0.2)

    def test_noise(self):
        self.velocity_handler.velocity_buffer = [10, 10, 10, 10]
        self.assertLess(self.velocity_handler.handle_velocity(100), 100)

    @patch('hardware_controllers.velocity_sensor_controller.VelocitySensorController')
    def test_update(self, mock_velocity_sensor_controller):
        self.velocity_handler.velocity_sensor_controller = mock_velocity_sensor_controller
        mock_velocity_sensor_controller.get_velocity.return_value = 60
        self.velocity_handler.update()
        self.assertEqual(self.velocity_handler.velocity, 1)
        self.assertEqual(self.velocity_handler.total_displacement, 0.02)
