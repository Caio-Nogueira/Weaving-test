import requests
from typing import List
import time
from hardware_controllers.cameras_controller import LightType

light_dict = {
    LightType.GREEN: "green_light",
    LightType.BLUE: "blue_light"
}

class APIhandler():
    def __init__(self):
        self.domain = "127.0.0.1"
        self.port = 5000

    def prepare_body(self, light, velocity, displacement, light_type):
        return {
            "light": light_dict[light_type],
            "creation_date": time.time(),
            "velocity": velocity,
            "displacement": displacement,
            "pictures": {
                "left:": {
                    "picture": light[0].tolist(),
                    "iso": light[3],
                    "exposure_time": light[1],
                    "diaphragm_opening": light[2],
                    "picture_shape": light[0].shape
                    }
                },
                "right": {
                    "picture": light[4].tolist(),
                    "iso": light[7],
                    "exposure_time": light[5],
                    "diaphragm_opening": light[6],
                    "picture_shape": light[4].shape
                }
            
        }
    
    def surface_movement_body(velocity, displacement):
        return {
            "velocity": velocity,
            "displacement": displacement
        }

    def send_pictures_batch(self, pictures_batch):
        url = f"http://{self.domain}:{self.port}/pictures_batch"
        response = requests.post(url, data=pictures_batch)
        return response
    
    def send_surface_movement(self, velocity, displacement):
        url = f"http://{self.domain}:{self.port}/surface_movement"
        response = requests.post(url, data=self.surface_movement_body(velocity, displacement))
        return response