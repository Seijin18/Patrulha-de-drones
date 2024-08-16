from vision import Vision
from djitellopy import Tello

global imgContour
global dir;

class Rotes:
    def __init__(self):
        self.drone = Tello()
        self.drone.connect()
        print(self.drone.get_battery())
        #self.drone.takeoff()

    def begin_params(self):
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 0

    def begin_vision(self):
        self.drone.vision = Vision(self.drone)
        self.drone.vision.followFlag()

    def disconnect(self):
        self.drone.land()
        self.vision.disconnect_cam()
        self.drone.end()

    # def drone_rotate_clockwise(self, rotation):
    #     self.drone.rotate_clockwise(rotation)
    #     print("Drone rotate to the right side.")
    #
    # def drone_forward(self, distance: int):
    #     self.drone.move_forward(distance)
    #     print(f"Move {distance}cm forward.")
    #
    # def moviment(self, distance):
    #     if distance == 0:
    #         self.drone_rotate_clockwise(90)
    #     else:
    #         self.drone_forward(distance)
    #
    # def following_flag(self):
    #     while True:
    #         distance = self.vision.distance_to_flag()
    #         self.moviment(distance)
    #
    #         if waitKey(1) & 0xFF == ord('q'):
    #             break
    #         time.sleep(0.1)
