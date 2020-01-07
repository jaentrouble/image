import pygame
from constants import *
import worker

class Texts(pygame.sprite.DirtySprite) :
    def __init__(self, color_status : list, area : pygame.Rect, agent : worker.Worker) :
        super().__init__(self.groups)
        self.font = pygame.font.SysFont('None', 25)
        self.color_status = color_status
        self.rect = area
        self.agent = agent
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.help1 = self.font.render('z: Undo',
                                    True, (0,0,0), (255,255,255))
        self.help2 = self.font.render('1:Red 2:Green',
                                    False, (0,0,0), (255,255,255))
        self.help3 = self.font.render('3:Blue 4:Default',
                                    False, (0,0,0), (255,255,255))
        self.update_image()

    def update_image(self) :
        self.image.fill((255,255,255))
        self.red_status = self.font.render('Red : {0}'.format(self.color_status[0]),
                                            False, (255,0,0), (255,255,255))
        self.green_status = self.font.render('Green : {0}'.format(self.color_status[1]),
                                            False, (0,255,0), (255,255,255))
        self.blue_status = self.font.render('Blue : {0}'.format(self.color_status[2]),
                                            False, (0,0,255), (255,255,255))

        self.image.blit(self.red_status, (0, 0))
        self.image.blit(self.green_status, (0, 30))
        self.image.blit(self.blue_status, (0, 60))
        self.image.blit(self.help1, (0,90))
        self.image.blit(self.help2, (0,120))
        self.image.blit(self.help3, (0,150))
        row = 180
        for ratio in self.agent.get_records()[-10:] :
            self.image.blit(self.font.render('{0:.2f}'.format(ratio), False,
                                             (0,0,0), (255,255,255)),(0,row))
            row += 30
        self.image.blit(self.font.render('total : {0} values'.format(len(self.agent.get_records())),
                                        False, (0,0,0), (255,255,255)),(0,500))
        self.image.blit(self.font.render('base red : {0}'.format(self.agent.get_standard()[0]),
                                        False, (0,0,0), (255,255,255)),(0,550))
        self.image.blit(self.font.render('base green : {0}'.format(self.agent.get_standard()[1]),
                                        False, (0,0,0), (255,255,255)),(0,580))
        self.image.blit(self.font.render('base blue : {0}'.format(self.agent.get_standard()[2]),
                                        False, (0,0,0), (255,255,255)),(0,610))
        self.dirty = True