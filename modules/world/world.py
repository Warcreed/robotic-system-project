import math

from .block import *
from .obstacle import *
from .bowl import *
import random

class World:

    FLOOR_LEVEL = -0.020
    HEIGHT = 0.42
    WIDTH = 0.5

    def __init__(self, ui):
        self.__blocks = [ ]
        self.__obstacles = [ 
            Obstacle(x = 220, y = 365, type = 0),
            Obstacle(x = 420, y = 350, type = 1),
            Obstacle(x = 430, y = 210, type = 2),
            Obstacle(x = 309, y = 165, type = 3),
            Obstacle(x = 218, y = 64, type = 4),
            Obstacle(x = 100, y = 110, type = 5)
        ]
        self.__bowl = Bowl(x = 0.04, y = Bowl.HEIGHT + World.FLOOR_LEVEL, a = 0)
        self.__block_slots = [
            BlockSlot(x = 0.145, y = 0.064, a = 0),       
            BlockSlot(x = 0.20, y = World.FLOOR_LEVEL, a = 0),
            BlockSlot(x = 0.24, y = World.FLOOR_LEVEL, a = 0),
            BlockSlot(x = 0.3, y = 0.1, a = 0),       
            BlockSlot(x = 0.285, y = 0.18, a = 90),       
            BlockSlot(x = 0.25, y = 0.25, a = 101),       
            BlockSlot(x = 0.205, y = 0.285, a = 0),       
            BlockSlot(x = 0.152, y = 0.332, a = -110),       
            BlockSlot(x = 0.11, y = 0.305, a = -24),       
            BlockSlot(x = 0.045, y = 0.292, a = -50),       
        ]

        self.ui = ui

        # print check
        self.print_block_slots = True

        self.collected_block_index = None

    def get_obstacles(self):
        return self.__obstacles

    def get_bowl(self):
        return self.__bowl

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

    def sense_block_presence(self):
        (x,y,a) = self.ui.arm.get_pose_xy_a().get_pose()
        L = self.ui.arm.element_3_model.L
        x_1 = (2.2*L) * math.cos(a) + x       # sposta punto di controllo su end effector
        y_1 = (2.2*L) * math.sin(a) + y       # simula la presenza di un raggio o vettore che interseca il blocco
        for b in self.__blocks:               # rilevarne la presenza
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                return True
        return False

    def sense_color(self):
        (x,y,a) = self.ui.arm.get_pose_xy_a().get_pose()
        L = self.ui.arm.element_3_model.L
        x_1 = (2.2*L) * math.cos(a) + x       # sposta punto di controllo su end effector
        y_1 = (2.2*L) * math.sin(a) + y       # simula la presenza di un raggio o vettore che interseca il blocco
        for b in self.__blocks:               # rilevarne il colore
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                return b.get_color()        
        return None

    def collect_block(self):
        (x,y,a) = self.ui.arm.get_pose_xy_a().get_pose()
        L = self.ui.arm.element_3_model.L
        x_1 = (2.2*L) * math.cos(a) + x       # sposta punto di controllo su end effector
        y_1 = (2.2*L) * math.sin(a) + y       # simula la presenza di un raggio o vettore che interseca il blocco
        for b in self.__blocks:               # rilevarne il colore
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                self.collected_block_index = self.__blocks.index(b)
                slot_index = b.get_slot_index()
                self.__block_slots[slot_index].set_as_free()
                return b.collect()
        return None
    
    def drop_block(self):
        if self.collected_block_index is not None:
            self.__blocks[self.collected_block_index].drop()
            self.collected_block_index = None
            if len(list(filter(lambda slot: slot.is_busy(), self.__block_slots)))== 0:
                 self.__blocks = []
        return 

    def paint(self, qp):
        qp.setPen(QtGui.QColor(217,95,14))
        y = Pose.xy_to_pixel(0, World.FLOOR_LEVEL)[1]
        qp.drawLine(50, y, 1450, y)
        qp.drawLine(50, y+1, 1450, y+1)

        self.__bowl.paint(qp)
        for o in self.__obstacles:
            o.paint(qp)
        if self.print_block_slots:
            for b in self.__block_slots:
                b.paint(qp)
        for b in self.__blocks:
            b.paint(qp, self.ui.arm, self.ui.t)


        

