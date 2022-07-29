import math
from PyQt5 import QtGui, QtCore
from modules.utils.pose import Pose

from modules.world.world import World

class NF1:
    def __init__(self, resolution):    
        self.resolution = resolution 
        self.nf1_path_active = False 
        self.current_cell = None
        self._world_matrix = []
        self.x_shift = 0.1215
        self.y_shift = 0.032
        #0.018  0.022
        self.x_gap = World.WIDTH / resolution
        self.y_gap = World.HEIGHT / resolution

        y_temp = World.HEIGHT - ((World.HEIGHT / resolution) / 2)
        for i in range(resolution):
            temp_row = []
            x_temp = ((World.WIDTH / resolution) / 2)
            for j in range(resolution):
                temp_row.append(NF1Cell(x= x_temp, y= y_temp))
                x_temp += self.x_gap
            self._world_matrix.append(temp_row)            
            y_temp -= self.y_gap
        
    def set_is_obstacle_for_world_matrix(self, obstacles):
        half_x_gap = self.x_gap / 2
        half_y_gap = self.y_gap / 2
        for els in self._world_matrix:
            for el in els:
                for obst in obstacles:
                    if obst.intersects(
                        QtGui.QPolygon(QtCore.QRect(
                                QtCore.QPoint(Pose.pixel_scale(el.x - half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y - half_y_gap + self.y_shift)),
                                QtCore.QPoint(Pose.pixel_scale(el.x + half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y + half_y_gap + self.y_shift)),
                            ))):
                        el.set_is_obstacle(True)
    
    def set_bowl_as_obstacle_for_world_matrix(self, bowl):
        half_x_gap = self.x_gap / 2
        half_y_gap = self.y_gap / 2
        for i in range(int(len(self._world_matrix)/2), len(self._world_matrix)):
            for j in range(len(self._world_matrix[0])):
                el = self._world_matrix[i][j]
                if bowl.intersects(
                    QtGui.QPolygon(QtCore.QRect(
                                QtCore.QPoint(Pose.pixel_scale(el.x - half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y - half_y_gap + self.y_shift)),
                                QtCore.QPoint(Pose.pixel_scale(el.x + half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y + half_y_gap + self.y_shift)),
                            ))):
                    el.set_is_obstacle(True)
    
    def __reset_matrix(self):
        for els in self._world_matrix:
            for el in els:
                el.set_value(math.inf)

    def run_nf1_for_taget_xy(self, x_taget, y_taget):
        # reset valori mappa
        self.__reset_matrix()
        self.nf1_path_active = True 
        # determinare cella target
        (i, j) = self.__get_cell_index_by_xy(x_taget, y_taget)
        # ricorsione celle vicine incrementando valore a partire dal target (valore 0)
        self.__nf1_adjacent_cells_value_spreading(i, j)

    def get_next_cell(self, x, y):
        # prendere cella posizione attuale braccio
        (i, j) = self.__get_cell_index_by_xy(x, y)
        # prendere la cella successiva
        min = math.inf
        i_target = None
        j_target = None
        for k in range(i-1, i+2):
            for p in range (j-1, j+2):
                if k >= 0 and k < self.resolution and p >= 0 and p < self.resolution:                    
                    if self._world_matrix[k][p].get_value() < min:
                        min = self._world_matrix[k][p].get_value()
                        i_target = k
                        j_target = p
        self.current_cell = self._world_matrix[i_target][j_target]
        return self.current_cell


    def __get_cell_index_by_xy(self, x, y):
        half_x_gap = self.x_gap / 2
        half_y_gap = self.y_gap / 2
        (pos_x, pos_y) = Pose.xy_to_pixel(x, y)
        for i in range(len(self._world_matrix)):
            for j in range(len(self._world_matrix)):
                el = self._world_matrix[i][j]
                polygon = QtGui.QPolygon(QtCore.QRect(
                                QtCore.QPoint(Pose.pixel_scale(el.x - half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y - half_y_gap + self.y_shift)),
                                QtCore.QPoint(Pose.pixel_scale(el.x + half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y + half_y_gap + self.y_shift)),
                            ))
                if polygon.intersects(QtGui.QPolygon([QtCore.QPoint(pos_x, pos_y)])):
                     return (i, j)
        return (None, None)
       

    # calcolo con distanza euclidea
    # def __get_cell_index_by_xy(self, x, y):
    #     min = math.inf
    #     i_index = None
    #     j_index = None
    #     target = (x, y)
    #     for i in range(len(self._world_matrix)):
    #         for j in range(len(self._world_matrix)):
    #             cell_point = (self._world_matrix[i][j].x + self.x_shift, self._world_matrix[i][j].y + self.y_shift)
    #             distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(target, cell_point)])) # distanza euclidea
    #             if distance < min:
    #                 min = distance
    #                 i_index = i
    #                 j_index = j                
    #     return (i_index, j_index)

    # ricorsiva
    def __nf1_adjacent_cells_value_spreading(self, i, j, value= 0):
        if (i < 0 or i >= self.resolution) or (j < 0 or j >= self.resolution):
            return
       
        self._world_matrix[i][j].set_value(value)
        for k in range(i-1, i+2):
            for p in range (j-1, j+2):
                if (not(k==i and p==j)) and (k >= 0 and k < self.resolution) and (p >= 0 and p < self.resolution) and (self._world_matrix[k][p].get_value() > value + 1) and not self._world_matrix[k][p].is_obstacle() :                    
                    self.__nf1_adjacent_cells_value_spreading(k, p, value + 1)

    def check_target_got(self):
        if self.current_cell is not None:
            if self.current_cell.get_value() == 0:
                self.nf1_path_active = False
                return True
        return False
    
    def paint(self, qp):
        qp.setPen(QtCore.Qt.blue)

        for i in range(len(self._world_matrix[0])):   # last row and last col is not printed    
            qp.drawLine(
                int(Pose.pixel_scale((self._world_matrix[i][0].x - self.x_gap / 2) + self.x_shift)), 
                int(Pose.pixel_scale((self._world_matrix[i][0].y - self.y_gap / 2) + self.y_shift)),
                int(Pose.pixel_scale((self._world_matrix[i][-1].x - self.x_gap / 2) + self.x_shift)), 
                int(Pose.pixel_scale((self._world_matrix[i][-1].y - self.y_gap / 2)+ self.y_shift))),     
            qp.drawLine(
                int(Pose.pixel_scale((self._world_matrix[0][i].x - self.x_gap / 2) + self.x_shift)), 
                int(Pose.pixel_scale((self._world_matrix[0][i].y - self.y_gap / 2) + self.y_shift)),
                int(Pose.pixel_scale((self._world_matrix[-1][i].x - self.x_gap / 2) + self.x_shift)), 
                int(Pose.pixel_scale((self._world_matrix[-1][i].y - self.y_gap / 2) + self.y_shift))),
            qp.drawText(
                Pose.pixel_scale(self._world_matrix[i][0].x - self.x_gap  + self.x_shift ), 
                Pose.pixel_scale(World.HEIGHT - self._world_matrix[i][0].y - self.y_gap  + self.y_shift ), 
                str(i - 1))
            qp.drawText(
                Pose.pixel_scale(self._world_matrix[0][i].x - self.x_gap + self.x_shift ), 
                Pose.pixel_scale(World.HEIGHT - self._world_matrix[0][i].y - self.y_gap + self.y_shift ), 
                str(i - 1))        
        
        # print obstacle
        # qp.setFont(QtGui.QFont("times",10)); 
        # for els in self._world_matrix:
        #     for el in els:
        #         qp.drawText(Pose.pixel_scale(el.x + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y + self.y_shift), str(el.is_obstacle()))

        # print map values
        for els in self._world_matrix:
            for el in els:
                qp.drawText(
                    Pose.pixel_scale(el.x + self.x_shift), 
                    Pose.pixel_scale(World.HEIGHT - el.y + self.y_shift), str(el.get_value()))
        
        # for els in self._world_matrix:
        #     for el in els:
        #         qp.drawText(
        #             Pose.pixel_scale(el.x + self.x_shift), 
        #             Pose.pixel_scale(World.HEIGHT - el.y + self.y_shift), str(round(el.x, 3)) + "/" + str(round(el.y, 3)))

        # qp.setPen(QtCore.Qt.blue)
        # qp.setBrush(QtCore.Qt.red)
        # for els in self._world_matrix:
        #     for el in els:
        #         qp.drawRect(
        #             Pose.pixel_scale(el.x + self.x_shift), 
        #             Pose.pixel_scale(World.HEIGHT - el.y + self.y_shift), 
        #             Pose.pixel_scale(0.006),
        #             Pose.pixel_scale(0.006)
        #             )

class NF1Cell:
    def __init__(self, x, y, value= math.inf, is_obstacle=False):
        self.x = x
        self.y = y
        self._value = value
        self._is_obstacle = is_obstacle

    def set_is_obstacle(self, value):
        self._is_obstacle = value

    def is_obstacle(self):
        return self._is_obstacle
    
    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value