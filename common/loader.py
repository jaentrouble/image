import pygame
import os
from common.constants import *

def l_loader(path : str) :
    """
    l_loader 
    returns a list of surfaces
    path : path to the image folder
    """
    surfs = []
    f = []
    imgnames = []
    for (dirpath, dirnames, filenames) in os.walk(path) :
        f.extend(filenames)
    for filename in f :
        try :
            surfs.append(pygame.image.load(os.path.join(path,filename)))
        except pygame.error :
            if pygame.get_error() == 'Unsupported image format' :
                print('Unsupported image : {}'.format(filename))
            else :
                raise pygame.error(pygame.get_error())
        else :
            imgnames.append(filename)

    return surfs, imgnames
