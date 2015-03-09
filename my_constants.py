import pygame
from pygame.locals import *


# frames per second
FPS = 30
     
# define colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
     
# assign colors
EXPLODE_COLORS = [RED, ORANGE, YELLOW]
TURRET_COLORS = [RED, BLACK, ORANGE, YELLOW, WHITE]
BGCOLOR = BLUE
GRASS = GREEN
     
# define the window size
WINWIDTH = 640
WINHEIGHT = 480
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
T_X = HALF_WINWIDTH
BORDER = 10
     
# define grass
GR_HEIGHT = 10
GR_WIDTH = WINWIDTH
     
# define power and health
MAX_POWER = int(WINHEIGHT / 5)
MIN_POWER = int(WINHEIGHT / 50)
     
# define turret size based on WINHEIGHT
T_H1 = int(WINHEIGHT / 100 * 2)
T_H2 = int(T_H1 / 2)
T_W1 = int(T_H1 * 2)
T_W2 = int(T_W1 * 2 / 3)
T_LEN = T_W2
T_WID = int(T_LEN / 2)

# define size of shell in pixels
SH1 = 3
SH2 = 3
 
