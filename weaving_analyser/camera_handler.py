from hardware_controllers.cameras_controller import CamerasController, LightType

from .config import info_logger, error_logger, console_logger, debug_logger
from .api import APIhandler
from .errors.pictures_not_collected_error import PicturesNotCollectedError
from threading import Lock

class Observer:
    """
    Observer is an abstract class that represents an observer.

    Methods
    -------
    update()
        Update the observer.
    """
    def update():
        pass

class CameraHandler(Observer):
    """CameraHandler is a class that handles the camera sensors and sends the pictures to the API.

    Attributes
    ----------
    _cameras_controller : CamerasController
        Instance of the cameras controller.
    _api_handler : APIhandler
        Instance of the API handler.
    velocity : float
        Current fabric velocity (cm/min).
    displacement : float
        Current fabric displacement (cm).
    camera_lock : Lock
        Lock the camera to prevent multiple threads from accessing it at the same time
    
    Methods
    -------
    update(velocity: float, displacement: float)
        Update the current fabric velocity and displacement.
    start()
        Start the cameras.
    trigger_camera(light_type: LightType)
        Trigger the cameras.
    make_batch()
        Make a batch of pictures. Pictures are taken sequentially.
    __call__()
        Call the CameraHandler to use the cameras and send the pictures to the API.

    """

    VERTICAL_FOV = 25

    def __init__(self) -> None:
        """
        Initialize the CameraHandler.

        Returns
        -------
        None
        """

        self.cameras_controller = CamerasController()
        self.api_handler = APIhandler()
        self.velocity, self.displacement = 0, 0
        self.camera_lock = Lock() # lock the camera to prevent multiple threads from accessing it at the same time

    def update(self, velocity: float, displacement: float) -> None:
        """
        Update the current fabric velocity and displacement.
        Args:
            velocity (float): velocity of the fabric
            displacement (float): displacement of the fabric

        Returns
        -------
        None
        """
        self.velocity, self.displacement = velocity, displacement
    
    def start(self) -> None:
        """
        Start the cameras.

        Returns
        -------
        None
        """
        try:
            self.cameras_controller.open_cameras()
        except Exception as e:
            error_logger.error(f"Cameras failed to open: {e}")

    def trigger_camera(self, light_type: LightType) -> None:
        
        """
        Trigger the cameras for an individual light type.

        Raises:
            PicturesNotCollectedError: Pictures were not collected.

        Returns:
            Tuple[np.ndarray, float, float, int, np.ndarray, float, float, int]
            Pictures and their metadata.
        """
        try:
            if not self.cameras_controller.trigger():
                raise PicturesNotCollectedError("Pictures were not collected.")
        
            picture = self.cameras_controller.collect_pictures(light_type)
            return picture
        except PicturesNotCollectedError as e:
            error_logger.error(f"Cameras failed to trigger: pictures were not collected: {e}")
            return None

    def make_batch(self) -> None:
        """
        Make a batch of pictures. Pictures are taken sequentially.

        Returns:
            List: List of pictures and their metadata.
        """

        self.camera_lock.acquire()

        debug_logger.debug(f"Sending batch request.")
        velocity, displacement = self.velocity, self.displacement
        batch = []
        
        green = self.trigger_camera(LightType.GREEN)
        if green is None:
            return None
        
        batch.append(self.api_handler.prepare_body(green, velocity, displacement, LightType.GREEN))
        info_logger.info(f"velocity: {velocity}, displacement: {displacement} after green picture.")
        debug_logger.debug(f"Green picture collected.")
        
        blue = self.trigger_camera(LightType.BLUE)
        debug_logger.debug(f"Blue picture collected.")
        self.camera_lock.release()
        info_logger.info(f"Displacement between pictures: {self.displacement - displacement}, ")
        velocity, displacement = self.velocity, self.displacement

        if blue is None:
            return None

        
        batch.append(self.api_handler.prepare_body(blue, velocity, displacement, LightType.BLUE))
        return batch


    def __call__(self) -> None:
        """
        Call the CameraHandler to use the cameras and send the pictures to the API.

        Returns:
            requests.Response: response from the API.
        """

        batch = self.make_batch()
        
        console_logger.info(f"Sending batch of pictures to API.")
        info_logger.info("Sending batch request to API.")
        
        response = self.api_handler.send_pictures_batch(batch)
        return response


