import pygame
import sys
import time
import math
import random
from pygame.locals import * 

pygame.init()
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

# set fonts and game caption
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
LITTLEFONT = pygame.font.Font('freesansbold.ttf', 16)
pygame.display.set_caption('Maginot Madness')

# define grass
GR_HEIGHT = 10
GR_WIDTH = WINWIDTH

# define power and health
MAX_POWER = int(WINHEIGHT / 5)
MIN_POWER = int(WINHEIGHT / 50)
MAXHEALTH = 100

# define turret size based on WINHEIGHT
T_H1 = int(WINHEIGHT / 100 * 2)
T_H2 = int(T_H1 / 2)
T_W1 = int(T_H1 * 2)
T_W2 = int(T_W1 * 2 / 3)
T_LEN = T_W2
T_WID = int(T_LEN / 2)
SH1 = 3 
SH2 = 3

# number of players - must be less than 5 at the moment
NUMPLAYERS = 2

class Turret():
 
    def __init__(self, number, health, barrel, x_coord, y_coord, power, turret_color):
        self.number = number
        self.health = health
        self.barrel = barrel
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.power = power
        self.barrel_endx = 0
        self.barrel_endy = 0
        self.color = turret_color

    def GetPlayerNum(self):
        return self.number

    def Hit(self, damage):
        """ 
        Lower health of turret due to shell hit

        input-
           amount of damage
        """
        self.health -= damage

    def Incrbarrel(self, increment):
        """ Increment barrel angle by increment """
        self.barrel += increment

    def Incrpower(self, increment):
        """ Increment shell power by increment """
        self.power += increment

    def Getpower(self):
        """ Return shell power """
        return self.power

    def Getbarrel(self):
        """ Return barrel angle """
        return self.barrel

    def Getxcoord(self):
        """ Return x-coordinate of turret """
        return self.x_coord

    def Gethealth(self):
        """ Return health of turret """
        return self.health

    def DrawTurret(self):
        """ Draw the turret on screen at x-coord """
        pygame.draw.rect(DISPLAYSURF, self.color, (int(self.x_coord - T_W1 / 2), WINHEIGHT - T_H1 - GR_HEIGHT, T_W1, T_H1), 0)
        pygame.draw.rect(DISPLAYSURF, self.color, (int(self.x_coord - T_W2 / 2), WINHEIGHT - (T_H2 + T_H1) - GR_HEIGHT, T_W2, T_H2), 0)
        self.barrel_endx = self.x_coord - int(T_LEN*(math.cos(self.barrel)))
        self.barrel_endy = WINHEIGHT - T_H1 - int(T_LEN*(math.sin(self.barrel))) - GR_HEIGHT
        pygame.draw.line(DISPLAYSURF, self.color, (self.x_coord, WINHEIGHT - T_H1 - GR_HEIGHT), (self.barrel_endx, self.barrel_endy), T_WID)

    def Getbarrelendx(self):
        """ Returns x-coordinate of end of turret barrel """
        return self.barrel_endx

    def Getbarrelendy(self):
        """ Returns y-coordinate of end of turret barrel """
        return self.barrel_endy

class Shell():

    def __init__(self, x_coord, y_coord, xVel, yVel, time, dt, gravity, size):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.xVel = xVel
        self.yVel = yVel 
        self.time = time
        self.gravity = gravity
        self.dt = dt
        self.size = size

    def Get_size(self):
        """ Returns radius of explosion in pixels """
        return self.size

    def Incr_size(self, ds):
        """ Increases radius of explosion by ds in pixels """
        self.size += ds

    def Getx_coord(self):
        """ Returns x-coordinate of shell """
        return self.x_coord

    def Gety_coord(self):
        """ Returns y-coordinate of shell """
        return self.y_coord

    def Updatetime(self):
        """ Updates flight time of shell by dt """
        self.time += self.dt

    def Incr_xy_coord(self):
        """ Increments x and y coordinates of shell """
        self.x_coord += int(self.xVel*self.dt)
        down_force = self.gravity*self.time*self.dt
        self.y_coord += int(-self.yVel*self.dt + self.gravity*self.time*self.dt)

    def Check_x_y_position(self):
        """
            Checks to make sure that shell is within DISPLAYSURF
              if shell is outside, it reverses that component of the velocity
        """
        if self.y_coord < BORDER:
            self.yVel = -self.yVel
            self.y_coord = BORDER
        elif self.x_coord < BORDER or self.x_coord > WINWIDTH - BORDER:
            self.xVel = -self.xVel

def main():
    global FPSCLOCK, DISPLAYSURF, NUMPLAYERS

#    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    while True:
        runGame()

def runGame():

    # display the background   
    DISPLAYSURF.fill(BGCOLOR)
    pygame.draw.rect(DISPLAYSURF, GRASS, (0, WINHEIGHT - GR_HEIGHT , GR_WIDTH, GR_HEIGHT))

    # define distance between tanks and x-coordinates of tanks
    dist_st = int(WINWIDTH / 10)
    dist_end = int(WINWIDTH - dist_st)
    dx = int((dist_end - dist_st) / (NUMPLAYERS - 1))
    x_dist = []
    x_dist.append(dist_st)
    if NUMPLAYERS == 2:
        x_dist.append(dist_end)
    elif NUMPLAYERS > 2:
        for i in range(NUMPLAYERS-2):
            x_dist.append(dist_st + (i+1)*dx)
        x_dist.append(dist_end)

    # create a turret

    players = []
    turn = []

    for i in range(NUMPLAYERS):
        n = Turret(i+1, MAXHEALTH, math.pi / 2.0, x_dist[i], GR_HEIGHT, MIN_POWER*2, TURRET_COLORS[i])
        players.append(n)         
        turn.append(i)

    # initialize the keyboard variables
    powerUp = False
    powerDown = False
    moveLeft = False
    moveRight = False
    shell = False
    fire = False
    explode = False
    deathmode = False
    winnermode = False

    # set player one 
    t1 = players[0]
  
    # initialize death list
    death = []

    #start game
    while True:

        # display the background   
        DISPLAYSURF.fill(BGCOLOR)
        pygame.draw.rect(DISPLAYSURF, GRASS, (0, WINHEIGHT - GR_HEIGHT , GR_WIDTH, GR_HEIGHT))

        # draw the turret
        for i in range(len(players)):
            players[i].DrawTurret()

        # draw the shell if needed
        if shell:
            pygame.draw.rect(DISPLAYSURF, BLACK, (sh1.Getx_coord(), sh1.Gety_coord(), SH1, SH2), 0)
            pygame.time.wait(100)
        elif explode:
            if sh1.Get_size() < 30:
                exp_clr = EXPLODE_COLORS[0]
                EXPLODE_COLORS.append(EXPLODE_COLORS.pop(0))
                pygame.draw.circle(DISPLAYSURF, exp_clr, (explode_x, explode_y), sh1.Get_size(), 0)
                pygame.time.wait(100)
                sh1.Incr_size(3) 
            elif not deathmode:
               for i in range(len(players)):
                   if abs(explode_x - players[i].Getxcoord()) < 25:
                       players[i].Hit(100)

#### need player death mode ####
#### and a way to delete dead players ####
                       if players[i].Gethealth() <= 0:
                          deathmode = True
                          death.append(i)
               if not deathmode:   # no turrets died- update player turn
                   explode = False
                   fire = False
                   players.append(players.pop(0))
                   t1 = players[0]

            elif deathmode:  
                if len(death) > 0:               
                    playerdeath = BIGFONT.render('Player ' + str(players[death[0]].GetPlayerNum()) + ' Destroyed!', True, RED)
                    playerdeathRect = playerdeath.get_rect()
                    playerdeathRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT / 2)
                    DISPLAYSURF.blit(playerdeath, playerdeathRect)
                    pygame.display.update()
                    pygame.time.wait(5000)
                    del players[death[0]]
                    del death[0]
                else: 
                    explode = False
                    fire = False 
                    deathmode = False   
                    players.append(players.pop(0))
                    t1 = players[0]
                    if len(players) == 1:
                        winnermode = True 

        # draw player number's turn health and power on screen
        elif not winnermode:
            playerturn = BIGFONT.render('Player ' + str(t1.GetPlayerNum()), True, YELLOW)
            playerhealth = LITTLEFONT.render('Health ' + str(t1.Gethealth()), True, GREEN)
            playerpower = LITTLEFONT.render('Shell Power ' + str(t1.Getpower()), True, RED)
     
            playerturnRect = playerturn.get_rect()
            playerturnRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT / 2)
            playerhealthRect = playerhealth.get_rect()
            playerhealthRect.center = (int(WINWIDTH / 5), HALF_WINHEIGHT - HALF_WINHEIGHT / 10)
            playerpowerRect = playerpower.get_rect()
            playerpowerRect.center = (int(WINWIDTH - WINWIDTH / 5), HALF_WINHEIGHT- HALF_WINHEIGHT / 10)

            DISPLAYSURF.blit(playerturn, playerturnRect)
            DISPLAYSURF.blit(playerhealth, playerhealthRect)
            DISPLAYSURF.blit(playerpower, playerpowerRect)

        else:
            playerwin = BIGFONT.render('Player ' + str(t1.GetPlayerNum()) + ' Wins!', True, WHITE)
            playerwinRect = playerwin.get_rect()
            playerwinRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT / 2)
            DISPLAYSURF.blit(playerwin, playerwinRect)

        # keyboard events
        if not fire:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
     
                elif event.type == KEYDOWN:
                    if event.key in (K_UP, K_w):
                         powerUp = True
                         powerDown = False 
                    elif event.key in (K_DOWN, K_s):
                         powerUp = False
                         powerDown = True
                    elif event.key in (K_LEFT, K_a):
                         moveLeft = True
                         moveRight = False
                    elif event.key in (K_RIGHT, K_d):
                         moveLeft = False
                         moveRight = True
                    elif event.key == K_SPACE:
                         fire = True

                elif event.type == KEYUP:
                    if event.key in (K_LEFT, K_a):
                         moveLeft = False
                    elif event.key in (K_RIGHT, K_d):
                         moveRight = False
                    elif event.key in (K_UP, K_w):
                         powerUp = False
                    elif event.key in (K_DOWN, K_s):
                         powerDown = False
                    elif event.key == K_SPACE:
                         fire = False

            if moveRight:
                if t1.Getbarrel() < 3.14:
                    t1.Incrbarrel(0.1) 
                
            if moveLeft:
                if t1.Getbarrel() > 0:
                    t1.Incrbarrel(-0.1)

            if powerUp:
                if t1.Getpower() < MAX_POWER:
                    t1.Incrpower(1)
            if powerDown:
                if t1.Getpower() > MIN_POWER:
                    t1.Incrpower(-1)

        elif not explode:    # firing shell
            if not shell:
                shell = True
                x_angle = math.cos(t1.Getbarrel())
                y_angle = math.sin(t1.Getbarrel())
                xVel = -t1.Getpower()*x_angle / 3.0 
                yVel = t1.Getpower()*y_angle  / 3.0
                grav = 1
                time = 1
                dt = 1 
                size = 5
                sh1 = Shell(t1.Getbarrelendx(), t1.Getbarrelendy(), xVel, yVel, time, dt, grav, size)
            else:
                sh1.Updatetime()
                sh1.Incr_xy_coord()
                sh1.Check_x_y_position()

                if sh1.Gety_coord() > (WINHEIGHT - GR_HEIGHT):
                    shell = False
                    explode = True
                    explode_x = sh1.Getx_coord()
                    explode_y = WINHEIGHT - GR_HEIGHT

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()


