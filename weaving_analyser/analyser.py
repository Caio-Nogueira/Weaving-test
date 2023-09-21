#! /usr/bin/env python3
from PIL import Image
from .config import console_logger, NUM_OF_WORKERS
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

# use the following line to import the hardware_controllers package from the parent directory
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .velocity_handler import VelocityHandler
from .camera_handler import CameraHandler

    
class WeavingAnalyzer:

    def __init__(self) -> None:
        self.do_run = False
        self.velocity_handler = VelocityHandler()
        self.camera_handler = CameraHandler()
        self.velocityThread = Thread(target=self.handle_velocity, name='velocity_thread')
        
        console_logger.info("WeavingAnalyzer initialized.")
        self.threadPoolVelocity = ThreadPoolExecutor(max_workers=50)
        self.threadPoolPictures = ThreadPoolExecutor(max_workers=16)

        self.current_frame = 0
        

    def start(self, ttl: int) -> None:
        console_logger.info("Starting handlers.")
        self.do_run = True
        self.velocity_handler.start()
        self.velocityThread.start()
        
        if ttl:
            time.sleep(ttl) 
            self.stop()
        
        
    def stop(self) -> None:
        console_logger.info("Stopping all handlers.")
        self.do_run = False
        self.velocity_handler.stop()

    
    def handle_velocity(self) -> None:
        
        while self.do_run:
            start_time = time.time()
            
            self.velocity_handler.update()

            self.threadPoolVelocity.submit(self.velocity_handler)
            
            avg_total_disp = sum(self.velocity_handler.displacement_buffer) / len(self.velocity_handler.displacement_buffer)
            if (avg_total_disp // CameraHandler.VERTICAL_FOV) > self.current_frame: # displacement is large enough for a camera iteration
                self.current_frame += 1
                self.threadPoolPictures.submit(lambda: self.camera_handler(self.velocity_handler.velocity, self.velocity_handler.total_displacement))

            elapsed_time = time.time() - start_time
            sleep_duration = max(0, 1 / VelocityHandler.SAMPLING_RATE - elapsed_time) # account for the time taken to read the sensor
            time.sleep(sleep_duration)



def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    weaving_analyzer.start()


if __name__ == '__main__':
    main()
