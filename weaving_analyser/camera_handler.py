from hardware_controllers.cameras_controller import CamerasController, LightType

from .config import info_logger, error_logger
from .api import APIhandler

class CameraHandler:
    VERTICAL_FOV = 25

    def __init__(self) -> None:
        self.cameras_controller = CamerasController()
        self.api_handler = APIhandler()

        self.start()
    
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

    def make_batch(self, velocity: float, displacement: float) -> None:
        batch = []
        green = self.trigger_camera(LightType.GREEN)
        blue = self.trigger_camera(LightType.BLUE)
        
        if green is None or blue is None:
            error_logger.error(f"Pictures were not collected")
            return

        batch.append(self.api_handler.prepare_body(green, velocity, displacement, LightType.GREEN))
        batch.append(self.api_handler.prepare_body(blue, velocity, displacement, LightType.BLUE))
        return batch

    def __call__(self, velocity: float, displacement: float) -> None:       
        batch = self.make_batch(velocity, displacement)
        info_logger.info(f"Sending batch request")
        response = self.api_handler.send_pictures_batch(batch)
        return response


