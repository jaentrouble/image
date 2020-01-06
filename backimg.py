import pygame
import loader
import numpy as np

class BackImage (pygame.sprite.DirtySprite):
    def __init__ (self, path : str) :
        pygame.sprite.DirtySprite.__init__(self, self.groups)
        self.imgs = loader.l_loader(path)
        self.img_idx = 0
        self.img_max = len(self.imgs) - 1
        self.image = self.imgs[self.img_idx]
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.array = pygame.surfarray.array3d(self.image)

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
        self.array = pygame.surfarray.array3d(self.image)