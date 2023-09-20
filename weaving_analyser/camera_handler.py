from hardware_controllers.cameras_controller import CamerasController, LightType
from threading import Thread
from config import info_logger

class CameraHandler(Thread):
    def __init__(self) -> None:
        super().__init__(name='camera_handler_thread')
        self.cameras_controller = CamerasController()
        self.cameras_controller.open_cameras()
    
    def __call__(self) -> None:
        # take pictures with both lights

        self.cameras_controller.trigger()
        green_pictures = self.cameras_controller.collect_pictures(LightType.GREEN)

        info_logger.log("Trigger with green light")
        
        self.cameras_controller.trigger()
        blue_pictures = self.cameras_controller.collect_pictures(LightType.BLUE)
        info_logger.log("Trigger with blue light")

        