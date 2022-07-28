from PyQt5 import QtGui, QtCore
from modules.utils.pose import *
import random

POLYGON_TYPE_ARRAY = [
    { "top" : 40, "left": 40, "right": 30, "bottom": 30},
    { "top" : 0, "left": 85, "right": 0, "bottom": 85},
    { "top" : 0, "left": 0, "right": 0, "bottom": 0},
    { "top" : 20, "left": 5, "right": 20, "bottom": 5},
    { "top" : 40, "left": 35, "right": 55, "bottom": 20},
]

class Obstacle:

    WIDTH = 0.085
    HEIGHT = 0.085

    def __init__(self, x, y, a, type, w = WIDTH, h = HEIGHT):
        self.__pose = Pose()
        self.__pose.set_pose(x,y,a)
        self.__w = Pose.pixel_scale(w)
        self.__h = Pose.pixel_scale(h)
        (x, y) = self.__pose.to_pixel()
        self.__polygon = QtGui.QPolygon([
            # QtCore.QPoint(random.uniform(x, x + self.__w), y),
            # QtCore.QPoint(x, random.uniform(y, y + self.__h)),
            # QtCore.QPoint(random.uniform(x, x + self.__w), y + self.__h),
            # QtCore.QPoint(x + self.__w, random.uniform(y, y + self.__h)),
            QtCore.QPoint(x + POLYGON_TYPE_ARRAY[type]["top"], y),
            QtCore.QPoint(x, y + POLYGON_TYPE_ARRAY[type]["left"]),
            QtCore.QPoint(x + POLYGON_TYPE_ARRAY[type]["bottom"], y + self.__h),
            QtCore.QPoint(x + self.__w, y + POLYGON_TYPE_ARRAY[type]["right"]),
        ])

    def get_polygon(self):
        return self.__polygon

    def get_pose(self):
        return self.__pose.get_pose()

    def paint(self, qp):
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtGui.QColor(211, 211, 211))

        (x, y) = self.__pose.to_pixel()

        t = QtGui.QTransform()
        t.translate(x + self.__w/2, y - self.__h/2)
        t.rotate(-self.__pose.get_a())
        t.translate(-(x + self.__w/2), -(y - self.__h/2))

        qp.setTransform(t)

        qp.drawPolygon(self.__polygon)

        # qp.drawLine(x, y, x + self.__w, y)
        # qp.drawLine(x, y, x, y + self.__h)
        # qp.drawLine(x, y + self.__h, x + self.__w, y + self.__h)
        # qp.drawLine(x + self.__w, y + self.__h, x + self.__w, y)