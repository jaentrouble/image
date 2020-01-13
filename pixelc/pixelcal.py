import numpy as np
import pygame
import math
from common.constants import *

class PixelCalculator () :
    def __init__(self) :
        self.unit_pixel = UNIT_PIXEL_DEFAULT
        self.unit_actual = UNIT_DEFAULT
        self.first_pin = None
        self.set_ratio()

    def set_unit(self) :
        if self.first_pin == None :
            self.first_pin = pygame.mouse.get_pos()
        else :
            second_pin = pygame.mouse.get_pos()
            x = abs(self.first_pin[0] - second_pin[0])
            y = abs(self.first_pin[1] - second_pin[1])
            self.unit_pixel = math.sqrt(x**2 + y**2)
            self.set_ratio()
            self.first_pin = None
    
    def get_pinned (self) :
        if self.first_pin != None :
            return True
        else :
            return False

    def set_ratio(self) :
        self.ratio = self.unit_actual**2 / self.unit_pixel**2

    def delta_actual(self, delta : int) :
        if self.unit_actual + delta > 0 :
            self.unit_actual += delta
            self.set_ratio()

    def get_unit_pixel (self) :
        return self.unit_pixel

    def get_unit_actual(self) :
        return self.unit_actual

    def get_ratio(self) :
        return self.ratio

    def calculate_area(self, pixel: int) :
        return self.ratio * pixel