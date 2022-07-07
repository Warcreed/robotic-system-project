from PyQt5 import QtGui, QtCore
from modules.utils.pose import *
import random

class Obstacle:
   
    WIDTH = 0.1
    HEIGHT = 0.1

    def __init__(self, x, y, a):
        self.__pose = Pose()
        self.__pose.set_pose(x,y,a)
        self.__w = Pose.pixel_scale(Obstacle.WIDTH)
        self.__h = Pose.pixel_scale(Obstacle.HEIGHT)
        (x, y) = self.__pose.to_pixel()
        self.__points = QtGui.QPolygon([
            QtCore.QPoint(random.uniform(x, x + self.__w), y),
            QtCore.QPoint(x, random.uniform(y, y + self.__h)),
            QtCore.QPoint(random.uniform(x, x + self.__w), y + self.__h),
            QtCore.QPoint(x + self.__w, random.uniform(y, y + self.__h)),
        ])
        print(x, y)

    def get_pose(self):
        return self.__pose.get_pose()

    def paint(self, qp):
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtGui.QColor(211, 211, 211))

        (x, y) = self.__pose.to_pixel()

        qp.drawPolygon(self.__points)
        
        qp.setPen(QtCore.Qt.black)
        qp.drawLine(x, y, x + self.__w, y)
        qp.drawLine(x, y, x, y + self.__h)
        qp.drawLine(x, y + self.__h, x + self.__w, y + self.__h)
        qp.drawLine(x + self.__w, y + self.__h, x + self.__w, y)