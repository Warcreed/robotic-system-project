import math
from PyQt5 import QtGui, QtCore
from modules.utils.pose import Pose

from modules.world.world import World

class NF1:
    def __init__(self, resolution):    
        self.resolution = resolution 
        self.current_cell = None
        self._world_matrix = []
        self.x_shift = 0.1215
        self.y_shift = 0.032
        self.x_gap = World.WIDTH / resolution
        self.y_gap = World.HEIGHT / resolution
        self.path = [] 
        self._build_matrix(resolution)

    # build matrix based on resolution value (resolution x resolution), every cell is a NF1Cell
    def _build_matrix(self, resolution):
        y_temp = World.HEIGHT - ((World.HEIGHT / resolution) / 2)
        for i in range(resolution):
            temp_row = []
            x_temp = ((World.WIDTH / resolution) / 2)
            for j in range(resolution):
                temp_row.append(NF1Cell(x= x_temp, y= y_temp))
                x_temp += self.x_gap
            self._world_matrix.append(temp_row)            
            y_temp -= self.y_gap
        
    # set NF1Cell unable to be picked due to obstacle
    def set_is_obstacle_for_world_matrix(self, obstacles):
        half_x_gap = self.x_gap / 2
        half_y_gap = self.y_gap / 2
        for els in self._world_matrix:
            for el in els:
                for obst in obstacles:
                    if obst.intersects_scaled_poly(
                        QtGui.QPolygon(QtCore.QRect(
                                QtCore.QPoint(Pose.pixel_scale(el.x - half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y - half_y_gap + self.y_shift)),
                                QtCore.QPoint(Pose.pixel_scale(el.x + half_x_gap + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y + half_y_gap + self.y_shift)),
                            ))):
                        el.set_is_obstacle(True)
    
    # set NF1Cell unable to be picked due to bowl
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
        self.path.clear()
        for els in self._world_matrix:
            for el in els:
                el.set_value(math.inf)

    def run_nf1_for_taget_xy(self, x_taget, y_taget):
        self.__reset_matrix()
        # get target cell
        (i, j) = self.__get_cell_index_by_xy(x_taget, y_taget)
        # recursion to neighboring cells by increasing value starting from the target (value 0)
        self.__nf1_adjacent_cells_value_spreading(i, j)

    # recursive spreading based on NF1
    def __nf1_adjacent_cells_value_spreading(self, i, j, value= 0):
        self._world_matrix[i][j].set_value(value)
        for k in range(i-1, i+2):
            for p in range (j-1, j+2):
                if (not(k==i and p==j)) and (k >= 0 and k < self.resolution) and (p >= 0 and p < self.resolution) and (self._world_matrix[k][p].get_value() > value + 1) and not self._world_matrix[k][p].is_obstacle() :                    
                    self.__nf1_adjacent_cells_value_spreading(k, p, value + 1)

    # build path from current end eff position to target
    def build_path(self, x_start, y_start, current_alpha_deg, target_alpha_deg):
        next_cell = NF1Cell(x= x_start, y= y_start)
        while next_cell.get_value() > 0:
            next_cell = self.get_next_cell(next_cell.x, next_cell.y) # get next NF1Cell
            self.path.append( [next_cell.x, next_cell.y, target_alpha_deg] )
        self._split_deg_based_on_path_length(current_alpha_deg, target_alpha_deg)
        return self.path

    # cell is scanned in order from top left to bottom right
    # cell picking could be improved keeping tracking of last cell
    def get_next_cell(self, x, y):
        (i, j) = self.__get_cell_index_by_xy(x, y)
        min = math.inf
        i_target = i
        j_target = j
        self.current_cell = self._world_matrix[i_target][j_target]
        for k in range(i-1, i+2):
            for p in range (j-1, j+2):
                if k >= 0 and k < self.resolution and p >= 0 and p < self.resolution:                    
                    if self._world_matrix[k][p].get_value() < min:
                        min = self._world_matrix[k][p].get_value()
                        i_target = k
                        j_target = p
        return self._world_matrix[i_target][j_target]

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

    def _split_deg_based_on_path_length(self, current_alpha_deg, target_alpha_deg):
        increment = (target_alpha_deg - current_alpha_deg) / len(self.path)
        incr = increment
        for el in self.path:
            el[2] = current_alpha_deg + incr
            incr += increment
    
    def paint(self, qp, print_map=False, print_obstacle=False, print_map_values=False, print_coord=False, print_path=False):
        qp.setPen(QtCore.Qt.blue)
        if print_map:
            self.print_map(qp)
        if print_obstacle:
            self.print_obstacles(qp)
        if print_map_values:
            self.print_map_values(qp)
        if print_coord:
            self.print_coord(qp)
        if print_path:
            self.print_path(qp)

    def print_map(self, qp):
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
    
    def print_obstacles(self, qp):
        qp.setFont(QtGui.QFont("times",10)); 
        for els in self._world_matrix:
            for el in els:
                qp.drawText(Pose.pixel_scale(el.x + self.x_shift), Pose.pixel_scale(World.HEIGHT - el.y + self.y_shift), str(el.is_obstacle()))

    def print_map_values(self, qp):
        for els in self._world_matrix:
            for el in els:
                qp.drawText(
                    Pose.pixel_scale(el.x + self.x_shift), 
                    Pose.pixel_scale(World.HEIGHT - el.y + self.y_shift), str(el.get_value()))

    def print_coord(self, qp):
        for els in self._world_matrix:
            for el in els:
                qp.drawText(
                    Pose.pixel_scale(el.x + self.x_shift), 
                    Pose.pixel_scale(World.HEIGHT - el.y + self.y_shift), str(round(el.x, 3)) + "/" + str(round(el.y, 3)))
    
    def print_path(self, qp):
        if len(self.path) > 0:
            qp.setPen(QtGui.QColor(217,95,14))
            last_el = self.path[0]
            for el in self.path:
                last_el_px = Pose.xy_to_pixel(last_el[0], last_el[1])
                el_px = Pose.xy_to_pixel(el[0], el[1])
                qp.drawLine(last_el_px[0], last_el_px[1], el_px[0], el_px[1])
                last_el = el
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