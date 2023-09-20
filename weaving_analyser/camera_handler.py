from hardware_controllers.cameras_controller import CamerasController, LightType

from config import info_logger
from api import APIhandler

class CameraHandler:
    VERTICAL_FOV = 25

    def __init__(self) -> None:
        # super().__init__(name='camera_handler_thread')
        self.cameras_controller = CamerasController()
        self.cameras_controller.open_cameras()
        self.api_handler = APIhandler()
    
    

    def __call__(self, velocity, displacement) -> None:
        # take pictures with both lights
        
        batch = []
        self.cameras_controller.trigger()
        green_pictures = self.cameras_controller.collect_pictures(LightType.GREEN)

        batch.append(self.api_handler.prepare_body(green_pictures, velocity, displacement, LightType.GREEN))
        
        self.cameras_controller.trigger()
        blue_pictures = self.cameras_controller.collect_pictures(LightType.BLUE)

        batch.append(self.api_handler.prepare_body(blue_pictures, velocity, displacement, LightType.BLUE))
        info_logger.info(f"Sending batch request")

        response = self.api_handler.send_pictures_batch({"lights": batch})
        return response








