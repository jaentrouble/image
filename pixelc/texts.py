import pygame
from common import backimg
from common.constants import *
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
        self.helps.append(self.font.render('F1 : Set Unit Ratio',
                                       False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        self.helps.append(self.font.render('COLOR DOES NOT EFFECT COUNTING',
                                       False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        self.help_end = 10 + 30*len(self.helps)

        self.unit_infos = []
        self.unit_infos.append(self.warning_font.render(
            'Setting mode  F1: Exit', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]
        ))
        self.unit_infos.append(self.font.render(
            'Left click two ends of Unit', False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]
        ))
        self.button1 = self.warning_font.render('+1', False, COLOR_LIST[WHITE], COLOR_LIST[BLACK])
        self.button10 = self.warning_font.render('+10', False, COLOR_LIST[WHITE], COLOR_LIST[BLACK])
        self.button50 = self.warning_font.render('+50', False, COLOR_LIST[WHITE], COLOR_LIST[BLACK])
        self.button1_m = self.warning_font.render('-1', False, COLOR_LIST[WHITE], COLOR_LIST[BLACK])
        self.button10_m = self.warning_font.render('-10', False, COLOR_LIST[WHITE], COLOR_LIST[BLACK])
        self.button50_m = self.warning_font.render('-50', False, COLOR_LIST[WHITE], COLOR_LIST[BLACK])
        self.warning_font.render('+ 1', False, COLOR_LIST[WHITE], COLOR_LIST[BLACK])
        self.saved = False
        self.save_fail = False
        self.mode = MODE_NONE
        self.clear_info = False
        self.update_image()

    def mode_changed(self, mode : int):
        self.mode = mode

    def clear_check(self) :
        self.clear_info = True

    def clear_not (self) :
        self.clear_info = False

    def update_image(self) :
        if self.mode != MODE_UNIT :
            self.normal_mode_update()
        else :
            pass

    def unit_mode_update(self) :
        self.image.fill(COLOR_LIST[WHITE])
        info_surfs = []
        info_end = len(self.unit_infos)
        for i in range(info_end) :
            self.image.blit(self.unit_infos[i], (0, 10 + 40*i))
        y = 10 + 40*(info_end + 3) #plus 3 for a line at the bottom
        self.image.blit(self.button1, (0, y))
        area1 = self.button1.get_rect(x=0, y=y)
        y+=40
        self.image.blit(self.button10, (0,y))
        area10 = self.button10.get_rect(x=0, y=y)
        y+=40
        self.image.blit(self.button50, (0,y))
        area50 = self.button50.get_rect(x=0, y=y)
        y+=40
        self.image.blit(self.button1_m, (0,y))
        area1_m = self.button1_m.get_rect(x=0, y=y)
        y+=40
        self.image.blit(self.button10_m, (0,y))
        area10_m = self.button10_m.get_rect(x=0, y=y)
        y+=40
        self.image.blit(self.button50_m, (0,y))
        area50_m = self.button50_m.get_rect(x=0, y=y)
        
        if pygame.mouse.get_pressed()[0] :
            pos = list(pygame.mouse.get_pos())
            pos[0] -= self.rect.left
            if area1.collidepoint(pos) :
                self.agent.delta_actual(1)
            elif area10.collidepoint(pos) :
                self.agent.delta_actual(10)
            elif area50.collidepoint(pos) :
                self.agent.delta_actual(50)
            elif area1_m.collidepoint(pos) :
                self.agent.delta_actual(-1)
            elif area10_m.collidepoint(pos) :
                self.agent.delta_actual(-10)
            elif area50_m.collidepoint(pos) :
                self.agent.delta_actual(-50)
            elif pos[0] < 0 :
                self.agent.set_unit()
        info_surfs.append(self.font.render(
            '{0:.2f} um^2 per {1} pixels'.format(
                self.agent.get_ratio()*UNIT_PIXEL_DEFAULT,
                UNIT_PIXEL_DEFAULT
            ),
            False,
            COLOR_LIST[BLACK],
            COLOR_LIST[WHITE],
        ))     

        info_surfs.append(self.font.render(
            'Unit length : {:.2f} um'.format(
                self.agent.get_unit_actual()
            ),
            False,
            COLOR_LIST[BLACK],
            COLOR_LIST[WHITE],
        ))   

        if self.agent.get_pinned() :
            info_surfs.append(self.font.render(
                'Click at the End point',
                False,
                COLOR_LIST[BLACK],
                COLOR_LIST[WHITE],
            ))   
        else :
            info_surfs.append(self.font.render(
                'Click at the Start point',
                False,
                COLOR_LIST[BLACK],
                COLOR_LIST[WHITE],
            ))   


        for i in range(len(info_surfs)) :
            self.image.blit(info_surfs[i], (0, 10 + 40*(info_end+i)))
        
        self.dirty = True
        self.saved = False
        self.save_fail = False

            
    def normal_mode_update(self) :
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
        info_surfs.append(self.font.render('Color : ' + current_color,
                                        False, word_color, back_color))
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

        if self.clear_info :
            info_surfs.append(self.warning_font.render('Clear all?',
                                        False, COLOR_LIST[RED], COLOR_LIST[WHITE]))
        
        info_surfs.append(self.font.render('Area : {:.2f} um^2'.format(self.agent.calculate_area()), False, COLOR_LIST[BLACK], COLOR_LIST[WHITE]))
        info_surfs.append(self.font.render(
            '{0:.2f} um^2 per {1} pixels'.format(
                self.agent.get_ratio()*UNIT_PIXEL_DEFAULT,
                UNIT_PIXEL_DEFAULT
            ),
            False,
            COLOR_LIST[BLACK],
            COLOR_LIST[WHITE],
        ))     
        for i in range(len(info_surfs)) :
            self.image.blit(info_surfs[i], (0, self.help_end + 30*i))
        
        self.dirty = True
        self.saved = False
        self.save_fail = False

    def save_complete(self) :
        self.saved = True

    def save_failed(self) :
        self.save_fail = True
