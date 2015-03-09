import pygame
import sys
import time
import math
import random
from pygame.locals import * 

# import my external files
from turret import Turret
from my_constants import *
from shell import Shell
from draw_elements import DrawPlayer
from draw_elements import DrawShellExplode
from draw_elements import DrawDeathMode
from draw_elements import DrawWinMode

pygame.init()

# number of players - must be less than 5 at the moment
NUMPLAYERS = 2

# set fonts and game caption
BIGFONT = pygame.font.Font('freesansbold.ttf', 32)
LITTLEFONT = pygame.font.Font('freesansbold.ttf', 16)
pygame.display.set_caption('Maginot Madness')


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
    x_dist = []
    x_dist = player_dist()

    # create a turret

    players = []
    turn = []

    for i in range(NUMPLAYERS):
        n = Turret(DISPLAYSURF, i+1, x_dist[i], GR_HEIGHT, MIN_POWER*2, TURRET_COLORS[i])
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
              DrawShellExplode(DISPLAYSURF, sh1).shell_explode()

            elif not deathmode:
               for i in range(len(players)):
                   dist_sh = abs(sh1.Get_Explode_x() - players[i].Getxcoord())
                   if dist_sh < 30:
                       if dist_sh <= 10.0:
                         damage = 80
                       else:
                         damage = (80 / dist_sh)*5.0 
                       players[i].Hit(damage)

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
                    DrawDeathMode(DISPLAYSURF, BIGFONT, players, death, t1.Getxcoord(), WINHEIGHT - GR_HEIGHT).death_mode()
                    del players[death[0]]
                    del death[0]
                    if len(players) == 1:
                      winnermode = True  
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
            DrawPlayer(DISPLAYSURF, BIGFONT, LITTLEFONT, t1).draw()  
 
        else:
            DrawWinMode(DISPLAYSURF, BIGFONT, players).win_mode()

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
                xVel = -t1.Getpower()*math.cos(t1.Getbarrel()) / 3.0 
                yVel = t1.Getpower()*math.sin(t1.Getbarrel())  / 3.0
                sh1 = Shell(t1.Getbarrelendx(), t1.Getbarrelendy(), xVel, yVel)
            else:
                sh1.Updatetime()
                sh1.Incr_xy_coord()
                sh1.Check_x_y_position()

                if sh1.Gety_coord() > (WINHEIGHT - GR_HEIGHT):
                    shell = False
                    explode = True
                    sh1.Set_Explode_x(sh1.Getx_coord())
                    sh1.Set_Explode_y(WINHEIGHT - GR_HEIGHT)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

### End rungame ###

def player_dist():
    """ determine starting distance between players """ 
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
    return x_dist


if __name__ == '__main__':
    main()


