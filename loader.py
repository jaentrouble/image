import pygame
import os

def l_loader(path : str) :
    """
    l_loader 
    returns a list of surfaces
    path : path to the image folder
    """
    surfs = []
    f = []
    for (dirpath, dirnames, filenames) in os.walk(path) :
        f.extend(filenames)
    for filename in f :
        surfs.append(pygame.image.load(os.path.join(path,filename)))

    return surfs