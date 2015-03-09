import pygame
import sys
import time
import math
import random
from pygame.locals import *
from my_constants import *

class Turret():
 
    def __init__(self, displaysurf, number, x_coord, y_coord, power, turret_color, health=100, barrel=math.pi/2.0):
        self.number = number
        self.health = health
        self.barrel = barrel
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.power = power
        self.barrel_endx = 0
        self.barrel_endy = 0
        self.color = turret_color
        self.displaysurf = displaysurf

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
        pygame.draw.rect(self.displaysurf, self.color, (int(self.x_coord - T_W1 / 2), WINHEIGHT - T_H1 - GR_HEIGHT, T_W1, T_H1), 0)
        pygame.draw.rect(self.displaysurf, self.color, (int(self.x_coord - T_W2 / 2), WINHEIGHT - (T_H2 + T_H1) - GR_HEIGHT, T_W2, T_H2), 0)
        self.barrel_endx = self.x_coord - int(T_LEN*(math.cos(self.barrel)))
        self.barrel_endy = WINHEIGHT - T_H1 - int(T_LEN*(math.sin(self.barrel))) - GR_HEIGHT
        pygame.draw.line(self.displaysurf, self.color, (self.x_coord, WINHEIGHT - T_H1 - GR_HEIGHT), (self.barrel_endx, self.barrel_endy), T_WID)

    def Getbarrelendx(self):
        """ Returns x-coordinate of end of turret barrel """
        return self.barrel_endx

    def Getbarrelendy(self):
        """ Returns y-coordinate of end of turret barrel """
        return self.barrel_endy

