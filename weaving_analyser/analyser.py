#! /usr/bin/env python3
from PIL import Image
from config import console_logger, info_logger,VERTICAL_FOV
import time
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor

# use the following line to import the hardware_controllers package from the parent directory
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from velocity_handler import VelocityHandler
from camera_handler import CameraHandler

    
class WeavingAnalyzer:

    def __init__(self) -> None:
        self.event = Event()
        self.velocity_handler = VelocityHandler(self.event)
        self.camera_handler = CameraHandler()
        self.cameraThread = Thread(target=self.handle_cameras,name='camera_thread')
        console_logger.info("WeavingAnalyzer initialized.")
        self.threadPool = ThreadPoolExecutor(max_workers=2)

    def start(self) -> None:
        console_logger.info("Starting velocity handler.")
        self.velocity_handler.start()
        self.cameraThread.start()
        
        time.sleep(10) #*TODO: REMOVE THIS 
        self.stop()
        
    
    def stop(self) -> None:
        console_logger.info("Stopping velocity handler.")
        self.event.set()

    def handle_cameras(self) -> None:
        current_frame = 0
        while self.event.is_set() == False:
            if (self.velocity_handler.total_displacement / VERTICAL_FOV) > current_frame: # displacement is large enough for a camera iteration
                current_frame += 1
                info_logger.info(f"Current frame: {current_frame}")
                future = self.threadPool.submit(self.camera_handler)

   

def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    weaving_analyzer.start()


if __name__ == '__main__':
    main()
