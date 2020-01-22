import tensorflow as tf
import numpy as np
from common.constants import *

class Alphago() :
    """
    All the standard points are left-top corner
    """
    def __init__(self, filename : str) :
        self.model = tf.keras.models.load_model(filename)

    def check_masked (self, pos : list,) :
        """
        check over 1/2 of pixels of AUTO_width1 blocks are True in grid
        """
        m_x = len(self.current_grid)
        m_y = len(self.current_grid[0])
        count = 0
        total = 0
        for x in range(pos[0],min(pos[0] + AUTO_width1, m_x)) :
            for y in range(pos[1], min(pos[1] + AUTO_width1, m_y)) :
                total += 1
                if self.current_grid[x][y] :
                    count += 1
        if count/total > 0.5 :
            return True
        else :
            return False

    def set_total_avg(self) :
        bright = 0
        count = 0
        for x in len(self.current_grid) :
            for y in len(self.current_grid) :
                if self.current_grid[x][y] :
                    bright += self.current_array[x][y]
                    count += 1
        self.current_total_avg = bright/count

    def vector_convert(self, pos) :
        """
        return np.array([width1/width2, width2/width3, width3/total])
        """
        width_bright = np.array([0, 0, 0])
        width_count = np.array([0, 0, 0])
        m_x = len(self.current_grid)
        m_y = len(self.current_grid[0])
        delta_2short = (AUTO_width2-AUTO_width1)//2
        delta_2long = AUTO_width2 - delta_2short
        delta_3short = (AUTO_width3-AUTO_width1)//2
        delta_3long = AUTO_width3 - delta_3short
        
        for x in range(max(0, pos[0]-delta_3short), min(pos[0] + delta_3long, m_x)) :
            for y in range(max(0, pos[1]-delta_3short), min(pos[1] + delta_3long, m_y)) :
                width_bright[2] += self.current_array[x][y]
                width_count[2] += 1
        for x in range(max(0, pos[0]-delta_2short), min(pos[0] + delta_2long, m_x)) :
            for y in range(max(0, pos[1]-delta_2short), min(pos[1] + delta_2long, m_y)) :
                width_bright[1] += self.current_array[x][y]
                width_count[1] += 1
        for x in range(pos[0],min(m_x, pos[0] + AUTO_width1)) :
            for y in range(pos[1], min(m_y, pos[1] + AUTO_width1)):
                width_bright[0] += self.current_array[x][y]
                width_count[0] += 1
        avg = width_bright/width_count
        return np.array([
            avg[0]/avg[1],
            avg[1]/avg[2]
            avg[2]/self.current_total_avg
        ])
        
    def predict(self, grid : np.array, array : np.array) :
        self.current_grid = grid
        self.current_array = array
        self.set_total_avg()
        guess = []
        for i in range(len(grid)//AUTO_width1) :
            x = i*AUTO_width1
            for j in range(len(grid[i])//AUTO_width1):
                y = j*AUTO_width1
                if self.check_masked([x,y]) and self.model.predict(self.vector_convert([x,y])):
                    guess.append([x,y])
