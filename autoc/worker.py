import numpy as np
import pygame
from common.constants import *
from common import backimg
from autoc import marker

def groupsetter(*groups) :
    Worker.groups = groups
    Line.groups = groups
    Bucket.groups = groups 

class Worker() :
    def __init__(self, target : backimg.BackImage) :
        self.target = target
        self.line_thickness = 3
        self.masks = []
        self.masks_colored = []
        self.l_pos_record = []
        self.l_s_pos = None #line start position
        self.set_image()   
        self.markers = marker.Markers()
        self.big_mode = AUTO_BIG_MODE_color
        self.mode = AUTO_MODE_none

    def big_mode_change(self) :
        if self.big_mode == AUTO_BIG_MODE_color :
            self.big_mode = AUTO_BIG_MODE_count
        else :
            self.big_mode = AUTO_BIG_MODE_color

    def mode_wrong(self) :
        if self.big_mode == AUTO_BIG_MODE_count:
            if self.mode == AUTO_MODE_wrong :
                self.mode = AUTO_MODE_none
            else :
                self.mode = AUTO_MODE_wrong

    def mouse_clicked(self) :
        if self.mode == AUTO_MODE_wrong :
            self.markers.wrong_choice()

    def set_image (self) :
        self.reference = self.target.get_current_array()
        self.target_idx = self.target.get_index()
        self.width = self.reference.shape[0]
        self.height = self.reference.shape[1]
        self.reset_grid()
        
    def reset_grid(self) :
        self.grid = np.zeros((self.width, self.height))

    def update_grid (self) :
        for mask in self.masks_colored :
            for pos in mask :
                self.grid[pos[0]][pos[1]] = True

    def clear_all (self) :
        for mask in self.masks :
            mask.kill()
        self.masks = []
        self.masks_colored = []
        self.l_s_pos = None
        self.l_pos_record = []
        self.reset_grid()

    def get_index(self) :
        return self.target_idx

    def undo (self) :
        if len(self.masks) != 0 :
            self.masks_colored.pop()
            dead = self.masks.pop()
            dead.kill()
            self.reset_grid()
            self.update_grid()
        if len(self.l_pos_record) != 0 :
            self.l_s_pos = self.l_pos_record.pop()

    def order_line (self) :
        if self.l_s_pos == None :
            self.line_start()
        else :
            self.line_continue()    

    def line_start(self) :
        self.l_s_pos = pygame.mouse.get_pos()

    def line_continue(self) :
        self.l_e_pos = pygame.mouse.get_pos()
        tmp = Line(self.l_s_pos, self.l_e_pos, self.line_thickness)
        self.masks.append(tmp)
        self.masks_colored.append(tmp.get_color_arr())
        self.update_grid()
        self.l_pos_record.append(self.l_s_pos)
        self.l_s_pos = self.l_e_pos

    def end_line(self) :
        self.l_s_pos = None

    def bucket_fill(self) :
        tmp = Bucket(self.grid)
        self.masks_colored.append(tmp.get_color_arr())
        self.masks.append(tmp)



class Line(pygame.sprite.DirtySprite) :
    def __init__(self, startpos, endpos, thick) :
        super().__init__(self.groups)
        self.left = min(startpos[0],endpos[0])
        self.top = min(startpos[1],endpos[1])
        self.width = abs(startpos[0]-endpos[0])+2
        self.height = abs(startpos[1]-endpos[1])+2
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.image.fill(TRANS_COLOR)
        self.image.set_colorkey(TRANS_COLOR)
        if (startpos[0]-endpos[0])*(startpos[1]-endpos[1]) >= 0 :
            # left-top to right-bottom
            pygame.draw.line(self.image, DRAW_COLOR, [0, 0], [self.width, self.height], thick)
        else :
            pygame.draw.line(self.image, DRAW_COLOR, [0, self.height],[self.width, 0], thick)
        self.image.convert_alpha()

    def get_color_arr(self) :
        """
        return : [pos of filled cells(absolute)]
        """
        filled = []
        array = pygame.surfarray.array3d(self.image)
        x = self.left
        for column in array :
            y = self.top
            for color in column :
                if not np.all(color == TRANS_COLOR):
                    filled.append([x,y])
                y += 1
            x += 1
        return filled

class Bucket(pygame.sprite.DirtySprite) :
    def __init__(self, grid : np.array) :
        super().__init__(self.groups)
        self.grid = grid
        self.startpos = pygame.mouse.get_pos()
        self.image = pygame.Surface(self.grid.shape)
        self.image.fill(TRANS_COLOR)
        self.rect = self.image.get_rect()
        self.img_array = pygame.surfarray.array3d(self.image)
        self.col_list = []
        self.filler(pygame.mouse.get_pos())
        self.update_image()

    def update_image(self):
        self.image = pygame.surfarray.make_surface(self.img_array)
        self.image.set_colorkey(TRANS_COLOR)
        self.image.convert_alpha()
        self.dirty = 1

    def get_color_arr(self) :
        return self.col_list.copy()

    def filler(self, start : list) :
        """
        puts all filled list (except the starting point) to 'filled_list'
        """
        x, y = start
        queue = []
        if self.grid[x][y] :
            return
        else :
            self.grid[x][y] = True
            self.col_list.append([x,y])
            self.img_array[x][y] = np.array(DRAW_COLOR)
            queue.append([x,y])
            while len(queue) > 0 :
                x,y = queue.pop(0)
                if x < self.grid.shape[0] - 1 :
                    if not self.grid[x+1][y] :
                        self.grid[x+1][y] = True
                        self.col_list.append([x+1,y])
                        self.img_array[x+1][y] = np.array(DRAW_COLOR)
                        queue.append([x+1,y])
                if x > 0 :
                    if not self.grid[x-1][y] :
                        self.grid[x-1][y] = True
                        self.col_list.append([x-1,y])
                        self.img_array[x-1][y] = np.array(DRAW_COLOR)
                        queue.append([x-1,y])
                if y < self.grid.shape[1] -1 :
                    if not self.grid[x][y+1] :
                        self.grid[x][y+1] = True
                        self.col_list.append([x,y+1])
                        self.img_array[x][y+1] = np.array(DRAW_COLOR)
                        queue.append([x,y+1])
                if y > 0 :
                    if not self.grid[x][y-1] :
                        self.grid[x][y-1] = True
                        self.col_list.append([x,y-1])
                        self.img_array[x][y-1] = np.array(DRAW_COLOR)
                        queue.append([x,y-1])
