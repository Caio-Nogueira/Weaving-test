import requests
from typing import List
import time
from hardware_controllers.cameras_controller import LightType
from .config import light_dict
import base64
import numpy as np

class APIhandler:
    """
    APIhandler is a class that handles the communication with the API.

    Attributes
    ----------
    domain : str
        Domain of the API.
    port : int
        Port of the API.

    Methods
    -------
    ping()
        Ping the API.
    encode_image(image: np.ndarray)
        Encode an image to base64.
    prepare_body(light: np.ndarray, velocity: float, displacement: float, light_type: LightType)
        Prepare the body of the request to the API.
    surface_movement_body(velocity: float, displacement: float)
        Prepare the body of the request to the API.
    send_surface_movement(velocity: float, displacement: float)
        Send the surface movement to the API.    
    send_pictures_batch(pictures_batch: List)
        Send a batch of pictures to the API.

    """

    def __init__(self):
        """
        Initialize the APIhandler.

        Returns
        -------
        None
        """

        self.domain = "127.0.0.1"
        self.port = 5000


    def ping(self):
        """
        Ping the API.

        Returns:
            requests.Response: response from the API.
        """
        url = f"http://{self.domain}:{self.port}/ping"
        response = requests.get(url)
        return response
    
    def encode_image(self, image: np.ndarray):
        """
        Encode an image to base64.

        Args:
            image (np.ndarray): image array

        Returns:
            bytes: base64 encoded image.
        """
        return base64.b64encode(image)


    def prepare_body(self, light: np.ndarray, velocity: float, displacement: float, light_type: LightType) -> dict:

        """
        Prepare the body of the request to the API.

        Returns:
            Dict: body of the request.
        """
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
    
    def surface_movement_body(self, velocity: float, displacement: float) -> dict:
        """
        Prepare the body of the request to the API.

        Args:
            velocity (float): velocity of the surface.
            displacement (float): displacement of the surface.

        Returns:
            dict: body of the request.
        """
        return {
            "velocity": velocity,
            "displacement": displacement
        }

    def send_pictures_batch(self, pictures_batch: List) -> requests.Response:
        """
        Send a batch of pictures to the API.

        Args:
            pictures_batch (List): batch of pictures.

        Returns:
            requests.Response: response from the API.
        """
        url = f"http://{self.domain}:{self.port}/pictures_batch"
        data = {
            "lights": pictures_batch
        }
        response = requests.post(url, data=data)
        return response
    
    def send_surface_movement(self, velocity: float, displacement: float) -> requests.Response:
        """
        Send the surface movement to the API.

        Args:
            velocity (float): velocity of the surface.
            displacement (float): displacement of the surface.

        Returns:
            requests.Response: response from the API.
        """
        url = f"http://{self.domain}:{self.port}/fabric_movement"
        response = requests.post(url, data=self.surface_movement_body(velocity, displacement))
        return response