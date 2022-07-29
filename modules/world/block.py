import math
from PyQt5 import QtGui, QtCore
from lib.models.arm_model import GRAVITY
from modules.utils.pose import *

COLOR_MAP = { 'red' : QtGui.QColor(255,0,0),
              'green' : QtGui.QColor(0,255,0),
              'blue' : QtGui.QColor(0,0,255)
            }

class BlockSlot:

    def __init__(self, x, y, a, busy = False):
        self.__pose = Pose(x, y, a)
        self.busy = busy
        self.__w = Pose.pixel_scale(Block.WIDTH)
        self.__h = Pose.pixel_scale(Block.HEIGHT)

    def is_busy(self):
        return self.busy

    def set_as_busy(self):
        self.busy = True

    def set_as_free(self):
        self.busy = False

    def get_slot_pose(self):
        return self.__pose.get_pose()
    
    def paint(self, qp):
       qp.setPen(QtCore.Qt.black)
       qp.setBrush(QtCore.Qt.white)

       (x, y) = self.__pose.to_pixel()

       t = QtGui.QTransform()
       t.translate(x + self.__w/2, y - self.__h/2)
       t.rotate(-self.__pose.get_a())
       t.translate(-(x + self.__w/2), -(y - self.__h/2))

       qp.setTransform(t)
       qp.drawRect(x, y - self.__h, self.__w, self.__h)
       qp.resetTransform()

class Block:

    WIDTH = 0.03
    HEIGHT = 0.02
    GRAVITY = 1.81
    FLOOR_LEVEL = -0.015
    
    def __init__(self, x, y, a, uColor, slot_index):
        self.__slot_index = slot_index
        self.__color = uColor
        self.__pose = Pose(x, y, a)
        self.__a = a
        self.__w = Pose.pixel_scale(Block.WIDTH)
        self.__h = Pose.pixel_scale(Block.HEIGHT)
        self.__is_collected = False
        self.__dropping = False

    def get_slot_index(self):
        return self.__slot_index

    def get_pose(self):
        return self.__pose.get_pose()

    def set_pose(self, x, y, a):
        self.__pose.set_pose(x,y,a)

    def get_color(self):
        return self.__color

    def collect(self):
        self.__is_collected=True
    
    def drop(self):
        self.__is_collected=False
        self.__dropping=True

    def follow_end_effector(self, arm):
        (x,y,a) = arm.get_pose_xy_a().get_pose()
        L = arm.element_3_model.L
        x_1 = (L+L/4) * math.cos(a) + x       # sposta punto di controllo su end effector
        y_1 = (L+L/4) * math.sin(a) + y
        self.__pose.set_pose(x_1, y_1, math.degrees(self.__a))
    
    def _dropping(self, time):
        (x, y, a) = self.__pose.get_pose()
        if y <= Block.FLOOR_LEVEL:
            self.__dropping = False
            return
        s = (-0.5) * Block.GRAVITY * time**2 + y
        self.__pose.set_pose(x, s, a)

    def paint(self, qp, arm, time):
        if self.__is_collected:
            self.follow_end_effector(arm)
        if self.__dropping:
            self._dropping(time)

        qp.setPen(QtCore.Qt.black)
        qp.setBrush(COLOR_MAP[self.__color])

        (x, y) = self.__pose.to_pixel()

        t = QtGui.QTransform()
        t.translate(x + self.__w/2, y - self.__h/2)
        t.rotate(-self.__pose.get_a())
        t.translate(-(x + self.__w/2), -(y - self.__h/2))

        qp.setTransform(t)
        qp.drawRect(x, y - self.__h, self.__w, self.__h)
        qp.resetTransform()


