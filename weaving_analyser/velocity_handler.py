from .config import debug_logger, warning_logger, info_logger
from hardware_controllers.velocity_sensor_controller import VelocitySensorController
from .api import APIhandler

ONE_HERTZ = 1

class VelocityHandler:
    SAMPLING_RATE = 50 * ONE_HERTZ
    WINDOW = 5
    total_displacement = 0

    def __init__(self) -> None:
        self._do_run = False
        self.velocity_sensor_controller = VelocitySensorController()
        self.total_displacement = 0
        self.velocity = 0
        self.api_handler = APIhandler()
        self.velocity_buffer = []
        self.displacement_buffer = []


    def start(self) -> None:
        self.velocity_sensor_controller.start_sensor()
    
    def stop(self) -> None:
        self.velocity_sensor_controller.stop_sensor()
    
    def handle_velocity(self, instant_velocity: float) -> float:
        # address noise in velocity readings by calculating the moving average velocity
        if instant_velocity < 0:
            warning_logger.warning(f"Negative velocity detected: {instant_velocity}")
        
        self.velocity_buffer.append(instant_velocity)
        
        if len(self.velocity_buffer) > VelocityHandler.WINDOW:
            self.velocity_buffer.pop(0)
        
        moving_average_velocity = sum(self.velocity_buffer) / len(self.velocity_buffer)
        return moving_average_velocity

    
    def get_displacement(self) -> float:
        return self.velocity / VelocityHandler.SAMPLING_RATE
    
    
    def update(self):

        instant_velocity = self.velocity_sensor_controller.get_velocity() # TODO: CATCH SENSOR EXCEPTIONS
        self.velocity = self.handle_velocity(instant_velocity)
        
        self.total_displacement += self.get_displacement()
        self.displacement_buffer.append(self.total_displacement)

        if len(self.displacement_buffer) > VelocityHandler.WINDOW:
            self.displacement_buffer.pop(0)
            
        debug_logger.debug(f"Total displacement: {self.total_displacement}; Moving average velocity: {self.velocity}; instant velocity: {instant_velocity}")


    def __call__(self):
        self.api_handler.send_surface_movement(self.velocity, self.total_displacement)