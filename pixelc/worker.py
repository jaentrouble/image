import pygame
import numpy as np
from constants import *
import backimg

class Worker() :
    def __init__(self, target : backimg.BackImage) :
        self.target = target
        self.line_thickness = 2
        self.masks = []
        self.l_s_pos = None

    def set_image (self) :
        self.reference = self.target.get_current_array()
        self.width = self.reference.shape[0]
        self.height = self.reference.shape[1]
        self.table = np.zeros((self.width, self.height))

    def undo (self) :
        if len(self.masks) != 0 :
            dead = self.masks.pop()
            dead.kill()

    def order_line (self) :
        if self.l_s_pos == None :
            self.line_start()
        else :
            self.line_continue()    

    def line_start(self) :
        self.l_s_pos = pygame.mouse.get_pos()

    def line_continue(self) :
        self.l_e_pos = pygame.mouse.get_pos()
        self.masks.append(Line(self.l_s_pos, self.l_e_pos, self.line_thickness))
        self.l_s_pos = self.l_e_pos

    def end_line(self) :
        self.l_s_pos = None


class Line(pygame.sprite.DirtySprite) :
    def __init__(self, startpos, endpos, thick) :
        super().__init__(self.groups)
        self.left = min(startpos[0],endpos[0])
        self.top = min(startpos[1],endpos[1])
        self.width = abs(startpos[0]-endpos[0])
        self.height = abs(startpos[1]-endpos[1])
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        if (startpos[0]-endpos[0])*(startpos[1]-endpos[1]) >= 0 :
            # left-top to right-bottom
            pygame.draw.line(self.image, DRAW_COLOR, [0, 0], [self.width, self.height], thick)
        else :
            pygame.draw.line(self.image, DRAW_COLOR, [0, self.height],[self.width, 0], thick)
        self.image.convert_alpha()

    def get_color_arr(self) :
        """
        return : [pos of filled cells(absolute)]
        """
        filled = []
        array = pygame.surfarray.array3d(self.image)
        x = self.left
        y = self.top
        for column in array :
            for color in column :
                if np.all(color == (0,0,0)) :
                    filled.append([x,y])
                x+=1
                y+=1
        return filled