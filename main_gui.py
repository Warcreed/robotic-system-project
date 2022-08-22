#
#
#

import sys

sys.path.insert(0, './lib')
sys.path.insert(0, './modules')

import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget

from modules.manipulator.manipulator import *
from modules.manipulator.manipulator_painters import *
from modules.utils.telemetry import *
from modules.utils.path_planning import *
from modules.world.world import *
from modules.phidias.phidias_interface import *

COLOR_NAMES = [ 'red',
                'green',
                'blue',
                ]

# TODO: far preferire la strada di fronte alla cella di arrivo, se possibile
# TODO: rendere smooth il passaggio tra le spezzate
# TODO: controllare il movimento end effector
# TODO: 

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Robotic Arm Project - Danilo Santitto')
        self.show()

        self.delta_t = 1e-3 # 10ms of time-tick
        self.t = 0

        self.trajectory = Path2DManipulator(_vmax = 1.0, _acc = 0.5, _dec = 0.5, _distance_threshold=0.01, _alpha_threshold=0.01)

        self.arm = ThreeJointsArm(self.trajectory)
        self.arm_painter = ThreeJointsArmPainter(self.arm)

        self.world = World(self)
        self.px_world_height = Pose.pixel_scale(World.HEIGHT)
        self.px_world_width = Pose.pixel_scale(World.WIDTH)
        self.px_world_floor_level = Pose.pixel_scale(World.FLOOR_LEVEL)

        self.telemetry = Telemetry()
        self.seconds_after_show_telemetry = 10

        self._timer_painter = QtCore.QTimer(self)
        self._timer_painter.timeout.connect(self.go)
        self._timer_painter.start(int(self.delta_t * 1000))
        self.notification = False

        self._phidias_agent = None

        self.block_poses = [
            Pose(0.095, 0.0676, 0),
            Pose(0.235, 0.032, -90),
            Pose(0.275, 0.032, -90),
            Pose(0.265, 0.11, 0),
            Pose(0.265, 0.19, 0),
            Pose(0.275, 0.215, 100),
            Pose(0.175, 0.295, 0),
            Pose(0.155, 0.3, 70),
            Pose(0.11, 0.28, 65),
            Pose(0.09, 0.27, 130),            
        ]
        self.nf1 = NF1(40)
        self.nf1.set_is_obstacle_for_world_matrix(self.world.get_obstacles())
        self.nf1.set_bowl_as_obstacle_for_world_matrix(self.world.get_bowl())
        self.target_alpha_deg = 0

        target_x = 0.1
        target_y = 0.15
        target_alpha = -90
        self.arm.set_path([ (target_x, target_y, target_alpha) ])
        self.arm.start()

        # print check

        ## Manipulator
        self.print_end_effector_ray = True

        ## telemetry
        self.show_telemetry = False
        self.print_telemetry_base_joint= True
        self.print_telemetry_second_joint= False
        self.print_telemetry_end_eff_joint= False

        ## obstacles
        self.print_block_slots = True
        self.print_scaled_obstacle = False
        
        ## NF1
        self.print_nf1 = True
        self.print_nf1_map = False
        self.print_nf1_obstacle = False
        self.print_nf1_map_values = False
        self.print_nf1_coord = False
        self.print_nf1_path = True

    def set_phidias_agent(self, _phidias_agent):
        self._phidias_agent = _phidias_agent

    def go_to(self,target_x, target_y, target_alpha):
        self.notification = False
        self.target_alpha_deg = target_alpha
        self.nf1.run_nf1_for_taget_xy(target_x, target_y)
        self._build_path(self.target_alpha_deg)
        self.arm.start()
    
    def go_to_block_slot(self, block_index):
        self.notification = False
        (target_x, target_y, self.target_alpha_deg) = self.block_poses[block_index].get_pose()
        self.nf1.run_nf1_for_taget_xy(target_x, target_y)
        self._build_path(self.target_alpha_deg)
        self.arm.start()

    def _build_path(self, target_alpha):
        (x, y, a) = self.arm.get_pose_xy_a()
        path = self.nf1.build_path(x, y, a, target_alpha)
        self.arm.set_path(path.copy())

    def sense_block_presence(self): #da sistemare
        if self._phidias_agent is not None:
            d = self.world.sense_block_presence()
            params = [d]
            Messaging.send_belief(self._phidias_agent, 'is_block_present', params, 'robot')

    def generate_new_block(self):
        if self.world.count_blocks() == 6:
            return
        self.world.new_block(random.choice(COLOR_NAMES))

    def notify_target_got(self):
        self.notification = True     
        if self._phidias_agent is not None:
            Messaging.send_belief(self._phidias_agent, 'target_got', [], 'robot')
   
    def sense_color(self):
        if self._phidias_agent is not None:
            d = self.world.sense_color()
            params = [] if d is None else [d]
            Messaging.send_belief(self._phidias_agent, 'color', params, 'robot')
    
    def collect_block(self):
        if self._phidias_agent is not None:
            self.world.collect_block()
            Messaging.send_belief(self._phidias_agent, 'block_collected', [], 'robot')
    
    def drop_block(self):
        if self._phidias_agent is not None:
            self.world.drop_block()
            Messaging.send_belief(self._phidias_agent, 'block_dropped', [], 'robot')
    
    def go(self):
        if self.show_telemetry:
            self.evaluate_telemetry()

        if self.trajectory.path_active:
            if self.trajectory.target_got:
                if not(self.notification):
                    self.notify_target_got()
                self.trajectory.target_got = False
                self.trajectory.path_active = False
            else:
                self.arm.evaluate_trajectory(self.delta_t)

        self.t += self.delta_t
        self.update() # repaint window

    def evaluate_telemetry(self):
        base_joint = (self.arm.theta1, self.arm.element_1_model.theta, self.arm.element_1_control.w_target, self.arm.element_1_model.w, self.arm.element_1_control.torque)
        second_joint = (self.arm.theta2, self.arm.element_2_model.theta, self.arm.element_2_control.w_target, self.arm.element_2_model.w, self.arm.element_2_control.torque)
        end_effector_joint = (self.arm.theta3, self.arm.element_3_model.theta, self.arm.element_3_control.w_target, self.arm.element_3_model.w, self.arm.element_3_control.torque)
        self.telemetry.gather(self.t, base_joint, second_joint, end_effector_joint)
        if self.t > self.seconds_after_show_telemetry:
           self.telemetry.show(print_base_joint= self.print_telemetry_base_joint, print_second_joint= self.print_telemetry_second_joint, print_end_eff_joint= self.print_telemetry_end_eff_joint)
           self.show_telemetry = False

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(255,255,255))
        qp.setBrush(QtGui.QColor(255,255,255))
        qp.drawRect(event.rect())   # white bg

        qp.setPen(QtCore.Qt.black)
        self.arm_painter.paint(qp, self.t, print_ray=self.print_end_effector_ray)        
        self.world.paint(qp, print_block_slots= self.print_block_slots, print_scaled_obstacles= self.print_scaled_obstacle)
        if self.print_nf1:
            self.nf1.paint(qp, print_map=self.print_nf1_map, print_obstacle= self.print_nf1_obstacle, print_map_values=self.print_nf1_map_values, print_coord=self.print_nf1_coord, print_path=self.print_nf1_path)

        qp.end()

def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    start_message_server_http(ex)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


