import pygame
from common import backimg
from common.constants import *
from autoc import worker

def groupsetter(*groups) :
    Texts.groups = groups

class Texts(pygame.sprite.DirtySprite) :
    def __init__(self, area : pygame.Rect, agent : worker.Worker, img : backimg.BackImage) :
        super().__init__(self.groups)
        self.font = pygame.font.SysFont('Arial', 20)
        self.rect = area
        self.agent = agent
        self.back_img = img
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.big_mode = agent.get_big_mode()
        self.mode = agent.get_mode()
        self.convert = agent.get_convert_mode()
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
        self.convert_fonts = [
            self.font.render('convert_red', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('convert_green', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('convert_blue', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('convert_weighted', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('convert_min', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('convert_min_yellow', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('not_yet_defined', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('not_yet_defined', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('not_yet_defined', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
            self.font.render('not_yet_defined', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]),
        ]


    def mode_changed(self) :
        self.big_mode = self.agent.get_big_mode()
        self.mode = self.agent.get_mode()
        self.convert = self.agent.get_convert_mode()
        self.update()

    def update_text(self) :
        self.image.fill(COLOR_LIST[WHITE])
        surfs = []
        surfs.append(self.big_mode_fonts[self.big_mode])
        surfs.append(self.mode_fonts[self.mode])
        surfs.append(self.convert_fonts[self.convert])

        counting_idx = self.agent.get_index()
        current_image_idx = self.back_img.get_index()
        index_text1 = 'Total index : 0 ~ {}'.format(len(self.back_img)-1)
        index_text2 = 'Current image index : {}'.format(current_image_idx)
        index_text3 = 'Counting target index : {}'.format(counting_idx)
        surfs.append(self.font.render(index_text1,
                                    False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        surfs.append(self.font.render(index_text2,
                                    False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        surfs.append(self.font.render(index_text3,
                                    False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        if counting_idx != current_image_idx :
            warning_text = 'Warning: Different index'
            surfs.append(self.font.render(warning_text,
                                False, COLOR_LIST[RED], COLOR_LIST[WHITE]))


        y=0
        for s in surfs :
            self.image.blit(s, (0, y))
            y += 40
        self.dirty = True
        