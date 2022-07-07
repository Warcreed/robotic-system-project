#
# test_manipulator_pos.py
#

import sys
sys.path.insert(0, './lib')

from models.manipulator import *
from models.robot import *
from models.inputs import *
from models.virtual_robot import *
from controllers.standard import *
from controllers.control2d import *
from data.plot import *
from gui.three_joints_gui import *

from PyQt5.QtWidgets import QApplication

class ManipulatorRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3) # delta_t = 1e-3
        self.arm = ThreeJointsPlanarArm(0.2, 0.2, 0.02,
                                        0.5, 0.5, 0.5,
                                        0.8)

        # joint 1
        self.speed_control_1 = PIDSat(kp=400, ki=100, kd=0,
                                        saturation=20, antiwindup=True) # 20Nm max torque, antiwindup

        # joint 2
        self.speed_control_2 = PIDSat(300, 100, 0,
                                        20, True) # 20Nm max torque, antiwindup

        # joint 3
        self.speed_control_3 = PIDSat(10, 4, 0,
                                        20, True) # 20Nm max torque, antiwindup

        self.pos_control_1 = PIDSat(50, 0, 0, 5) # 2 rad/s max speed
        self.pos_control_2 = PIDSat(50, 0, 0, 5) # 2 rad/s max speed
        self.pos_control_3 = PIDSat(50, 0, 0, 5) # 2 rad/s max speed


        self.path_controller = Path2DManipulator(1.0, 0.2, 0.2, 0.01)
        self.path = [   (0.1, 0.1),
                        (0.1, 0.2),
                        (0.2, 0.215),
                        (0.0, 0.3) ]
        self.path_controller.set_path( self.path.copy() )
        (x, y, _) = self.arm.get_pose()
        self.path_controller.start( (x,y) )

        self.plotter = DataPlotter()

        self.target_alpha = math.radians(0.2)

    def run(self):

        pose = self.arm.get_pose()

        target_coords = self.path_controller.evaluate(self.delta_t, pose)
        if target_coords is None:
            self.plotter.plot( [ 't', 'Time' ],
                               [ [ 'Theta_ref', 'Theta Ref'] , [ 'Theta', 'Theta' ] ])
            self.plotter.plot( [ 't', 'Time' ],
                               [ [ 'w', 'W']  ])
            self.plotter.plot( [ 't', 'Time' ],
                               [ [ 'torque1', 'torque1']  ])
            self.plotter.plot( [ 't', 'Time' ],
                               [ [ 'torque2', 'torque2']  ])
            self.plotter.plot( [ 't', 'Time' ],
                               [ [ 'torque3', 'torque3']  ])
           # self.plotter.show()
            return False
        
        (self.theta1, self.theta2, self.theta3) = self.arm.inverse_kinematics(target_coords[0], target_coords[1], self.target_alpha)
        
        if self.theta1 is None:
            print("Target not reachable")
            return False
        wref_1 = self.pos_control_1.evaluate(self.delta_t, self.theta1, self.arm.element_1.theta)
        wref_2 = self.pos_control_2.evaluate(self.delta_t, self.theta2, self.arm.element_2.theta)
        wref_3 = self.pos_control_3.evaluate(self.delta_t, self.theta3, self.arm.element_3.theta)

        torque1 = self.speed_control_1.evaluate(self.delta_t, wref_1, self.arm.element_1.w)
        torque2 = self.speed_control_2.evaluate(self.delta_t, wref_2, self.arm.element_2.w)
        torque3 = self.speed_control_3.evaluate(self.delta_t, wref_3, self.arm.element_3.w)

        self.arm.evaluate(self.delta_t, torque1, torque2, torque3)

        (xr, yr, ar) = self.arm.get_pose()

        self.plotter.add('Theta_ref', self.theta3)
        self.plotter.add('Theta', self.arm.element_3.theta)
        self.plotter.add('w', wref_3)

        self.plotter.add('torque1', torque1) 
        self.plotter.add('torque2', torque2)
        self.plotter.add('torque3', torque3)
        self.plotter.add('t', self.t)

        # self.plotter.add('x', xr)
        # self.plotter.add('y', yr)
 
        # if self.t > 4:
        #     self.plotter.plot( [ 'x', 'X' ],
        #                        [ [ 'y', 'Y']  ])
        #     self.plotter.show()
        #     return False
        # else:
        #     return True
        return True

    def get_joint_positions(self):
        return self.arm.get_joint_positions()

    def get_pose_degrees(self):
        return self.arm.get_pose_degrees()

    def getPath(self):
        return self.path



if __name__ == '__main__':
    robot = ManipulatorRobot()
    app = QApplication(sys.argv)
    ex = ManipulatorWindow(robot)
    sys.exit(app.exec_())
