from PyQt5 import QtGui, QtCore
from modules.utils.pose import Pose

from modules.world.world import World

class NF1:
    def __init__(self, resolution):
        self._world_matrix = []
        self.x_gap = World.WIDTH / resolution
        self.y_gap = World.HEIGHT / resolution

        y_temp = ((World.HEIGHT / resolution) / 2) + 0.05
        for i in range(resolution):
            temp_row = []
            x_temp = ((World.WIDTH / resolution) / 2) + 0.05
            for j in range(resolution):
                temp_row.append(NF1Cell(x= x_temp, y= y_temp, is_obstacle=False))
                x_temp += self.x_gap
            self._world_matrix.append(temp_row)            
            y_temp += self.y_gap

    def set_is_obstacle_for_world_matrix(self, obstacles):
        half_x_gap = self.x_gap / 2
        half_y_gap = self.y_gap / 2
        for els in self._world_matrix:
            for el in els:
                for obst in obstacles:
                    el.set_is_obstacle(obst.get_polygon().intersects(
                        QtGui.QPolygon(
                            QtCore.QRect(
                                QtCore.QPoint(el.x - half_x_gap, el.y - half_y_gap),
                                QtCore.QPoint(el.x + half_x_gap, el.y + half_y_gap),
                            ))))
                print(el.x, el.y)
                print(el.is_obstacle)
                print()
                    
               
        
    def paint(self, qp):
        qp.setPen(QtCore.Qt.blue)
        for i in range(len(self._world_matrix[0])):   # last row and last col is not printed    
            qp.drawLine(
                int(Pose.pixel_scale(self._world_matrix[i][0].x - self.x_gap / 2)), 
                int(Pose.pixel_scale(self._world_matrix[i][0].y - self.y_gap / 2)), 
                int(Pose.pixel_scale(self._world_matrix[i][-1].x - self.x_gap / 2)), 
                int(Pose.pixel_scale(self._world_matrix[i][-1].y - self.y_gap / 2)))         
            qp.drawLine(
                int(Pose.pixel_scale(self._world_matrix[0][i].x - self.x_gap / 2)), 
                int(Pose.pixel_scale(self._world_matrix[0][i].y - self.y_gap / 2)), 
                int(Pose.pixel_scale(self._world_matrix[-1][i].x - self.x_gap / 2)), 
                int(Pose.pixel_scale(self._world_matrix[-1][i].y - self.y_gap / 2)))
            qp.drawText(
                Pose.pixel_scale(self._world_matrix[i][0].x - self.x_gap), 
                Pose.pixel_scale(self._world_matrix[i][0].y - self.y_gap), 
                str(i - 1))
            qp.drawText(
                Pose.pixel_scale(self._world_matrix[0][i].x - self.x_gap), 
                Pose.pixel_scale(self._world_matrix[0][i].y - self.y_gap), 
                str(i - 1))        
                
        for els in self._world_matrix:
            for el in els:
                qp.drawText(Pose.pixel_scale(el.x), Pose.pixel_scale(el.y), str(1 if el.is_obstacle else 0))

class NF1Cell:
    def __init__(self, x, y, is_obstacle):
        self.x = x
        self.y = y
        self.is_obstacle = is_obstacle

    def set_is_obstacle(self, value):
        self.is_obstacle = value