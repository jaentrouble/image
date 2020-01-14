import pygame
import numpy as np
from common import backimg
from common.constants import *

class Worker(pygame.sprite.DirtySprite) :
    def __init__(self, target : backimg.BackImage) :
        super().__init__(self.groups)
        self.size = 10
        self.target = target
        self.image_setter()
        self.dots = []
        self.standard = np.array([255,255,255])
        self.ratio_record = []
        self.img_idx = []

    def get_image_length(self) :
        return len(self.target)

    def get_index(self) :
        return self.target.get_index()

    def image_setter(self) :
        self.image = pygame.Surface((self.size,self.size))
        self.image.fill((255,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        temp = pygame.Surface((self.size-2, self.size-2))
        temp.fill((0,0,0))
        self.image.blit(temp, (1,1))
        self.image.convert_alpha()
        self.dirty = True

    def calculate_gray(self, color : np.array) :
        return (color[0]**2 + color[1]**2 + color[2]**2)/np.sum(color)

    def set_standard(self) :
        self.standard = self.calculate_mean()

    def get_standard(self) :
        return self.standard

    def takeout_pin(self) :
        if len(self.dots) != 0 :
            self.ratio_record.pop()
            self.img_idx.pop()
            dead = self.dots.pop()
            dead.kill()

    def get_records(self) :
        return self.ratio_record.copy()

    def flush_records(self) :
        total = []
        tmp = self.ratio_record
        self.ratio_record = []
        tmpidx = self.img_idx
        self.img_idx = []
        for _ in range(len(self.dots)):
            dead = self.dots.pop()
            dead.kill()
        for i in range(len(tmp)) :
            total.append([tmp[i],tmpidx[i]])
        return total

    def record_ratio(self) :
        self.ratio_record.append(self.get_ratio(True))
        self.img_idx.append(self.target.get_index())

    def get_ratio(self, pin : bool = True) :
        c = self.calculate_mean()
        if pin :
            self.dots.append(Dot(self.rect))
        return self.calculate_gray(c)/self.calculate_gray(self.standard)

    def calculate_mean(self) :
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        bottom = self.rect.bottom
        array = self.target.get_current_array()
        if left >= len(array) or top >= len(array[0]) :
            return
        c = np.zeros(3)
        px = 0
        for column in array[left:right] :
            for color in column[top:bottom] :
                c += color
                px += 1
        return c/px

    def update(self) :
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()
        self.dirty = True
    
    def increase_size(self) :
        self.size += 2
        self.image_setter()

    def decrease_size(self) :
        if self.size > 2 :
            self.size -= 2
            self.image_setter()

class Dot(pygame.sprite.DirtySprite) :
    def __init__(self, rect : pygame.Rect) :
        super().__init__(self.groups)
        self.rect = rect.copy()
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(DRAW_COLOR)
