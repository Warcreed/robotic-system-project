import math

from .block import *
from .obstacle import *
from .bowl import *

class World:

    FLOOR_LEVEL = -0.015

    def __init__(self, ui):
        self.__blocks = [ ]
        self.__obstacles = [ 
            Obstacle(x = 0.3, y = 0.1, a = 0, type = 2),
            Obstacle(x = 0.31, y = 0.23, a = 0, type = 1),
            Obstacle(x = 0.24, y = 0.27, a = -45, type = 0),
            Obstacle(x = 0.03, y = 0.38, a = 45, type = 4),
            Obstacle(x = -0.02, y = 0.335, a = 0, type = 4),
            Obstacle(x = 0.15, y = 0.095, a = -45, type = 2, w = 0.055, h = 0.055),
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

    def new_block(self, uColor):
        slot = random.choice(self.__block_slots)
        while slot.is_busy():
            slot = random.choice(self.__block_slots)
        slot.set_as_busy()
        (x, y, a) = slot.get_slot_pose()
        b = Block(x, y, a, uColor)
        self.__blocks.append(b)

    def count_blocks(self):
        return len(self.__blocks)

    def get_block_slot_at(self, index):
        return self.__block_slots[index]

    def sense_block_presence(self):
        (x,y,a) = self.ui.arm.get_pose_xy_a().get_pose()
        L = self.ui.arm.element_3_model.L
        x_1 = (2*L) * math.cos(a) + x       # sposta punto di controllo su end effector
        y_1 = (2*L) * math.sin(a) + y       # simula la presenza di un raggio o vettore che interseca il blocco
        for b in self.__blocks:               # rilevarne la presenza
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                return True
        return False

    def sense_color(self):
        (x,y,a) = self.ui.arm.get_pose_xy_a().get_pose()
        L = self.ui.arm.element_3_model.L
        x_1 = (2*L) * math.cos(a) + x       # sposta punto di controllo su end effector
        y_1 = (2*L) * math.sin(a) + y       # simula la presenza di un raggio o vettore che interseca il blocco
        for b in self.__blocks:               # rilevarne il colore
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                return b.get_color()
        return None

    def collect_block(self):
        (x,y,a) = self.ui.arm.get_pose_xy_a().get_pose()
        L = self.ui.arm.element_3_model.L
        x_1 = (2*L) * math.cos(a) + x       # sposta punto di controllo su end effector
        y_1 = (2*L) * math.sin(a) + y       # simula la presenza di un raggio o vettore che interseca il blocco
        for b in self.__blocks:               # rilevarne il colore
            (xb,yb,ab) = b.get_pose()           
            if (x_1 >= xb)and(x_1 <= (xb + Block.WIDTH)) and (y_1 >= yb)and(y_1 <= (yb + Block.WIDTH)):
                self.collected_block_index = self.__blocks.index(b)
                return b.collect()
        return None
    
    def drop_block(self):
        if self.collected_block_index is not None:
            self.__blocks[self.collected_block_index].drop()
            self.collected_block_index = None
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


        

