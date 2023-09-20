#! /usr/bin/env python3

"""
This is the "golden standard" of this test.
Golden Standard doesn't mean that it is the best implementation!
"""

from PIL import Image

# use the following line to import the hardware_controllers package from the parent directory
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from hardware_controllers.cameras_controller import CamerasController, LightType
from velocity_handler import VelocityHandler


class WeavingAnalyzer:
    def __init__(self) -> None:
        self.velocity_handler = VelocityHandler()
        print("Weaving Analyzer initialized.")

    def start(self) -> None:
        print("Starting all the handlers and runners.")
        # self.velocity_handler.start()
        self.test_cameras()
        print("All started!")

    def test_cameras(self):
        cameras_controller = CamerasController()
        cameras_controller.open_cameras()
        cameras_controller.trigger()
        green_pictures = cameras_controller.collect_pictures(LightType.GREEN)

        print('*** GREEN LIGHT ***')
        print('Left picture:')
        print(f'· iso: {green_pictures[3]}')
        print(f'· exposure time: {green_pictures[1]}')
        print(f'· diaphragm opening: {green_pictures[2]}')
        print(f'· picture shape: {green_pictures[0].shape}')
        green_left_picture = Image.fromarray(green_pictures[0])
        green_left_picture.show()
        print('Right picture:')
        print(f'· iso: {green_pictures[7]}')
        print(f'· exposure time: {green_pictures[5]}')
        print(f'· diaphragm opening: {green_pictures[6]}')
        print(f'· picture shape: {green_pictures[4].shape}')
        green_left_picture = Image.fromarray(green_pictures[4])
        green_left_picture.show()


def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    weaving_analyzer.start()


if __name__ == '__main__':
    main()
