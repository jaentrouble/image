import pygame
from common import loader
import numpy as np
from common.constants import *

def groupsetter(*groups) :
    BackImage.groups = groups

class BackImage (pygame.sprite.DirtySprite):
    def __init__ (self, path : str) :
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.imgs, self.img_names = loader.l_loader(path)
        self.img_idx = 0
        self.img_max = len(self.imgs) - 1
        self.image = self.imgs[self.img_idx]
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.array = pygame.surfarray.array3d(self.image)

    def __len__(self) :
        return len(self.imgs)

    def get_rect(self) :
        return self.rect.copy()

    def get_index(self) :
        return self.img_idx

    def get_names(self) :
        return self.img_names.copy()

    def get_max_size(self) :
        width = 0
        height = 0
        for image in self.imgs :
            if image.get_width() > width :
                width = image.get_width()
            if image.get_height() > height :
                height = image.get_height()
        return [width, height]

    def forward (self) :
        """
        increases image index by 1
        if reached the end, goes to 0
        returns the new index
        """
        self.img_idx += 1
        if self.img_idx > self.img_max :
            self.img_idx = 0
        self.img_reload()
        return self.img_idx

    def backward (self) :
        """
        decreases image index by 1
        if reached 0, goes to the end
        returns the new index
        """
        self.img_idx -= 1
        if self.img_idx < 0 :
            self.img_idx = self.img_max
        self.img_reload()
        return self.img_idx

    def img_reload (self) :
        self.image = self.imgs[self.img_idx]
        self.dirty = 1
        self.image.convert()
        self.rect = self.image.get_rect()
        self.array = pygame.surfarray.array3d(self.image)

    def get_original_array(self) :
        return self.array.copy()

    def get_current_array(self) :
        return pygame.surfarray.array3d(self.image)

    def color_mode(self, target_color: list) :
        temp = self.array.copy()
        if target_color == DEFAULT :
            self.img_reload()
            return
        else :
            for column in temp :
                for color in column :
                    if not target_color[0] :
                        color[0] = 0
                    if not target_color[1] :
                        color[1] = 0
                    if not target_color[2] :
                        color[2] = 0
            self.image = pygame.surfarray.make_surface(temp)
            self.image.convert()
            self.dirty = 1
