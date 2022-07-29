from PyQt5 import QtGui, QtCore
# from modules.utils.pose import *

POLYGON_TYPE_ARRAY = [
    QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(38, -35),
            QtCore.QPoint(75, 0),
        ]),
    QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(100, 0),
            QtCore.QPoint(0, 100),
        ]),
    QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(0, 100),
            QtCore.QPoint(100, 100),
            QtCore.QPoint(100, 0),
        ]),
    QtGui.QPolygon([
            QtCore.QPoint(10, 0),
            QtCore.QPoint(60, 0),
            QtCore.QPoint(70, 48),
            QtCore.QPoint(0, 48),
        ]),
    QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(70, 5),
            QtCore.QPoint(50, 70),
            QtCore.QPoint(3, 50),
        ]),
    QtGui.QPolygon([
            QtCore.QPoint(0, 40),
            QtCore.QPoint(40, 5),
            QtCore.QPoint(85, 60),
            QtCore.QPoint(20, 90),
        ]),
]

class Obstacle:

    WIDTH = 0.085
    HEIGHT = 0.085

    def __init__(self, x, y, type):
        self.__polygon = POLYGON_TYPE_ARRAY[type]
        for point in self.__polygon:
            point.setX(x + point.x())
            point.setY(y + point.y())

    def get_polygon(self):
        return self.__polygon
    
    def intersects(self, polygon):
        return self.__polygon.intersects(polygon)

    def paint(self, qp):
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtGui.QColor(211, 211, 211))
        qp.drawPolygon(self.__polygon)
