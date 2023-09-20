#! /usr/bin/env python3
from PIL import Image


# use the following line to import the hardware_controllers package from the parent directory
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from velocity_handler import VelocityHandler

class WeavingAnalyzer:
    def __init__(self) -> None:
        self.velocity_handler = VelocityHandler()
        print("Weaving Analyzer initialized.")

    def start(self) -> None:
        print("Starting all the handlers and runners.")
        self.velocity_handler.start()
        print("All started!")

   
def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    weaving_analyzer.start()


if __name__ == '__main__':
    main()
