import sys
import math

from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt, QPoint
from modules.utils.pose import *

class ArmPainter:

    def __init__(self, arm):
        self.arm = arm

    def draw_arm_element(self, qp, x1, y1, x2, y2, ellipse=True):
        qp.setPen(QPen(Qt.black, 8))
        qp.drawLine(x1, y1, x2, y2)

        if ellipse:
            qp.setPen(QPen(Qt.black, 3))

            qp.drawEllipse(QPoint(x1, y1), 10, 10)
            qp.drawEllipse(QPoint(x1, y1), 4, 4)

            qp.drawEllipse(QPoint(x2, y2), 10, 10)
            qp.drawEllipse(QPoint(x2, y2), 4, 4)


class ThreeJointsArmPainter(ArmPainter):

    def __init__(self, arm):
        super(ThreeJointsArmPainter, self).__init__(arm)

    def print_ray(self, qp):
        (x,y,a) = self.arm.get_pose_xy_a()
        L = self.arm.element_3_model.L
        x_1 = (2.2*L) * math.cos(a) + x       
        y_1 = (2.2*L) * math.sin(a) + y  
        (x_1, y_1) = Pose.xy_to_pixel(x_1, y_1)
        (x, y) = Pose.xy_to_pixel(x, y)
        qp.setPen(QPen(Qt.blue, 3))
        qp.drawLine(x, y, x_1, y_1)

    def paint(self, qp, t, print_ray=False):
        th = self.arm.get_pose_degrees()
        p = self.arm.get_pose()
        (x1, y1) = p[0]
        (x2, y2) = p[1]
        (x3, y3) = p[2]
        x_draw_point = 650
        qp.drawText(x_draw_point,  20, "X  = %6.3f m"   % (x2))
        qp.drawText(x_draw_point,  40, "Y  = %6.3f m"   % (y2))
        qp.drawText(x_draw_point,  60, "Th1= %6.3f deg" % (th[0]))
        qp.drawText(x_draw_point,  80, "Th2= %6.3f deg" % (th[1]))
        qp.drawText(x_draw_point, 100, "Th3= %6.3f deg" % (th[2]))
        qp.drawText(x_draw_point, 120, "T  = %6.3f s"   % (t))

        (x1_pos, y1_pos) = Pose.xy_to_pixel(x1, y1)
        (x2_pos, y2_pos) = Pose.xy_to_pixel(x2, y2)
        (x3_pos, y3_pos) = Pose.xy_to_pixel(x3, y3)

        if print_ray:
            self.print_ray(qp)

        self.draw_arm_element(qp, Pose.x_center, Pose.y_center, x1_pos, y1_pos)

        self.draw_arm_element(qp, x1_pos, y1_pos, x2_pos, y2_pos)

        self.draw_arm_element(qp, x2_pos, y2_pos, x3_pos, y3_pos, False)

