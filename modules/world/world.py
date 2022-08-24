import math

from modules.utils.config import Config

from .block import *
from .obstacle import *
from .bowl import *
import random

class World:

    HEIGHT = 0.42
    WIDTH = 0.5

    def __init__(self, ui):
        self.__blocks = [ ]
        self.__obstacles = Config.obstacles
        self.__bowl = Bowl(x = 0.04, y = Bowl.HEIGHT + Config.FLOOR_LEVEL, a = 0)
        self.__block_slots = Config.block_slots
        self.ui = ui
        self.collected_block_index = None

    def get_obstacles(self):
        return self.__obstacles

    def get_bowl(self):
        return self.__bowl

    # generate new block on map
    def new_block(self, uColor):
        slot = random.choice(self.__block_slots)
        while slot.is_busy():
            slot = random.choice(self.__block_slots)
        slot.set_as_busy()
        (x, y, a) = slot.get_slot_pose()
        b = Block(x, y, a, uColor, self.__block_slots.index(slot))
        self.__blocks.append(b)

    def count_blocks(self):
        return len(self.__blocks)

    def get_block_slot_at(self, index):
        return self.__block_slots[index]

    def get_ray_xy(self):
        (x,y,a) = self.ui.arm.get_pose_xy_a()
        L = self.ui.arm.element_3_model.L
        x_1 = (Config.ray_length_factor*L) * math.cos(a) + x
        y_1 = (Config.ray_length_factor*L) * math.sin(a) + y
        return (x_1, y_1)

    # ray vector simulation which intersects blocks to get if slot is occupied
    def sense_block_presence(self):
        (x_1, y_1) = self.get_ray_xy()
        for b in self.__blocks:
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                return True
        return False

    # ray vector simulation which intersects blocks to get block color
    def sense_color(self):
        (x_1, y_1) = self.get_ray_xy()
        for b in self.__blocks:
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                return b.get_color()        
        return None

    # ray vector simulation which intersects blocks to pick the one in front of the end effector
    def collect_block(self):
        (x_1, y_1) = self.get_ray_xy()     
        for b in self.__blocks:               
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                self.collected_block_index = self.__blocks.index(b)
                slot_index = b.get_slot_index()
                self.__block_slots[slot_index].set_as_free()
                return b.collect()
        return None
    
    # drop picked block into the bowl
    def drop_block(self):
        if self.collected_block_index is not None:
            self.__blocks[self.collected_block_index].drop()
            self.collected_block_index = None
            if len(list(filter(lambda slot: slot.is_busy(), self.__block_slots)))== 0:
                 self.__blocks = []

    def paint_floor_line(self, qp):
        qp.setPen(QtGui.QColor(217,95,14))
        y = Pose.xy_to_pixel(0, Config.FLOOR_LEVEL)[1]
        qp.drawLine(50, y, 750, y)
        qp.drawLine(50, y+1, 750, y+1)

    def paint(self, qp, print_block_slots= False, print_scaled_obstacles= False):
        self.paint_floor_line(qp)
        self.__bowl.paint(qp)
        for o in self.__obstacles:
            o.paint(qp, print_scaled_obstacles)
        if print_block_slots:
            for b in self.__block_slots:
                b.paint(qp)
        for b in self.__blocks:
            b.paint(qp, self.ui.arm, self.ui.t)


        

