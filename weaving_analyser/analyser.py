#! /usr/bin/env python3
from PIL import Image
from config import console_logger, info_logger
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
        self.do_run = False
        self.velocity_handler = VelocityHandler()
        self.camera_handler = CameraHandler()
        
        self.cameraThread = Thread(target=self.handle_cameras, name='camera_thread')
        self.velocityThread = Thread(target=self.handle_velocity, name='velocity_thread')
        
        console_logger.info("WeavingAnalyzer initialized.")
        
        self.threadPool = ThreadPoolExecutor(max_workers=16)

    def start(self) -> None:
        console_logger.info("Starting handlers.")
        self.do_run = True
        self.velocity_handler.start()
        self.velocityThread.start()
        self.cameraThread.start()
        
        time.sleep(10) #! PROGRAM RUNS FOR 10 SECONDS 
        
        self.stop()
        
    
    def stop(self) -> None:
        console_logger.info("Stopping all handlers.")
        self.do_run = False
        self.velocity_handler.stop()

    
    def handle_velocity(self) -> None:
        velocity_buffer = []
        while self.do_run:
            start_time = time.time()
            
            self.velocity_handler.update(velocity_buffer)
            elapsed_time = time.time() - start_time

            self.threadPool.submit(self.velocity_handler)

            sleep_duration = max(0, 1 / VelocityHandler.SAMPLING_RATE - elapsed_time) # account for the time taken to read the sensor
            time.sleep(sleep_duration)

    
    def handle_cameras(self) -> None:
        current_frame = 0
        while self.do_run:
            if (self.velocity_handler.total_displacement // CameraHandler.VERTICAL_FOV) > current_frame: # displacement is large enough for a camera iteration
                current_frame += 1
                future = self.threadPool.submit(lambda: self.camera_handler(self.velocity_handler.velocity, self.velocity_handler.total_displacement))

   

def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    weaving_analyzer.start()


if __name__ == '__main__':
    main()
