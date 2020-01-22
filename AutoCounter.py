import pygame
import numpy as np
import os
from common import loader
from common import backimg
from common import exporter
from common.constants import *
from autoc import worker
from autoc import marker
from autoc import texts

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
        backimg.groupsetter(self.allgroup)
        worker.groupsetter(self.allgroup)
        marker.groupsetter(self.allgroup)
        texts.groupsetter(self.allgroup)

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.mode = MODE_NONE
        self.worker = worker.Worker(self.img)
        self.texts = texts.Texts(self.text_rect, self.worker)
        self.texts.update_text()

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
            ########################
                    # change image
                    elif event.key == pygame.K_RIGHT :
                        self.img.forward()
                    elif event.key == pygame.K_LEFT :
                        self.img.backward()
                    elif event.key == pygame.K_t :
                        self.worker.set_image()

                    # change big mode
                    elif event.key == pygame.K_F1 :
                        self.worker.big_mode_change()
                        self.texts.mode_changed()
                    # change mode
                    elif event.key == pygame.K_f :
                        self.worker.mode_wrong()
                        self.texts.mode_changed()
                    elif event.key == pygame.K_a :
                        self.worker.mode_user()
                        self.texts.mode_changed()
                    elif event.key == pygame.K_l :
                        self.worker.mode_line()
                        self.texts.mode_changed()
                    elif event.key == pygame.K_b :
                        self.worker.mode_bucket()
                        self.texts.mode_changed()

                    # calculate
                    elif event.key == pygame.K_c :
                        self.worker.calculate()
                    
                    # save
                    elif event.key == pygame.K_s:
                        self.worker.flush_record()

                    # undo
                    elif event.key == pygame.K_z :
                        self.worker.undo()
                    
                    #update text
                    self.texts.update_text()

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[0] :
                        self.worker.mouse_clicked()

                    #update text
                    self.texts.update_text()
        
            self.allgroup.update()
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            pygame.display.flip()

if __name__ == '__main__' :
    Main().run()