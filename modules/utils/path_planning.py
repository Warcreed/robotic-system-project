from PyQt5 import QtGui, QtCore
from modules.utils.pose import Pose

from modules.world.world import World

class NF1:
    def __init__(self, resolution):
        self._world_matrix = []
        x_temp = (World.WIDTH / resolution) / 2
        y_temp = (World.HEIGHT / resolution) / 2
        x_gap = World.WIDTH / resolution
        y_gap = World.HEIGHT / resolution

        for i in range(resolution):
            temp_row = []
            x_temp = (World.WIDTH / resolution) / 2
            for j in range(resolution):
                temp_row.append(NF1Cell(x= x_temp, y= y_temp, is_obstacle=False))
                x_temp += x_gap
            self._world_matrix.append(temp_row)            
            y_temp += y_gap

        for elements in self._world_matrix:
            for el in elements:
                print(el.x, el.y)
        print()
        print(int(Pose.pixel_scale(self._world_matrix[0][0].x)))
        print(int(Pose.pixel_scale(self._world_matrix[0][0].y))) 
        print(int(Pose.pixel_scale(self._world_matrix[0][-1].x))) 
        print(int(Pose.pixel_scale(self._world_matrix[0][-1].y))) 
        
    def paint(self, qp):
        qp.setPen(QtCore.Qt.blue)
        for i in range(len(self._world_matrix[0])):          
            qp.drawLine(
                int(Pose.pixel_scale(self._world_matrix[i][0].x)), 
                int(Pose.pixel_scale(self._world_matrix[i][0].y)), 
                int(Pose.pixel_scale(self._world_matrix[i][-1].x)), 
                int(Pose.pixel_scale(self._world_matrix[i][-1].y)))         
            qp.drawLine(
                int(Pose.pixel_scale(self._world_matrix[0][i].x)), 
                int(Pose.pixel_scale(self._world_matrix[0][i].y)), 
                int(Pose.pixel_scale(self._world_matrix[-1][i].x)), 
                int(Pose.pixel_scale(self._world_matrix[-1][i].y)))

class NF1Cell:
    def __init__(self, x, y, is_obstacle):
        self.x = x
        self.y = y
        self.is_obstacle = is_obstacle