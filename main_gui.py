#
#
#

import sys

sys.path.insert(0, './lib')
sys.path.insert(0, './modules')

import math
import random

#
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^ use these for Qt5
#
#

#from PyQt4 import QtGui, QtCore

from modules.arm.arm import *
from modules.arm.arm_painters import *
from modules.utils.telemetry import *
from modules.world.world import *
from modules.phidias.phidias_interface import *

COLOR_NAMES = [ 'red',
                'green',
                'blue',
                ]

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1500, 800)
        self.setWindowTitle('Robotic Arm Project - Danilo Santitto')
        self.show()

        self.delta_t = 1e-3 # 10ms of time-tick
        self.t = 0

        self.trajectory_data = [ ]
        self.target_trajectory_data = [ ]

        self.use_profile = False
        self.use_trajectory = True
        self.use_angle_interpolation = False

        self.trajectory = Trajectory3(1.0, 1.5, 1.5)

        self.arm = ThreeJointsArm(self.trajectory, self.use_profile)
        self.painter = ThreeJointsArmPainter(self.arm)

        target_x = 0.1
        target_y = 0.05
        target_alpha = -90

        self.arm.set_target_xy_a(target_x, target_y, target_alpha)

        self.world = World(self)

        self.telemetry = Telemetry()

        self._timer_painter = QtCore.QTimer(self)
        self._timer_painter.timeout.connect(self.go)
        self._timer_painter.start(int(self.delta_t * 1000))
        self.notification = False

        self._phidias_agent = None

    def set_phidias_agent(self, _phidias_agent):
        self._phidias_agent = _phidias_agent

    def go_to(self,target_x, target_y, target_alpha):
        self.notification = False
        self.arm.set_target_xy_a(target_x, target_y, target_alpha)
    
    def go_to_block_slot(self, block_index):
        # add moving to target
        # block = self.world.get_block_slot_at(block_index)
        self.notification = False
        (target_x, target_y, target_alpha) = self.block_poses[block_index].get_pose()
        self.arm.set_target_xy_a(target_x, target_y, target_alpha)

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

    def go(self):
        #self.telemetry.gather(self.delta_t, self.arm.element_3_model.w, self.arm.element_3_control.w_target)
        #if self.t > 8:
        #    self.telemetry.show()
        #    sys.exit(0)

        if self.trajectory.target_got:
            if not(self.notification):
                self.notify_target_got()

        self.arm.evaluate_trajectory(self.delta_t)

        #p = self.arm.get_pose()
        #self.trajectory_data.append(p[-1])
        #if self.use_trajectory:
        #    self.target_trajectory_data.append( (self.arm.trajectory_x, self.arm.trajectory_y) )
        self.t += self.delta_t
        self.update() # repaint window


    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtGui.QColor(255,255,255))
        qp.setBrush(QtGui.QColor(255,255,255))
        qp.drawRect(event.rect())

        # qp.setPen(QtCore.Qt.black)
        # qp.drawLine(50, 500, 900, 500)
        # qp.drawLine(50, 500, 50, 50)
        # qp.drawLine(50, 50, 900, 50)
        # qp.drawLine(900, 50, 900, 500)

        qp.setPen(QtCore.Qt.black)
        self.painter.paint(qp, self.t)
        self.world.paint(qp)

        qp.end()



def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    start_message_server_http(ex)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

