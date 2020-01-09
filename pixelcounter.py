import pygame
import numpy as np
import os
import loader
import backimg
import exporter
from constants import *
from pixelc import worker

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
        worker.Worker.groups = self.allgroup
        worker.Line.groups = self.allgroup
        worker.Bucket.groups = self.allgroup

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        self.worker = worker.Worker(self.img)
        self.line_mode = False
        self.bucket_mode = False

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
                    elif event.key == pygame.K_l :
                        if self.line_mode :
                            self.worker.end_line()
                        if self.bucket_mode :
                            self.bucket_mode = False
                        self.line_mode = not self.line_mode
                    elif event.key == pygame.K_z :
                        self.worker.undo()
                    elif event.key == pygame.K_b :
                        if self.line_mode :
                            self.line_mode = False
                            self.worker.end_line()
                        self.bucket_mode = not self.bucket_mode
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if pygame.mouse.get_pressed()[0] :
                        if self.line_mode :
                            self.worker.order_line()
                        if self.bucket_mode :
                            self.worker.bucket_fill()
                        print(self.worker.count_color())
            self.allgroup.update()
            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            pygame.display.flip()


if __name__ == '__main__' :
    Main().run()