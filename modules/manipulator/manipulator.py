import math
from lib.models.arm_model import *
from .manipulator_control import *
from modules.utils.trajectory import *
from lib.data.geometry import *
from modules.utils.pose import *

class ThreeJointsArm:

    def __init__(self, trajectory_controller):
        self.element_1_model = ArmElement(_length = 0.2, _mass = 0.8 + 0.8 + 0.1, _friction = 8e-5)
        self.element_1_control = ArmControl(self.element_1_model, base_joint=True)
        self.element_2_model = ArmElement(_length = 0.2, _mass = 0.8 + 0.1, _friction = 8e-5)
        self.element_2_control = ArmControl(self.element_2_model)
        self.element_3_model = ArmElement(_length = 0.02, _mass = 0.1, _friction = 8e-5)
        self.element_3_control = ArmControl(self.element_3_model)
        self.trajectory = trajectory_controller
        self.trajectory.arm = self
        self.pose = Pose(0.1, 0.1, -90)
        self.theta1 = 0
        self.theta2 = 0
        self.theta3 = 0

    def set_target(self, theta1, theta2, theta3):
        self.element_1_control.set_target(theta1)
        self.element_2_control.set_target(theta2)
        self.element_3_control.set_target(theta3)

    def evaluate(self, delta_t):
        self.element_1_control.evaluate(delta_t)
        self.element_2_control.evaluate(delta_t)
        self.element_3_control.evaluate(delta_t)

    def get_pose_degrees(self):
        return ( math.degrees(self.element_1_model.theta),
                 math.degrees(self.element_2_model.theta),
                 math.degrees(self.element_3_model.theta) )

    def get_pose(self):
        (x1, y1) = self.element_1_model.get_pose()

        (_x2, _y2) = self.element_2_model.get_pose()
        (x2, y2) = local_to_global(x1, y1, self.element_1_model.theta, _x2, _y2)

        alpha = self.element_1_model.theta + self.element_2_model.theta + self.element_3_model.theta
        (x3, y3) = local_to_global(x2, y2, alpha, self.element_3_model.L, 0)

        return [    (x1, y1), 
                    (x2, y2), 
                    (x3, y3) ]

    def get_pose_xy_a(self):
        (x1, y1) = self.element_1_model.get_pose()

        (_x2, _y2) = self.element_2_model.get_pose()
        (x2, y2) = local_to_global(x1, y1, self.element_1_model.theta, _x2, _y2)

        alpha = self.element_1_model.theta + self.element_2_model.theta + self.element_3_model.theta

        self.pose.set_pose(x2, y2, alpha)

        return self.pose.get_pose()

    def inverse_kinematics(self, xt, yt, alpha):
        atan_den = (xt**2 + yt ** 2 - self.element_1_model.L ** 2 - self.element_2_model.L ** 2) / (2 * self.element_1_model.L * self.element_2_model.L )
        arg = 1 - atan_den**2
        if arg < 0:
            return (None, None, None)
        # theta2 = math.atan2( - math.sqrt( arg ), atan_den ) if xt >= 0 else math.atan2( + math.sqrt( arg ), atan_den )
        theta2 = math.atan2( - math.sqrt( arg ), atan_den ) 
        theta1 = math.atan2(yt, xt) - math.atan2(self.element_2_model.L * math.sin(theta2),
                                                 self.element_1_model.L + self.element_2_model.L * math.cos(theta2) )
        theta3 = math.radians(alpha) - theta1 - theta2
        return (theta1, theta2, theta3)

    def set_target_xy_a(self, x_target, y_target, a_target):
        (x_current, y_current, a_current) = self.get_pose_xy_a()
        # self.trajectory.set_target(p[1][0], p[1][1], alpha, x, y, math.radians(a))
        self.trajectory.set_target((x_current, y_current), (x_target, y_target), a_target)

    def evaluate_trajectory(self, delta_t):
        (trajectory_x, trajectory_y, trajectory_a) = self.trajectory.evaluate(delta_t)
        (self.theta1, self.theta2, self.theta3) = self.inverse_kinematics(trajectory_x, trajectory_y, trajectory_a)
        if self.theta1 is not None:
            self.set_target(self.theta1, self.theta2, self.theta3)
        self.evaluate(delta_t)

