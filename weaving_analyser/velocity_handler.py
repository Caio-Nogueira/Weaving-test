from threading import Thread
from typing import List
from config import debug_logger, warning_logger, info_logger
from hardware_controllers.velocity_sensor_controller import VelocitySensorController
from api import APIhandler

ONE_HERTZ = 1

class VelocityHandler(Thread):
    SAMPLING_RATE = 50 * ONE_HERTZ
    WINDOW = 5
    total_displacement = 0

    def __init__(self) -> None:
        super().__init__(name='velocity_handler_thread')
        self._do_run = False
        self.velocity_sensor_controller = VelocitySensorController()
        self.total_displacement = 0
        self.velocity = 0
        self.api_handler = APIhandler()

    def start(self) -> None:
        self.velocity_sensor_controller.start_sensor()
    
    def stop(self) -> None:
        self.velocity_sensor_controller.stop_sensor()
    
    def handle_velocity(self, velocity_list: List, instant_velocity: int) -> float:
        # address noise in velocity readings by calculating the moving average velocity
        if instant_velocity < 0:
            warning_logger.warning(f"Negative velocity detected: {instant_velocity}")
        
        velocity_list.append(instant_velocity)
        
        if len(velocity_list) > VelocityHandler.WINDOW:
            velocity_list.pop(0)
        
        moving_average_velocity = sum(velocity_list) / len(velocity_list)
        return moving_average_velocity

    def get_displacement(self) -> float:
        return self.velocity / VelocityHandler.SAMPLING_RATE
    
    
    def update(self, velocity_buffer: List):

        instant_velocity = self.velocity_sensor_controller.get_velocity()
        self.velocity = self.handle_velocity(velocity_buffer, instant_velocity)
        self.total_displacement += self.get_displacement()

        debug_logger.debug(f"Total displacement: {self.total_displacement}; Moving average velocity: {self.velocity}; instant velocity: {instant_velocity}")


    def __call__(self):
        info_logger.info(f"Sending surface movement request")
        self.api_handler.send_surface_movement(self.velocity, self.total_displacement)