from hardware_controllers.cameras_controller import CamerasController, LightType

from .config import info_logger, error_logger, console_logger, debug_logger
from .api import APIhandler
from threading import Lock

class Observer:
    def update():
        pass

class CameraHandler(Observer):
    VERTICAL_FOV = 25

    def __init__(self) -> None:
        self.cameras_controller = CamerasController()
        self.api_handler = APIhandler()
        self.velocity, self.displacement = 0, 0
        self.camera_lock = Lock() # lock the camera to prevent multiple threads from accessing it at the same time

    def update(self, velocity: float, displacement: float) -> None:
        self.velocity, self.displacement = velocity, displacement
    
    def start(self) -> None:
        try:
            self.cameras_controller.open_cameras()
        except Exception as e:
            error_logger.error(f"Cameras failed to open: {e}")

    def trigger_camera(self, light_type: LightType) -> None:
        
        try:
            if not self.cameras_controller.trigger():
                raise Exception("Cameras were not triggered")
        
            picture = self.cameras_controller.collect_pictures(light_type)
            return picture
        except Exception as e:
            error_logger.error(f"Cameras failed to trigger: probably pictures were not collected: {e}")
            return None

    def make_batch(self) -> None:
        self.camera_lock.acquire()

        debug_logger.debug(f"Sending batch request.")
        velocity, displacement = self.velocity, self.displacement
        batch = []
        
        green = self.trigger_camera(LightType.GREEN)
        if green is None:
            return None
        
        batch.append(self.api_handler.prepare_body(green, velocity, displacement, LightType.GREEN))
        debug_logger.debug(f"Green picture collected.")
        
        blue = self.trigger_camera(LightType.BLUE)
        debug_logger.debug(f"Blue picture collected.")
        self.camera_lock.release()
        velocity, displacement = self.velocity, self.displacement
        info_logger.info("Sending batch request.")

        if blue is None:
            return None

        batch.append(self.api_handler.prepare_body(blue, velocity, displacement, LightType.BLUE))
        return batch


    def __call__(self) -> None:
        batch = self.make_batch()
        response = self.api_handler.send_pictures_batch(batch)
        return response


