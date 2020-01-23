RED = 0
GREEN = 1
BLUE = 2
WHITE = 3
BLACK = 4
CYAN = 5
YELLOW = 6
MAGENTA = 7

DEFAULT = -1
PATH = 'img'
TEXT_WIDTH = 400
D_HEIGHT = 800  #Default height

COLOR_LIST = [
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,255),
    (0,0,0),
    (0,255,255),
    (255,255,0),
    (255,0,255),
]
DRAW_COLOR = (0,0,255)
TRANS_COLOR = (0,0,0)

MODE_NONE = 0
MODE_LINE = 1
MODE_BUCKET = 2
MODE_UNIT = 3
MODE_COUNT = 4

UNIT_PIXEL_DEFAULT = 100
UNIT_DEFAULT = 50

AUTO_width1 = 4
AUTO_width2 = 12
AUTO_width3 = 24
AUTO_alphago_color = COLOR_LIST[YELLOW]
AUTO_wrong_color = COLOR_LIST[RED]
AUTO_user_color = COLOR_LIST[MAGENTA]
AUTO_MODE_none = 0
AUTO_MODE_line = 1
AUTO_MODE_bucket = 2
AUTO_MODE_wrong = 3
AUTO_MODE_user = 4
AUTO_BIG_MODE_color = 0
AUTO_BIG_MODE_count = 1
AUTO_PATH = 'model'
AUTO_vector_size = 10
AUTO_default_filename = 'model.h5'
AUTO_database_filename = 'database.xlsx'
AUTO_convert_red = 0
AUTO_convert_green = 1
AUTO_convert_blue = 2
AUTO_convert_weighted = 3
AUTO_convert_min = 4
AUTO_convert_min_yellow = 5
AUTO_alphago_epoch = 3
AUTO_teacher_epoch = 10