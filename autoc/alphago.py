import tensorflow as tf
import numpy as np
from common.constants import *
from common import exporter
import math
import os
import random

class Alphago() :
    """
    All the standard points are left-top corner
    Arrays should be 'brigtness' single value ; 2D array not 3D
    """
    def __init__(self, filename : str) :
        self.model_path = os.path.join(AUTO_PATH, filename)
        self.model = tf.keras.models.load_model(self.model_path)
        self.saver = exporter.Saver(AUTO_database_filename)

    def check_masked (self, pos : list,) :
        """
        check over 1/2 of pixels of AUTO_width1 blocks are True in grid
        """
        count = 0
        total = 0
        for x in range(pos[0],min(pos[0] + AUTO_width1, self.m_x)) :
            for y in range(pos[1], min(pos[1] + AUTO_width1, self.m_y)) :
                total += 1
                if self.current_grid[x][y] :
                    count += 1
        if count/total > 0.5 :
            return True
        else :
            return False

    def set_grid_array(self, grid, array) :
        self.current_grid = grid
        self.current_array = array
        self.m_x = len(self.current_grid)
        self.m_y = len(self.current_grid[0])
        self.set_total_avg()

    def set_total_avg(self) :
        bright = 0
        count = 0
        if np.count_nonzero(self.current_grid) == 0 :
            for x in range(len(self.current_grid)) :
                for y in range(len(self.current_grid[0])) :
                    bright += self.current_array[x][y]
                    count += 1
            print('empty mask ; using total brightness instead')
        else :
            for x in range(len(self.current_grid)) :
                for y in range(len(self.current_grid[0])) :
                    if self.current_grid[x][y] :
                        bright += self.current_array[x][y]**2
                        count += 1
        self.current_total_avg = math.sqrt(bright/count)

    def vector_convert_2(self, pos) :
        """
        return np.array([width1/width2, width2/width3, width3/total])
        """
        width_bright = np.array([0, 0, 0])
        width_count = np.array([0, 0, 0])
        delta_2short = (AUTO_width2-AUTO_width1)//2
        delta_2long = AUTO_width2 - delta_2short
        delta_3short = (AUTO_width3-AUTO_width1)//2
        delta_3long = AUTO_width3 - delta_3short
        
        for x in range(max(0, pos[0]-delta_3short), min(pos[0] + delta_3long, self.m_x)) :
            for y in range(max(0, pos[1]-delta_3short), min(pos[1] + delta_3long, self.m_y)) :
                width_bright[2] += self.current_array[x][y]**2
                width_count[2] += 1
        for x in range(max(0, pos[0]-delta_2short), min(pos[0] + delta_2long, self.m_x)) :
            for y in range(max(0, pos[1]-delta_2short), min(pos[1] + delta_2long, self.m_y)) :
                width_bright[1] += self.current_array[x][y]**2
                width_bright[2] -= self.current_array[x][y]**2
                width_count[1] += 1
                width_count[2] -= 1
        for x in range(pos[0],min(self.m_x, pos[0] + AUTO_width1)) :
            for y in range(pos[1], min(self.m_y, pos[1] + AUTO_width1)):
                width_bright[0] += self.current_array[x][y]**2
                width_bright[1] -= self.current_array[x][y]**2
                width_count[0] += 1
                width_count[1] -= 1
        avg = np.sqrt(width_bright/width_count)
        return np.array([
            avg[0]/avg[1],
            avg[0]/avg[2],
            avg[0]/self.current_total_avg,
        ])
        
    def vector_convert(self, pos) :
        """
        divide width2 square into 9 squares
        """
        delta = AUTO_width2//3
        bright_list = []
        for i in range(-1,2):
            for j in range(-1,2) :
                b = 0
                count = 0
                for x in range(max(0, pos[0] + i*delta), min(self.m_x, pos[0] + (i+1)*delta)):
                    for y in range(max(0, pos[1] + j*delta), min(self.m_y, pos[1] + (j+1)*delta)):
                        b += self.current_array[x][y]
                        count += 1
                if count == 0 :
                    bright_list.append(0)
                else :
                    bright_list.append(b/count)
        bright_list = np.array(bright_list)
        m = np.max(bright_list)/self.current_total_avg
        bright_list = bright_list/np.min(bright_list) -1
        bright_list = np.append(bright_list, m)
        return bright_list
        
    def predict(self, grid : np.array, array : np.array) :
        """
        returns 'Center point', not the left-top point
        """
        self.set_grid_array(grid, array)
        guess = []
        candidates = []
        for i in range(len(grid)//AUTO_width1) :
            x = i*AUTO_width1
            for j in range(len(grid[i])//AUTO_width1):
                y = j*AUTO_width1
                if self.check_masked([x,y]):
                    candidates.append([x,y])
        for c in candidates :
            prob = self.model.predict(np.array([self.vector_convert(c)]))[0]
            if np.argmax(prob) == 1 :
                guess.append([min(c[0]+(AUTO_width1//2), self.m_x),min(c[1]+(AUTO_width1//2), self.m_y)])
        return guess

    def fit(self, correct_choice, wrong_choice, grid, array) :
        """
        correct_choice : True data -> please inclue correct alphago choice too
        wrong_choice : False data
        """
        self.set_grid_array(grid, array)
        correct_choice = list(correct_choice)
        wrong_choice = list(wrong_choice)
        if len(correct_choice) > len(wrong_choice) :
            for _ in range(len(correct_choice)-len(wrong_choice)) :
                x = random.randrange(0, self.m_x)
                y = random.randrange(0, self.m_y)
                while [x,y] in correct_choice :
                    x = random.randrange(0, self.m_x)
                    y = random.randrange(0, self.m_y)
                wrong_choice.append([x,y])
        elif len(correct_choice) < len(wrong_choice) :
            wrong_choice = random.sample(wrong_choice, len(correct_choice))
        user_y = np.ones(len(correct_choice))
        wrong_y = np.zeros(len(wrong_choice))
        total_x = np.concatenate((correct_choice,wrong_choice))
        vectorized_x = []
        for tx in total_x :
            vectorized_x.append(self.vector_convert([max(0, tx[0]-(AUTO_width1//2)), max(0, tx[1]-(AUTO_width1//2))]))
        vectorized_x = np.array(vectorized_x)
        total_y = np.concatenate((user_y, wrong_y))
        self.saver.save(np.hstack((vectorized_x, total_y.reshape((-1,1)))))
        self.model.fit(x = vectorized_x, y = total_y, epochs = AUTO_alphago_epoch)
        self.model.save(self.model_path)
        print('model saved')