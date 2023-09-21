#! /usr/bin/env python3
from .config import console_logger, NUM_OF_WORKERS
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from signal import signal, SIGINT

# use the following line to import the hardware_controllers package from the parent directory
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .velocity_handler import VelocityHandler
from .camera_handler import CameraHandler

    
class WeavingAnalyzer:
    """
    WeavingAnalyzer is a class that handles the velocity and camera handlers.
    
    Attributes
    ----------
    velocity_handler : VelocityHandler
        Instance of the velocity handler.
    camera_handler : CameraHandler
        Instance of the camera handler.
    updateThread : Thread
        Thread that updates the velocity handler.
    threadPoolVelocity : ThreadPoolExecutor
        Thread pool for the velocity handler.
    threadPoolPictures : ThreadPoolExecutor
        Thread pool for the camera handler.
    _current_frame : int
        Current frame number.
    do_run : bool
        Whether the WeavingAnalyzer should run or not.

    Methods
    -------
    start(ttl: int)
        Start the WeavingAnalyzer.
    stop()
        Stop the WeavingAnalyzer.
    update()
        Update the velocity and camera handlers.
        
    """

    def __init__(self) -> None:
        """
        Initialize the WeavingAnalyzer.

        Returns
        -------
        None
        """

        self.do_run = False
        self.velocity_handler = VelocityHandler()
        self.camera_handler = CameraHandler()
        
        self.velocity_handler.register_observer(self.camera_handler)
        self.updateThread = Thread(target=self.update, name='update_thread', daemon=True)
        
        console_logger.info("WeavingAnalyzer initialized.")
        self.threadPoolVelocity = ThreadPoolExecutor(max_workers=50, thread_name_prefix='velocity_thread_')
        self.threadPoolPictures = ThreadPoolExecutor(max_workers=2, thread_name_prefix='picture_thread_')
        self.current_frame = 0
        


    def start(self, ttl=None) -> None:
        """
        Start the WeavingAnalyzer.

        Args:
            ttl (int, optional): time to live. Defaults to None.

        Returns
        -------
        None
        """

        console_logger.info("Starting handlers.")
        self.do_run = True
        self.velocity_handler.start()
        self.camera_handler.start()
        self.updateThread.start()
        
        if ttl is not None:
            time.sleep(ttl) 
            self.stop()
        
        
    def stop(self) -> None:
        """
        Stop the WeavingAnalyzer.

        Returns
        -------
        None
        """

        console_logger.info("Stopping all handlers.")
        self.do_run = False
        self.velocity_handler.stop()

        self.threadPoolVelocity.shutdown(wait=False)
        self.threadPoolPictures.shutdown(wait=False)
        self.updateThread.join()

    
    def update(self) -> None:
        """
        Update the velocity and camera handlers.

        Returns
        -------
        None
        """

        while self.do_run:
            start_time = time.time()
            
            self.velocity_handler.update()

            self.threadPoolVelocity.submit(self.velocity_handler)
            avg_total_disp = sum(self.velocity_handler.displacement_buffer) / len(self.velocity_handler.displacement_buffer)
            if (avg_total_disp // CameraHandler.VERTICAL_FOV) > self.current_frame: # displacement is large enough for a camera iteration
                self.current_frame += 1
                self.threadPoolPictures.submit(lambda: self.camera_handler())

            elapsed_time = time.time() - start_time
            sleep_duration = max(0, 1 / VelocityHandler.SAMPLING_RATE - elapsed_time) # account for the time taken to read the sensor
            time.sleep(sleep_duration)
