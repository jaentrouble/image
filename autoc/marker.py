import pygame
from common.constants import *

def groupsetter(*groups) :
    Alphago.groups = groups
    Wrong.groups = groups
    User.groups = groups

class Markers() :
    def __init__(self) :
        self.alphago_choices = []
        self.alphago_markers = []
        self.wrong_choices = []
        self.wrong_markers = []
        self.user_choices = []
        self.user_markers = []

    def wrong_choice(self) :
        for am in self.alphago_markers :
            if am.mouse_collide() :
                wc = am.get_center()
                if not(wc in self.wrong_choices):
                    self.wrong_choices.append(wc)
                    self.wrong_markers.append(Wrong(wc))

    
class Alphago(pygame.sprite.DirtySprite) :
    image = pygame.Surface((AUTO_width2, AUTO_width2))
    image.fill(AUTO_alphago_color)
    image.set_colorkey(TRANS_COLOR)
    temp = pygame.Surface((AUTO_width2-2, AUTO_width2-2))
    temp.fill(TRANS_COLOR)
    image.blit(temp,(1,1))
    def __init__(self, pos : list) :
        super().__init__(self.groups)
        self.image = Alphago.image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]

    def mouse_collide(self) :
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def get_center(self) :
        return [self.rect.centerx, self.rect.centery]
        
class Wrong(pygame.sprite.DirtySprite) :
    image = pygame.Surface((AUTO_width2, AUTO_width2))
    image.fill(TRANS_COLOR)
    image.set_colorkey(TRANS_COLOR)
    pygame.draw.line(image, AUTO_wrong_color, [0,0], [AUTO_width2,AUTO_width2], 2)
    pygame.draw.line(image, AUTO_wrong_color, [0,AUTO_width2], [AUTO_width2,0], 2)
    def __init__(self, pos: list) :
        super().__init__(self.groups)
        self.image = Wrong.image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]

class User(pygame.sprite.DirtySprite) :
    image = pygame.Surface((AUTO_width2, AUTO_width2))
    image.fill(AUTO_user_color)
    image.set_colorkey(TRANS_COLOR)
    temp = pygame.Surface((AUTO_width2-2, AUTO_width2-2))
    temp.fill(TRANS_COLOR)
    image.blit(temp,(1,1))
    def __init__(self, pos : list) :
        super().__init__(self.groups)
        self.image = User.image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]
