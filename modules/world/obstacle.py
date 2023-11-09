from PyQt6.QtGui import QPolygon, QColor, QPen
from PyQt6.QtCore import QPoint, Qt

POLYGON_TYPE_ARRAY = [
    (   
        QPolygon([
            QPoint(0, 0),
            QPoint(38, -35),
            QPoint(75, 0),
            QPoint(75, 40),
            QPoint(50, 40),
            QPoint(50, 0),
        ]),
        QPolygon([
            QPoint(-20, 7),
            QPoint(38, -60),
            QPoint(115, 0),
            QPoint(115, 65),
            QPoint(45, 65),
            QPoint(45, 5),
        ]),
    ),
    (
        QPolygon([
            QPoint(0, 0),
            QPoint(100, 0),
            QPoint(0, 100),
        ]),
        QPolygon([
            QPoint(-10, -10),
            QPoint(110, -10),
            QPoint(-10, 110),
        ]),
    ),
    (
        QPolygon([
            QPoint(0, 0),
            QPoint(0, 100),
            QPoint(100, 100),
            QPoint(100, 0),
        ]),
        QPolygon([
            QPoint(-20, -20),
            QPoint(-20, 120),
            QPoint(120, 120),
            QPoint(120, -20),
        ]),
    ),
    (
        QPolygon([
            QPoint(10, 0),
            QPoint(60, 0),
            QPoint(70, 48),
            QPoint(0, 48),
        ]),
        QPolygon([
            QPoint(0, -10),
            QPoint(110, -10),
            QPoint(110, 30),
            QPoint(70, 48),
            QPoint(70, 70),
            QPoint(-15, 70),
        ]),
    ),
    (
        QPolygon([
            QPoint(0, 0),
            QPoint(70, 5),
            QPoint(50, 70),
            QPoint(3, 50),
        ]),
        QPolygon([
            QPoint(-10, -10),
            QPoint(85, 0),
            QPoint(50, 100),
            QPoint(-7, 60),
        ]),
    ),
    (
        QPolygon([
            QPoint(0, 40),
            QPoint(40, 5),
            QPoint(84, 60),
            QPoint(20, 95),
        ]),
        QPolygon([
            QPoint(-15, 40),
            QPoint(40, -10),
            QPoint(90, 60),
            QPoint(20, 105),
        ]),
    )
]

class Obstacle:

    WIDTH = 0.085
    HEIGHT = 0.085

    def __init__(self, x, y, type):
        self.__polygon = POLYGON_TYPE_ARRAY[type][0].translated(x, y)
        self.__scaled_polygon = POLYGON_TYPE_ARRAY[type][1].translated(x, y)

    def get_polygon(self):
        return self.__polygon
    
    def get_scaled_polygon(self):
        return self.__scaled_polygon
    
    def intersects(self, polygon):
        return self.__polygon.intersects(polygon)

    def intersects_scaled_poly(self, polygon):
        return self.__scaled_polygon.intersects(polygon)

    def paint(self, qp, print_scaled):

        if print_scaled:
            qp.setPen(QPen(Qt.GlobalColor.black))
            qp.setBrush(QColor(235, 171, 52))
            qp.drawPolygon(self.__scaled_polygon)

        qp.setPen(QPen(Qt.GlobalColor.black))
        qp.setBrush(QColor(211, 211, 211))
        qp.drawPolygon(self.__polygon)