import pygame
import numpy as np
import os
import loader
import backimg
import worker
from constants import *
import texts

PATH = 'img'
TEXT_WIDTH = 200

class Main() :
    def __init__(self, fps = 60) :
        pygame.init()
        self.allgroup = pygame.sprite.LayeredDirty()
        self.groupsetter()
        print('start loading')
        self.img = backimg.BackImage(PATH)
        print('loaded')
        self.width, self.height = self.img.get_max_size()
        self.text_rect = pygame.Rect(self.width,0,TEXT_WIDTH,self.height)
        self.width += TEXT_WIDTH
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((255,255,255))
        self.background.convert()
        self.clock = pygame.time.Clock()
        self.color = [True, True, True] #r,g,b
        
    def groupsetter(self) :
        backimg.BackImage.groups = self.allgroup
        worker.Worker.groups = self.allgroup
        worker.Dot.groups = self.allgroup
        texts.Texts.groups = self.allgroup

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.worker = worker.Worker(self.img)
        self.text = texts.Texts(self.color, self.text_rect, self.worker)

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
                        for i in range(3): self.color[i] = True
                    elif event.key == pygame.K_LEFT :
                        self.img.backward()
                        for i in range(3): self.color[i] = True
                    elif event.key == pygame.K_1 :
                        self.color[0] = not self.color[0]
                        self.img.color_mode(self.color)
                    elif event.key == pygame.K_2 :
                        self.color[1] = not self.color[1]
                        self.img.color_mode(self.color)
                    elif event.key == pygame.K_3 :
                        self.color[2] = not self.color[2]
                        self.img.color_mode(self.color)
                    elif event.key == pygame.K_4 :
                        for i in range(3): self.color[i] = True
                        self.img.color_mode(DEFAULT)
                    elif event.key == pygame.K_RIGHTBRACKET :
                        self.worker.increase_size()
                    elif event.key == pygame.K_LEFTBRACKET :
                        self.worker.decrease_size()
                    elif event.key == pygame.K_z :
                        self.worker.takeout_pin()
                    self.text.update_image()
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[2] :
                        self.worker.set_standard()
                    elif pygame.mouse.get_pressed()[0] :
                        self.worker.record_ratio()
                    self.text.update_image()
            self.allgroup.update()
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            pygame.display.flip()

if __name__ == '__main__' :
    Main().run()