import time

from threading import Thread
from typing import List
from config import debug_logger, warning_logger
from hardware_controllers.velocity_sensor_controller import VelocitySensorController

ONE_HERTZ = 1

class VelocityHandler(Thread):
    SAMPLING_RATE = 50 * ONE_HERTZ
    WINDOW = 5
    total_displacement = 0

    def __init__(self, event) -> None:
        super().__init__(name='velocity_handler_thread')
        self._do_run = False
        self.velocity_sensor_controller = VelocitySensorController()
        self.event = event
        self.total_displacement = 0

    def stop(self) -> None:
        self._do_run = False
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

    def get_displacement(self, velocity: int) -> float:
        return velocity / VelocityHandler.SAMPLING_RATE
    
    def run(self):
        self._do_run = True
        self.velocity_sensor_controller.start_sensor()
        
        # create a circular buffer to store the last WINDOW velocities
        velocity_buffer = []
        
        while self.event.is_set() == False:

            start_time = time.time()
            
            instant_velocity = self.velocity_sensor_controller.get_velocity()
            velocity = self.handle_velocity(velocity_buffer, instant_velocity)
            
            self.total_displacement += self.get_displacement(velocity)

            elapsed_time = time.time() - start_time
            sleep_duration = max(0, 1 / VelocityHandler.SAMPLING_RATE - elapsed_time) # account for the time taken to read the sensor
            debug_logger.debug(f"Total displacement: {self.total_displacement}; Moving average velocity: {velocity}; instant velocity: {instant_velocity}; sleep duration: {sleep_duration}")

            time.sleep(sleep_duration)
