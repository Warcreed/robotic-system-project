from PyQt6.QtGui import QPolygon, QColor, QPen, QBrush
from PyQt6.QtCore import QPoint
from modules.utils.pose import *

class Bowl:

    WIDTH = 0.1
    HEIGHT = 0.05

    def __init__(self, x, y, a):
        self.__pose = Pose()
        self.__pose.set_pose(x, y, a)
        self.__w = Pose.pixel_scale(Bowl.WIDTH)
        self.__h = Pose.pixel_scale(Bowl.HEIGHT)
        (x, y) = self.__pose.to_pixel()
        self.__polygon = QPolygon([
            QPoint(x, y),
            QPoint(x + 15, y + self.__h),
            QPoint(x + self.__w - 15, y + self.__h),
            QPoint(x + self.__w, y),
        ])

    def get_pose(self):
        return self.__pose.get_pose()

    def intersects(self, polygon):
        return self.__polygon.intersects(polygon)

    def paint(self, qp):
        qp.setPen(QPen(QColor(179, 163, 126)))
        qp.setBrush(QBrush(QColor(228, 208, 163)))
        qp.drawPolygon(self.__polygon)
