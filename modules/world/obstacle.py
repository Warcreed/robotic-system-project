from PyQt5 import QtGui, QtCore

POLYGON_TYPE_ARRAY = [
    (   
        QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(38, -35),
            QtCore.QPoint(75, 0),
            QtCore.QPoint(75, 40),
            QtCore.QPoint(50, 40),
            QtCore.QPoint(50, 0),
        ]),
        QtGui.QPolygon([
            QtCore.QPoint(-20, 7),
            QtCore.QPoint(38, -60),
            QtCore.QPoint(115, 0),
            QtCore.QPoint(115, 65),
            QtCore.QPoint(45, 65),
            QtCore.QPoint(45, 5),
        ]),
    ),
    (
        QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(100, 0),
            QtCore.QPoint(0, 100),
        ]),
        QtGui.QPolygon([
            QtCore.QPoint(-10, -10),
            QtCore.QPoint(110, -10),
            QtCore.QPoint(-10, 110),
        ]),
    ),
    (
        QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(0, 100),
            QtCore.QPoint(100, 100),
            QtCore.QPoint(100, 0),
        ]),
        QtGui.QPolygon([
            QtCore.QPoint(-20, -20),
            QtCore.QPoint(-20, 120),
            QtCore.QPoint(120, 120),
            QtCore.QPoint(120, -20),
        ]),
    ),
    (
        QtGui.QPolygon([
            QtCore.QPoint(10, 0),
            QtCore.QPoint(60, 0),
            QtCore.QPoint(70, 48),
            QtCore.QPoint(0, 48),
        ]),
        QtGui.QPolygon([
            QtCore.QPoint(0, -10),
            QtCore.QPoint(110, -10),
            QtCore.QPoint(110, 30),
            QtCore.QPoint(70, 48),
            QtCore.QPoint(70, 70),
            QtCore.QPoint(-15, 70),
        ]),
    ),
    (
        QtGui.QPolygon([
            QtCore.QPoint(0, 0),
            QtCore.QPoint(70, 5),
            QtCore.QPoint(50, 70),
            QtCore.QPoint(3, 50),
        ]),
        QtGui.QPolygon([
            QtCore.QPoint(-10, -10),
            QtCore.QPoint(85, 0),
            QtCore.QPoint(50, 100),
            QtCore.QPoint(-7, 60),
        ]),
    ),
    (
        QtGui.QPolygon([
            QtCore.QPoint(0, 40),
            QtCore.QPoint(40, 5),
            QtCore.QPoint(84, 60),
            QtCore.QPoint(20, 95),
        ]),
        QtGui.QPolygon([
            QtCore.QPoint(-15, 40),
            QtCore.QPoint(40, -10),
            QtCore.QPoint(90, 60),
            QtCore.QPoint(20, 105),
        ]),
    )
]

class Obstacle:

    WIDTH = 0.085
    HEIGHT = 0.085

    def __init__(self, x, y, type):
        self.__polygon = POLYGON_TYPE_ARRAY[type][0]
        self.__scaled_polygon = POLYGON_TYPE_ARRAY[type][1]       
        for point in self.__polygon:
            point.setX(x + point.x())
            point.setY(y + point.y())
        for point in self.__scaled_polygon:
            point.setX(x + point.x())
            point.setY(y + point.y())

    def get_polygon(self):
        return self.__polygon
    
    def get_scaled_polygon(self):
        return self.__polygon
    
    def intersects(self, polygon):
        return self.__polygon.intersects(polygon)

    def intersects_scaled_poly(self, polygon):
        return self.__scaled_polygon.intersects(polygon)

    def paint(self, qp, print_scaled):

        if print_scaled:
            qp.setPen(QtCore.Qt.black)
            qp.setBrush(QtGui.QColor(235, 171, 52))
            qp.drawPolygon(self.__scaled_polygon)

        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtGui.QColor(211, 211, 211))
        qp.drawPolygon(self.__polygon)
