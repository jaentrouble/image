import pygame
from common.constants import *
from autoc import alphago

def groupsetter(*groups) :
    Alphago_mark.groups = groups
    Wrong_mark.groups = groups
    User_mark.groups = groups

class Markers() :
    def __init__(self) :
        self.alphago_choices = []
        self.alphago_markers = []
        self.wrong_choices = []
        self.wrong_markers = []
        self.user_choices = []
        self.user_markers = []
        self.alphago = alphago.Alphago(AUTO_default_filename)

    def undo_wrong(self) :
        if len(self.wrong_choices) != 0 :
            dead = self.wrong_markers.pop()
            dead.kill()
            self.wrong_choices.pop()

    def undo_user(self) :
        if len(self.user_choices) != 0 :
            dead = self.user_markers.pop()
            dead.kill()
            self.user_choices.pop()

    def wrong_choice(self) :
        for am in self.alphago_markers :
            if am.mouse_collide() :
                wc = am.get_center()
                if not(wc in self.wrong_choices):
                    self.wrong_choices.append(wc)
                    self.wrong_markers.append(Wrong_mark(wc))

    def user_choice(self) :
        uc = pygame.mouse.get_pos()
        self.user_choices.append(uc)
        self.user_markers.append(User_mark(uc))

    def reset(self) :
        for mks in self.alphago_markers :
            mks.kill()
        for mks in self.wrong_markers :
            mks.kill()
        for mks in self.user_markers :
            mks.kill()
        self.alphago_markers = []
        self.wrong_markers = []
        self.user_markers = []
        self.alphago_choices = []
        self.wrong_choices = []
        self.user_choices = []

    def count(self) :
        return len(self.alphago_choices)-len(self.wrong_choices)+len(self.user_choices)

    def fit(self) :
        correct = self.user_choices.copy()
        for ac in self.alphago_choices :
            if not ac in self.wrong_choices :
                correct.append(ac)
        self.alphago.fit(correct, self.wrong_choices.copy(), self.grid, self.array)

    def calculate(self, grid, array) :
        """
        grid : masked cells
        array : 3d array of the target image
        """
        self.reset()
        self.alphago_choices = self.alphago.predict(grid, array)
        self.grid = grid
        self.array = array
        for ac in self.alphago_choices :
            self.alphago_markers.append(Alphago_mark(ac))
    
class Alphago_mark(pygame.sprite.DirtySprite) :
    image = pygame.Surface((AUTO_width2, AUTO_width2))
    image.fill(AUTO_alphago_color)
    image.set_colorkey(TRANS_COLOR)
    temp = pygame.Surface((AUTO_width2-2, AUTO_width2-2))
    temp.fill(TRANS_COLOR)
    image.blit(temp,(1,1))
    def __init__(self, pos : list) :
        super().__init__(self.groups)
        self.image = Alphago_mark.image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]

    def mouse_collide(self) :
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def get_center(self) :
        return [self.rect.centerx, self.rect.centery]
        
class Wrong_mark(pygame.sprite.DirtySprite) :
    image = pygame.Surface((AUTO_width2, AUTO_width2))
    image.fill(TRANS_COLOR)
    image.set_colorkey(TRANS_COLOR)
    pygame.draw.line(image, AUTO_wrong_color, [0,0], [AUTO_width2,AUTO_width2], 2)
    pygame.draw.line(image, AUTO_wrong_color, [0,AUTO_width2], [AUTO_width2,0], 2)
    def __init__(self, pos: list) :
        super().__init__(self.groups)
        self.image = Wrong_mark.image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]

class User_mark(pygame.sprite.DirtySprite) :
    image = pygame.Surface((AUTO_width2, AUTO_width2))
    image.fill(AUTO_user_color)
    image.set_colorkey(TRANS_COLOR)
    temp = pygame.Surface((AUTO_width2-2, AUTO_width2-2))
    temp.fill(TRANS_COLOR)
    image.blit(temp,(1,1))
    def __init__(self, pos : list) :
        super().__init__(self.groups)
        self.image = User_mark.image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos[0], pos[1]
