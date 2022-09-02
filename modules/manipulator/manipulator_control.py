import math
from lib.controllers.standard import *

class ArmControl:

    def __init__(self, arm, end_effector=False):
        self.arm = arm
        # self.speed_controller = PIDSat(kp=0.3, ki=10, kd=0, saturation=10, antiwindup=True) if self.arm.L < 0.03 else PIDSat(kp=200, ki=3, kd=0, saturation=10, antiwindup=True)
        # self.position_controller = PIDSat(kp=8, ki=0, kd=0, saturation=10, antiwindup=True)
        if not end_effector:
            self.speed_controller = PIDSat(kp=330, ki=50, kd=0, saturation=10, antiwindup=True)
            self.position_controller = PIDSat(kp=55, ki=0, kd=0, saturation=10, antiwindup=True)
        else:
            self.speed_controller = PIDSat(kp=2, ki=8, kd=0, saturation=10, antiwindup=True)  # todo: fare tuning
            self.position_controller = PIDSat(kp=55, ki=0, kd=0, saturation=5, antiwindup=True)
        self.theta_target = 0
        self.w_target = 0
        self.torque = 0

    def set_target(self, theta_target):
        self.theta_target = theta_target

    def evaluate(self, delta_t):
        self.w_target = self.position_controller.evaluate(delta_t, self.theta_target, self.arm.theta)
        self.torque = self.speed_controller.evaluate(delta_t, self.w_target, self.arm.w)
        self.arm.evaluate(self.torque, delta_t)

