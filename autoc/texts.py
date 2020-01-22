import pygame
from common import backimg
from common.constants import *
from autoc import worker

def groupsetter(*groups) :
    Texts.groups = groups

class Texts(pygame.sprite.DirtySprite) :
    def __init__(self, area : pygame.Rect, agent : worker.Worker, img = backimg.BackImage) :
        super().__init__(self.groups)
        self.font = pygame.font.SysFont('Arial', 20)
        self.rect = area
        self.agent = agent
        self.back_img = img
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.big_mode = agent.get_big_mode()
        self.mode = agent.get_mode()
        self.big_mode_fonts = [
            self.font.render('Selecting Area Mode', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('Counting Mode', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
        ]
        self.mode_fonts = [
            self.font.render('Mode Unselected', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('Line Mode', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('Bucket Mode', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('Fix Mode', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('Add Mode', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
        ]

    def mode_changed(self) :
        self.big_mode = self.agent.get_big_mode()
        self.mode = self.agent.get_mode()
        self.update()

    def update_text(self) :
        self.image.fill(COLOR_LIST[WHITE])
        surfs = []
        surfs.append(self.big_mode_fonts[self.big_mode])
        surfs.append(self.mode_fonts[self.mode])
        y=0
        for s in surfs :
            self.image.blit(s, (0, y))
            y += 40
        self.dirty = True
        