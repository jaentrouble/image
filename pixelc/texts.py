import pygame
import backimg
from constants import *
import numpy as np
from pixelc import worker

class Texts(pygame.sprite.DirtySprite) :
    def __init__(self, area : pygame.Rect, agent : worker.Worker, img = backimg.BackImage) :
        super().__init__(self.groups)
        self.font = pygame.font.SysFont('Arial', 20)
        self.warning_font = pygame.font.SysFont('Arial', 30)
        self.rect = area
        self.agent = agent
        self.back_img = img
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.helps = []
        self.helps.append(self.font.render('z: Undo | s: Save | L: Line | B: bucket',
                                       False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        self.helps.append(self.font.render('c: Clear all | t: Set counting image',
                                       False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        self.helps.append(self.font.render('1: Red | 2: Green | 3:Blue',
                                       False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        self.helps.append(self.font.render('4: White | 5: Black',
                                       False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        self.helps.append(self.font.render('COLOR DOES NOT EFFECT COUNTING',
                                       False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        self.help_end = 10 + 30*len(self.helps)
        self.saved = False
        self.save_fail = False
        self.mode = MODE_NONE
        self.update_image()

    def mode_changed(self, mode : int):
        self.mode = mode

    def update_image(self) :
        self.image.fill(COLOR_LIST[WHITE])
        info_surfs = []
        for i in range(len(self.helps)) :
            self.image.blit(self.helps[i], (0, 10 + 30*i))
        if worker.DRAW_COLOR == COLOR_LIST[RED] :
            word_color = COLOR_LIST[RED]
            back_color = COLOR_LIST[WHITE]
            current_color = 'Red'
        elif worker.DRAW_COLOR == COLOR_LIST[GREEN] :
            word_color = COLOR_LIST[GREEN]
            back_color = COLOR_LIST[WHITE]
            current_color = 'Green'
        elif worker.DRAW_COLOR == COLOR_LIST[BLUE] :
            word_color = COLOR_LIST[BLUE]
            back_color = COLOR_LIST[WHITE]
            current_color = 'Blue'
        elif worker.DRAW_COLOR == COLOR_LIST[WHITE] :
            word_color = COLOR_LIST[WHITE]
            back_color = COLOR_LIST[BLACK]
            current_color = 'White'
        elif worker.DRAW_COLOR == COLOR_LIST[BLACK] :
            word_color = COLOR_LIST[BLACK]
            back_color = COLOR_LIST[WHITE]
            current_color = 'Black'
        color_status = self.font.render('Color : ' + current_color,
                                        False, word_color, back_color)
        counting_idx = self.agent.get_index()
        current_image_idx = self.back_img.get_index()
        index_text1 = 'Total index : 0 ~ {}'.format(len(self.back_img))
        index_text2 = 'Current image index : {}'.format(current_image_idx)
        index_text3 = 'Counting target index : {}'.format(counting_idx)
        info_surfs.append(self.font.render(index_text1,
                                    False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        info_surfs.append(self.font.render(index_text2,
                                    False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        info_surfs.append(self.font.render(index_text3,
                                    False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        if counting_idx != current_image_idx :
            warning_text = 'Warning: Different index'
            info_surfs.append(self.font.render(warning_text,
                                False, COLOR_LIST[RED], COLOR_LIST[WHITE]))
        if self.saved :
            info_surfs.append(self.font.render('Saved', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        elif self.save_fail :
            info_surfs.append(self.font.render('Save Failed', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        
        if self.mode == MODE_NONE :
            pass
        elif self.mode == MODE_LINE :
            mode = 'Line Drawing'
        elif self.mode == MODE_BUCKET :
            mode = 'Bucket Filling'

        if self.mode != MODE_NONE :
            info_surfs.append(self.font.render(mode, False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        for i in range(len(info_surfs)) :
            self.image.blit(info_surfs[i], (0, self.help_end + 30*i))
        self.dirty = True
        self.saved = False
        self.save_fail = False

    def save_complete(self) :
        self.saved = True

    def save_failed(self) :
        self.save_fail = True