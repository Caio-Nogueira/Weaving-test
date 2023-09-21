import requests
from typing import List
import time
from hardware_controllers.cameras_controller import LightType
from .config import error_logger, debug_logger
import base64
import numpy as np

light_dict = {
    LightType.GREEN: "green_light",
    LightType.BLUE: "blue_light"
}

class APIhandler:
    def __init__(self):
        self.domain = "127.0.0.1"
        self.port = 5000

        try:
            ping_response = self.ping()
        except requests.exceptions.ConnectionError as e:
            error_logger.error(f"API server failed or is not running.")
            raise Exception(f"API server failed or is not running.")

    def ping(self):
        url = f"http://{self.domain}:{self.port}/ping"
        response = requests.get(url)
        return response
    
    def encode_image(self, image: np.ndarray):
        return base64.b64encode(image)


    def prepare_body(self, light: np.ndarray, velocity: float, displacement: float, light_type: LightType):

        return {
            "light": light_dict[light_type],
            "creation_date": time.time(),
            "velocity": velocity,
            "displacement": displacement,
            "pictures": {
                "left:": {
                    "picture": self.encode_image(light[0]),
                    "iso": light[3],
                    "exposure_time": light[1],
                    "diaphragm_opening": light[2],
                    "picture_shape": light[0].shape
                    }
                },
                "right": {
                    "picture": self.encode_image(light[4]),
                    "iso": light[7],
                    "exposure_time": light[5],
                    "diaphragm_opening": light[6],
                    "picture_shape": light[4].shape
                }
        }
    
    def surface_movement_body(self, velocity: float, displacement: float):
        return {
            "velocity": velocity,
            "displacement": displacement
        }

    def send_pictures_batch(self, pictures_batch: List):
        url = f"http://{self.domain}:{self.port}/pictures_batch"
        data = {
            "lights": pictures_batch
        }
        response = requests.post(url, data=data)
        return response
    
    def send_surface_movement(self, velocity: float, displacement: float):
        url = f"http://{self.domain}:{self.port}/fabric_movement"
        response = requests.post(url, data=self.surface_movement_body(velocity, displacement))
        return response