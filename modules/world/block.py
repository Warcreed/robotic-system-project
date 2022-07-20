from PyQt5 import QtGui, QtCore
from modules.utils.pose import *

COLOR_MAP = { 'red' : QtGui.QColor(255,0,0),
              'green' : QtGui.QColor(0,255,0),
              'blue' : QtGui.QColor(0,0,255)
            }

class Block:

    WIDTH = 0.03
    HEIGHT = 0.02
    GAP = 0.01

    def __init__(self, uColor):
        self.__color = uColor
        self.__pose = Pose()
        self.__w = Pose.pixel_scale(Block.WIDTH)
        self.__h = Pose.pixel_scale(Block.HEIGHT)

    def get_pose(self):
        return self.__pose.get_pose()

    def set_pose(self, x, y, a):
        self.__pose.set_pose(x,y,a)

    def get_color(self):
        return self.__color

    def paint(self, qp):
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(COLOR_MAP[self.__color])

        (x, y) = self.__pose.to_pixel()

        t = QtGui.QTransform()
        t.translate(x + self.__w/2, y - self.__h/2)
        t.rotate(-self.__pose.get_a())
        t.translate(-(x + self.__w/2), -(y - self.__h/2))

        qp.setTransform(t)
        qp.drawRect(x, y - self.__h, self.__w, self.__h)


