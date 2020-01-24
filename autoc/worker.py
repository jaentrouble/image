import numpy as np
import pygame
from common.constants import *
from common import backimg
from autoc import marker
from autoc import tools

def groupsetter(*groups) :
    Worker.groups = groups
    Line.groups = groups
    Bucket.groups = groups 

class Worker(pygame.sprite.DirtySprite) :
    #cursor image
    image = pygame.Surface((AUTO_width2, AUTO_width2))
    image.fill(AUTO_user_color)
    image.set_colorkey(TRANS_COLOR)
    temp = pygame.Surface((AUTO_width2-2, AUTO_width2-2))
    temp.fill(TRANS_COLOR)
    image.blit(temp,(1,1))

    cursor = pygame.Surface((3,3))
    cursor.fill(AUTO_user_color)

    def __init__(self, target : backimg.BackImage) :
        super().__init__(self.groups)
        self.image = Worker.cursor
        self.image.convert()
        self.rect = Worker.image.get_rect()
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()
        self.target = target
        self.line_thickness = 3
        self.masks = []
        self.masks_colored = []
        self.l_pos_record = []
        self.l_s_pos = None #line start position
        self.set_image()   
        self.markers = marker.Markers()
        self.big_mode = AUTO_BIG_MODE_color #alphago mode vs human mode
        self.mode = AUTO_MODE_none
        self.dirty = False
        self.convert_funcs = [
            tools.convert_red,
            tools.convert_green,
            tools.convert_blue,
            tools.convert_weighted,
            tools.convert_min,
            tools.convert_min_yellow,
        ]
        self.convert_mode = AUTO_convert_weighted
        self.backimg_rect = self.target.get_rect()

    def mode_convert(self, func : int) :
        if func < len(self.convert_funcs):
            self.convert_mode = func

    def get_convert_mode(self) :
        return self.convert_mode

    def reset_all(self) :
        self.markers.reset()
        self.reset_masks()

    def flush_record(self) :
        tmp = self.markers.count()
        converted = self.convert_funcs[self.convert_mode](self.reference)
        self.markers.fit(self.grid, converted)
        self.reset_all()
        return [[tmp, self.target_idx]]

    def get_big_mode(self) :
        return self.big_mode

    def get_mode(self) :
        return self.mode

    def big_mode_change(self) :
        if self.big_mode == AUTO_BIG_MODE_color :
            self.big_mode = AUTO_BIG_MODE_count
        else :
            self.big_mode = AUTO_BIG_MODE_color
        self.mode = AUTO_MODE_none
        self.cursor_off()

    def mode_wrong(self) :
        if self.big_mode == AUTO_BIG_MODE_count:
            if self.mode == AUTO_MODE_wrong :
                self.mode = AUTO_MODE_none
            else :
                self.mode = AUTO_MODE_wrong
            self.cursor_off()

    def mode_user(self) :
        if self.big_mode == AUTO_BIG_MODE_count :
            if self.mode == AUTO_MODE_user :
                self.mode = AUTO_MODE_none
            else :
                self.mode = AUTO_MODE_user
                # self.cursor_on()
                
    def mode_line(self) :
        if self.big_mode == AUTO_BIG_MODE_color :
            if self.mode == AUTO_MODE_line :
                self.mode = AUTO_MODE_none
            else :
                self.mode = AUTO_MODE_line
            self.cursor_off()

    def mode_bucket(self) :
        if self.big_mode == AUTO_BIG_MODE_color :
            if self.mode == AUTO_MODE_bucket :
                self.mode = AUTO_MODE_none
            else :
                self.mode = AUTO_MODE_bucket
            self.cursor_off()

    def calculate(self) :
        if self.big_mode == AUTO_BIG_MODE_count:
            converted = self.convert_funcs[self.convert_mode](self.reference)
            self.markers.calculate(self.grid, converted)
            self.hide_masks()

    def cursor_on (self) :
        self.image = Worker.image
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def cursor_off(self) :
        self.image = Worker.cursor
        self.image.convert()
        self.rect = self.image.get_rect()

    def mouse_clicked(self) :
        if self.backimg_rect.collidepoint(pygame.mouse.get_pos()):
            if self.mode == AUTO_MODE_wrong :
                self.markers.wrong_choice()
            elif self.mode == AUTO_MODE_user :
                self.markers.user_choice()
            elif self.mode == AUTO_MODE_line :
                self.order_line()
            elif self.mode == AUTO_MODE_bucket :
                self.bucket_fill()

    def set_image (self) :
        self.reference = self.target.get_current_array()
        self.reference = self.reference.astype(float)
        self.target_idx = self.target.get_index()
        self.width = self.reference.shape[0]
        self.height = self.reference.shape[1]
        self.reset_masks()
        
    def reset_grid(self) :
        self.grid = np.zeros((self.width, self.height))

    def update_grid (self) :
        for mask in self.masks_colored :
            for pos in mask :
                self.grid[pos[0]][pos[1]] = True

    def hide_masks(self) :
        for mask in self.masks :
            mask.hide()

    def show_masks(self) :
        for mask in self.masks :
            mask.show()

    def hide_alphago_marks(self) :
        self.markers.hide_alphago_marks()
        
    def show_alphago_marks(self) :
        self.markers.show_alphago_marks()

    def reset_masks (self) :
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
        if self.big_mode == AUTO_BIG_MODE_color :
            if len(self.masks) != 0 :
                self.masks_colored.pop()
                dead = self.masks.pop()
                dead.kill()
                self.reset_grid()
                self.update_grid()
            if len(self.l_pos_record) != 0 :
                self.l_s_pos = self.l_pos_record.pop()
        elif self.mode == AUTO_MODE_wrong :
            self.markers.undo_wrong()
        elif self.mode == AUTO_MODE_user :
            self.markers.undo_user()

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

    def update(self) :
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()
        self.dirty = True

class Line(pygame.sprite.DirtySprite) :
    trans = pygame.Surface((2,2))
    trans.fill(TRANS_COLOR)
    trans.set_colorkey(TRANS_COLOR)
    def __init__(self, startpos, endpos, thick) :
        super().__init__(self.groups)
        self.left = min(startpos[0],endpos[0])
        self.top = min(startpos[1],endpos[1])
        self.width = abs(startpos[0]-endpos[0])+2
        self.height = abs(startpos[1]-endpos[1])+2
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.image_saved = self.image
        self.rect_saved = self.rect
        self.image.fill(TRANS_COLOR)
        self.image.set_colorkey(TRANS_COLOR)
        if (startpos[0]-endpos[0])*(startpos[1]-endpos[1]) >= 0 :
            # left-top to right-bottom
            pygame.draw.line(self.image, DRAW_COLOR, [0, 0], [self.width, self.height], thick)
        else :
            pygame.draw.line(self.image, DRAW_COLOR, [0, self.height],[self.width, 0], thick)
        self.image.convert_alpha()

    def hide(self) :
        self.image = Line.trans
        self.image.convert_alpha()
        self.dirty = True

    def show(self) :
        self.image = self.image_saved
        self.rect = self.rect_saved
        self.dirty = True

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
    trans = pygame.Surface((2,2))
    trans.fill(TRANS_COLOR)
    trans.set_colorkey(TRANS_COLOR)

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
        self.image_saved = self.image
        self.rect_saved = self.rect

    def hide(self) :
        self.image = Bucket.trans
        self.image.convert_alpha()
        self.dirty = True

    def show(self) :
        self.image = self.image_saved
        self.rect = self.rect_saved
        self.dirty = True

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
