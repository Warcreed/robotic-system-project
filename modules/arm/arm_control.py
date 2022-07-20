import math
from lib.controllers.standard import *
from lib.controllers.profile_position_control import *

class ArmControl:

    def __init__(self, arm, use_profile):
        self.arm = arm
        self.use_profile = use_profile
        if self.arm.L < 0.03:
            self.speed_controller = PIDSat(kp=0.3, ki=10, kd=0, saturation=10)
        else:
            self.speed_controller = PIDSat(kp=10, ki=5, kd=0, saturation=10)
        if self.use_profile:
            self.position_controller = ProfilePositionController(6.0, 2.0, 2.0)
        else:
            self.position_controller = PIDSat(kp=15, ki=0, kd=0, saturation=10)
        self.target = 0
        self.w_target = 0

    def set_target(self, target):
        self.target = math.radians(target)

    def evaluate(self, delta_t):
        if self.use_profile:
            self.w_target = self.position_controller.evaluate(self.target, delta_t, self.arm.theta, self.arm.w, )
        else:
            self.w_target = self.position_controller.evaluate(delta_t, self.target, self.arm.theta)
        torque = self.speed_controller.evaluate(delta_t, self.w_target, self.arm.w)
        #print(">>", self, self.w_target, self.target)
        self.arm.evaluate(torque, delta_t)

