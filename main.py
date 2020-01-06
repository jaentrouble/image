import pygame
import numpy as np
import os
import loader
import backimg

PATH = 'img'

class Main() :
    def __init__(self, width = 1280, height = 1024, fps = 60) :
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((255,255,255))
        self.background.convert()
        self.clock = pygame.time.Clock()
        self.allgroup = pygame.sprite.LayeredDirty()
        self.groupsetter()
        
    def groupsetter(self) :
        backimg.BackImage.groups = self.allgroup

    def run(self) :
        mainloop = True
        self.screen.blit(self.background, (0,0))
        print('start loading')
        self.img = backimg.BackImage(PATH)
        print('loaded')

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

            self.allgroup.clear(self.screen, self.background)
            self.allgroup.draw(self.screen)
            pygame.display.flip()

if __name__ == '__main__' :
    Main().run()