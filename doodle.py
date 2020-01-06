import os
import pygame

image = pygame.image.load(os.path.join('img','sample.tif'))
pygame.init()
screen = pygame.display.set_mode((1280,1024))
loop = True
while loop :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            loop = False
    screen.blit(image, (0,0))
    pygame.display.flip()