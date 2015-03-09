import pygame
import sys
import time
import math
import random
from pygame.locals import *
from my_constants import *

class Shell():

    def __init__(self,  x_coord, y_coord, xVel, yVel, time = 1, dt = 1, gravity = 1, size = 5, explode_x = 0, explode_y = 0):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.xVel = xVel
        self.yVel = yVel 
        self.time = time
        self.gravity = gravity
        self.dt = dt
        self.size = size
        self.explode_x = explode_x
        self.explode_y = explode_y

    def Get_Explode_x(self):
        """ returns x coord of explosion"""
        return self.explode_x

    def Get_Explode_y(self):
        """ returns y coord of explosion """
        return self.explode_y
  
    def Set_Explode_x(self, x_coord):
        """ sets x coord of explosion """
        self.explode_x = x_coord

    def Set_Explode_y(self, y_coord):
        """ sets y coord of explosion """
        self.explode_y = y_coord

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


