import sys

from modules.utils.config import Config

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

COLOR_NAMES = [ 'red', 'green', 'blue' ]

# TODO: controllare alcuni spike di potenza, tuning costanti
# TODO: controllare taratura

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Robotic Manipulator Project - Danilo Santitto')
        self.show()

        self.delta_t = 1e-3 # 10ms of time-tick
        self.t = 0

        self.trajectory = Path2DManipulator(_vmax = 0.1, _acc = 0.1, _dec = 0.1, _distance_threshold=0.005, _alpha_deg_threshold=1.5)

        self.arm = ThreeJointsArm(self.trajectory)
        self.arm_painter = ThreeJointsArmPainter(self.arm)

        self.world = World(self)
        self.px_world_height = Pose.pixel_scale(World.HEIGHT)
        self.px_world_width = Pose.pixel_scale(World.WIDTH)
        self.px_world_floor_level = Pose.pixel_scale(Config.FLOOR_LEVEL)

        self.telemetry = Telemetry()

        self._timer_painter = QtCore.QTimer(self)
        self._timer_painter.timeout.connect(self.go)
        self._timer_painter.start(int(self.delta_t * 1000))
        self.notification = False

        self._phidias_agent = None

        self.nf1 = NF1(Config.nf1_map_resolution)
        self.nf1.set_is_obstacle_for_world_matrix(self.world.get_obstacles())
        self.nf1.set_bowl_as_obstacle_for_world_matrix(self.world.get_bowl())
        self.target_alpha_deg = 0

        # set initial position
        target_x = 0.1
        target_y = 0.15
        target_alpha = -90
        self.arm.set_path([ (target_x, target_y, target_alpha) ])
        self.arm.start()

        ## telemetry
        self.show_telemetry = Config.show_telemetry

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
        (target_x, target_y, self.target_alpha_deg) = Config.end_eff_block_poses[block_index].get_pose()
        self.nf1.run_nf1_for_taget_xy(target_x, target_y)
        self._build_path(self.target_alpha_deg)
        self.arm.start()

    def _build_path(self, target_alpha_deg):
        (x, y, a) = self.arm.get_pose_xy_a()
        path = self.nf1.build_path(x, y, math.degrees(a), target_alpha_deg)
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
            self.evaluate_trajectory()

        self.t += self.delta_t
        self.update() # repaint window
    
    def evaluate_trajectory(self):
        if self.trajectory.target_got:
            if not(self.notification):
                self.notify_target_got()
            self.trajectory.target_got = False
            self.trajectory.path_active = False
        else:
            self.arm.evaluate_trajectory(self.delta_t)

    def evaluate_telemetry(self):
        base_joint = (self.arm.theta1, self.arm.element_1_model.theta, self.arm.element_1_control.w_target, self.arm.element_1_model.w, self.arm.element_1_control.torque)
        second_joint = (self.arm.theta2, self.arm.element_2_model.theta, self.arm.element_2_control.w_target, self.arm.element_2_model.w, self.arm.element_2_control.torque)
        end_effector_joint = (self.arm.theta3, self.arm.element_3_model.theta, self.arm.element_3_control.w_target, self.arm.element_3_model.w, self.arm.element_3_control.torque)
        self.telemetry.gather(self.t, base_joint, second_joint, end_effector_joint)
        if self.t > Config.seconds_after_show_telemetry:
           self.telemetry.show(print_base_joint= Config.print_telemetry_base_joint, print_second_joint= Config.print_telemetry_second_joint, print_end_eff_joint= Config.print_telemetry_end_eff_joint)
           self.show_telemetry = False

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(255,255,255))
        qp.setBrush(QtGui.QColor(255,255,255))
        qp.drawRect(event.rect())   # white bg

        qp.setPen(QtCore.Qt.black)
        self.arm_painter.paint(qp, self.t, print_ray=Config.print_end_effector_ray)        
        self.world.paint(qp, print_block_slots= Config.print_block_slots, print_scaled_obstacles= Config.print_scaled_obstacle)
        self.nf1.paint(qp, print_map=Config.print_nf1_map, print_obstacle= Config.print_nf1_obstacle, print_map_values=Config.print_nf1_map_values, print_coord=Config.print_nf1_coord, print_path=Config.print_nf1_path)

        qp.end()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    start_message_server_http(ex)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


