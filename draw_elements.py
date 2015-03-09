import pygame
import sys
import time
import math
import random
from pygame.locals import *
from my_constants import *

class DrawPlayer():
    def __init__(self, displaysurf, bigfont, littlefont, turret):
        self.displaysurf = displaysurf
        self.bigfont = bigfont
        self.littlefont = littlefont
        self.turret = turret
   
    def draw(self):
    """ Draws Player Turn, Player Health, and Cannon Power Messages """     
        playerturn = self.bigfont.render('Player ' + str(self.turret.GetPlayerNum()), True, YELLOW)
        playerhealth = self.littlefont.render('Health ' + str(self.turret.Gethealth()), True, GREEN)
        playerpower = self.littlefont.render('Shell Power ' + str(self.turret.Getpower()), True, RED)
   
        playerturnRect = playerturn.get_rect()
        playerturnRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT / 2)
        playerhealthRect = playerhealth.get_rect()
        playerhealthRect.center = (int(WINWIDTH / 5), HALF_WINHEIGHT - HALF_WINHEIGHT / 10)
        playerpowerRect = playerpower.get_rect()
        playerpowerRect.center = (int(WINWIDTH - WINWIDTH / 5), HALF_WINHEIGHT- HALF_WINHEIGHT / 10)
   
        self.displaysurf.blit(playerturn, playerturnRect)
        self.displaysurf.blit(playerhealth, playerhealthRect)
        self.displaysurf.blit(playerpower, playerpowerRect)
   
class DrawShellExplode():
    """ Draws Shell Explosion """
    def __init__(self, displaysurf, shell):
        self.displaysurf = displaysurf
        self.shell = shell

    def shell_explode(self):
        exp_clr = EXPLODE_COLORS[0]
        EXPLODE_COLORS.append(EXPLODE_COLORS.pop(0))
        pygame.draw.circle(self.displaysurf, exp_clr, (self.shell.Get_Explode_x(), self.shell.Get_Explode_y()), self.shell.Get_size(), 0)
        pygame.time.wait(100)
        self.shell.Incr_size(3)

class DrawDeathMode():
    """ Draws Death Explosion and Prints Message of Which Player Died """
    def __init__(self, displaysurf, bigfont, players, death, x_coord, y_coord):
        self.displaysurf = displaysurf
        self.bigfont = bigfont
        self.players = players
        self.death = death
        self.xcoord = x_coord
        self.ycoord = y_coord

    def death_mode(self):
        explode_size = 3
        while explode_size < 30:
            exp_clr = EXPLODE_COLORS[0]
            EXPLODE_COLORS.append(EXPLODE_COLORS.pop(0))
            pygame.draw.circle(self.displaysurf, exp_clr, (self.xcoord, self.ycoord), explode_size)
            pygame.display.update()
            pygame.time.wait(100)
            explode_size += 3
        playerdeath = self.bigfont.render('Player ' + str(self.players[self.death[0]].GetPlayerNum()) + ' Destroyed!', True, RED)
        playerdeathRect = playerdeath.get_rect()
        playerdeathRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT / 2)
        self.displaysurf.blit(playerdeath, playerdeathRect)
        pygame.display.update()
        pygame.time.wait(3000)

class DrawWinMode():
    """ Draws Message for Winning Player """
    def __init__(self, displaysurf, bigfont, players):
        self.displaysurf = displaysurf
        self.bigfont = bigfont
        self.players = players

    def win_mode(self):
        playerwin = self.bigfont.render('Player ' + str(self.players[0].GetPlayerNum()) + ' Wins!', True, WHITE)
        playerwinRect = playerwin.get_rect()
        playerwinRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT / 2)
        self.displaysurf.blit(playerwin, playerwinRect)
        pygame.display.update()
        pygame.time.wait(5000)







