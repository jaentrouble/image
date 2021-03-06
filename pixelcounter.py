import pygame
import numpy as np
import os
from common import loader
from common import backimg
from common import exporter
from common.constants import *
import pixelc

class Main() :
    def __init__(self, fps = 60) :
        pygame.init()
        self.allgroup = pygame.sprite.LayeredDirty()
        self.groupsetter()
        print('start loading')
        self.img = backimg.BackImage(PATH)
        print('loaded')
        self.width, self.height = self.img.get_max_size()
        self.height = max([self.height, D_HEIGHT])
        self.text_rect = pygame.Rect(self.width, 0 , TEXT_WIDTH, self.height)
        self.width += TEXT_WIDTH
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((255,255,255))
        self.background.convert()
        self.clock = pygame.time.Clock()
        self.saver = exporter.Saver()

    def groupsetter(self) :
        backimg.BackImage.groups = self.allgroup
        pixelc.worker.Worker.groups = self.allgroup
        pixelc.worker.Line.groups = self.allgroup
        pixelc.worker.Bucket.groups = self.allgroup
        pixelc.texts.Texts.groups = self.allgroup

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.worker = pixelc.worker.Worker(self.img)
        self.text = pixelc.texts.Texts(self.text_rect, self.worker, self.img)
        self.line_mode = False
        self.bucket_mode = False
        self.clear_check = False
        self.unit_mode = False

        while mainloop :
            self.clock.tick(self.fps)
            ####escape########
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    mainloop = False
                    break
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        mainloop = False
                        break
            ##############################################
                    elif event.key == pygame.K_RIGHT :
                        self.img.forward()
                    elif event.key == pygame.K_LEFT :
                        self.img.backward()
                        
                    # Unit setting mode
                    elif event.key == pygame.K_F1 :
                        self.unit_mode = not self.unit_mode
                        self.line_mode = False
                        self.bucket_mode = False

                    # Clear all
                    if not self.unit_mode:
                        if event.key == pygame.K_c :
                            if not self.clear_check :
                                self.clear_check = True
                                self.text.clear_check()
                            else :
                                self.worker.clear_all()
                                self.clear_check = False
                                self.text.clear_not()

                        # Line mode
                        elif event.key == pygame.K_l :
                            if self.line_mode :
                                self.worker.end_line()
                            if self.bucket_mode :
                                self.bucket_mode = False
                            self.line_mode = not self.line_mode
                            if self.line_mode :
                                self.text.mode_changed(MODE_LINE)
                            else :
                                self.text.mode_changed(MODE_NONE)

                        # Undo
                        elif event.key == pygame.K_z :
                            self.worker.undo()

                        #Bucket mode
                        elif event.key == pygame.K_b :
                            if self.line_mode :
                                self.line_mode = False
                                self.worker.end_line()
                            self.bucket_mode = not self.bucket_mode
                            if self.bucket_mode :
                                self.text.mode_changed(MODE_BUCKET)
                            else :
                                self.text.mode_changed(MODE_NONE)

                        #Set counting
                        elif event.key == pygame.K_t :
                            if not self.clear_check :
                                self.clear_check = True
                                self.text.clear_check()
                            else :
                                self.worker.clear_all()
                                self.worker.set_image()
                                self.clear_check = False
                                self.text.clear_not()                            

                        #Save
                        elif event.key == pygame.K_s :
                            if self.saver.save(self.worker.flush_record()) :
                                self.text.save_complete()
                            else :
                                self.text.save_failed()

                        ###color change
                        elif event.key == pygame.K_1 :
                            pixelc.worker.DRAW_COLOR = COLOR_LIST[RED]
                        elif event.key == pygame.K_2 :
                            pixelc.worker.DRAW_COLOR = COLOR_LIST[GREEN]
                        elif event.key == pygame.K_3 :
                            pixelc.worker.DRAW_COLOR = COLOR_LIST[BLUE]
                        elif event.key == pygame.K_4 :
                            pixelc.worker.DRAW_COLOR = COLOR_LIST[WHITE]
                        elif event.key == pygame.K_5 :
                            pixelc.worker.DRAW_COLOR = COLOR_LIST[BLACK]
                    
                    if event.key != pygame.K_c and event.key != pygame.K_t:
                        self.text.clear_not()
                    if self.unit_mode :
                        self.text.unit_mode_update()
                    else :
                        self.text.update_image()
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[0] :
                        if self.line_mode :
                            self.worker.order_line()
                        if self.bucket_mode :
                            self.worker.bucket_fill()
                        if self.unit_mode :
                            self.text.unit_mode_update()
                        else :
                            self.text.update_image()
            self.allgroup.update()
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            pygame.display.flip()


if __name__ == '__main__' :
    Main().run()