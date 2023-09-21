from .config import debug_logger, warning_logger, info_logger
from hardware_controllers.velocity_sensor_controller import VelocitySensorController
from .api import APIhandler
from typing import Any

ONE_HERTZ = 1

class VelocityHandler:
    """
    VelocityHandler is a class that handles the velocity sensor and sends the velocity to the API.

    Attributes
    ----------
    SAMPLING_RATE : int
        Sampling rate of the velocity sensor (Hz).
    WINDOW : int
        Window size for the moving average velocity.
    total_displacement : float
        Total displacement of the fabric (cm).
    _displacement_threshold : float
        Threshold for the total displacement (cm).
    _velocity : float
        Current fabric velocity (cm/sec).
    _velocity_sensor_controller : VelocitySensorController
        Instance of the velocity sensor controller.
    api_handler : APIhandler
        Instance of the API handler.
    _velocity_buffer : List
        Buffer for the moving average velocity.
    _displacement_buffer : List
        Buffer for the total displacement.
    _observers : List
        List of observers.

    Methods
    -------
    register_observer(observer)
        Register an observer.
    _notify_observers()
        Notify the observers.
    start()
        Start the velocity sensor.
    stop()
        Stop the velocity sensor.
    handle_velocity(instant_velocity: float)
        Handle the velocity readings. Smooths the velocity readings using a moving average.
    get_displacement()
        Get the displacement.
    update()
        Update the velocity handler.
    __call__()
        Call the VelocityHandler to use the velocity sensor and send the velocity data to the API.

    """
    SAMPLING_RATE = 50 * ONE_HERTZ
    WINDOW = 5
    total_displacement = 0

    def __init__(self) -> None:
        """
        Initialize the VelocityHandler.
        """
        self._do_run = False
        self.velocity_sensor_controller = VelocitySensorController()
        self.total_displacement = 0
        self.displacement_threshold = 5
        self.velocity = 0
        self.api_handler = APIhandler()
        self.velocity_buffer = []
        self.displacement_buffer = []
        self.observers = []

    def register_observer(self, observer: Any) -> None:
        """
        Register an observer.

        Args:
            observer (any): observer that updates information from the velocity handler.
        """
        self.observers.append(observer)

    def notify_observers(self) -> None:
        """
        Notify the observers.

        Returns
        -------
        None
        """
        for observer in self.observers:
            observer.update(self.velocity, self.total_displacement)

    def start(self) -> None:
        """
        Start the velocity sensor.

        Returns
        -------
        None
        """
        self.velocity_sensor_controller.start_sensor()
    
    def stop(self) -> None:
        """
        Stop the velocity sensor.

        Returns
        -------
        None
        """
        self.velocity_sensor_controller.stop_sensor()
    
    def handle_velocity(self, instant_velocity: float) -> float:
        """
        Handle the velocity readings. Smooths the velocity readings using a moving average.

        Args:
            instant_velocity (float): instant velocity from the velocity sensor.

        Returns:
            float: moving average velocity.
        """
        if instant_velocity < 0:
            warning_logger.warning(f"Negative velocity detected: {instant_velocity}")
        
        self.velocity_buffer.append(instant_velocity)
        
        if len(self.velocity_buffer) > VelocityHandler.WINDOW:
            self.velocity_buffer.pop(0)
        
        moving_average_velocity = sum(self.velocity_buffer) / len(self.velocity_buffer)
        return moving_average_velocity

    
    def get_displacement(self) -> float:
        """
        Calculate the displacement based on the velocity.

        Returns:
            float: displacement.
        """
        return self.velocity / VelocityHandler.SAMPLING_RATE
    
    
    def update(self) -> None:
        """
        Update the velocity handler.

        Returns
        -------
        None
        """
        instant_velocity = self.velocity_sensor_controller.get_velocity() / 60 # convert from cm/min to cm/sec
        self.velocity = self.handle_velocity(instant_velocity)
        
        self.total_displacement += self.get_displacement()
        self.displacement_buffer.append(self.total_displacement)

        if len(self.displacement_buffer) > VelocityHandler.WINDOW:
            self.displacement_buffer.pop(0)
        
        if self.total_displacement > self.displacement_threshold:
            info_logger.info(f"Total displacement reached: {self.displacement_threshold}")
            self.displacement_threshold += 5

        self.notify_observers()
        debug_logger.debug(f"Total displacement: {self.total_displacement}; Moving average velocity: {self.velocity}; instant velocity: {instant_velocity}")


    def __call__(self) -> None:
        """
        Call the VelocityHandler to use the velocity sensor and send the velocity data to the API.

        Returns
        -------
        None
        """
        self.api_handler.send_surface_movement(self.velocity, self.total_displacement)