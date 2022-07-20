#
#
#

import math

GRAVITY = 9.81

class ArmElement:

    def __init__(self, _length, _mass, _friction):
        self.w = 0.0
        self.theta = 0.0
        self.L = _length
        self.M = _mass
        self.b = _friction

    def evaluate(self, _input_torque, delta_t):
        self.w = self.w - GRAVITY * delta_t * math.cos(self.theta) - \
            (self.b * delta_t * self.w * self. L) / self.M + \
            delta_t * _input_torque / (self.M * self.L)
        self.theta = self.theta + delta_t * self.w

    def get_pose(self):
        return (self.L * math.cos(self.theta), self.L * math.sin(self.theta) )
