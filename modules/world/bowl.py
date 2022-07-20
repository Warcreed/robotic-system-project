from PyQt5 import QtGui, QtCore
from modules.utils.pose import *

class Bowl:

    WIDTH = 0.1
    HEIGHT = 0.07

    def __init__(self, x, y, a):
        self.__pose = Pose()
        self.__pose.set_pose(x,y,a)
        self.__w = Pose.pixel_scale(Bowl.WIDTH)
        self.__h = Pose.pixel_scale(Bowl.HEIGHT)
        (x, y) = self.__pose.to_pixel()
        self.__points = QtGui.QPolygon([        
            QtCore.QPoint(x, y),
            QtCore.QPoint(x + 15, y + self.__h),
            QtCore.QPoint(x + self.__w - 15, y + self.__h),
            QtCore.QPoint(x + self.__w, y),
        ])

    def get_pose(self):
        return self.__pose.get_pose()

    def paint(self, qp):
        qp.setPen(QtGui.QColor(179, 163, 126))
        qp.setBrush(QtGui.QColor(228, 208, 163))
        qp.drawPolygon(self.__points)