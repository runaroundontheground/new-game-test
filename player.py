from controls import keysPressed, keys, mouse
import pygame
# just for faster writing:
up = pygame.K_w
left = pygame.K_a
right = pygame.K_d
down = pygame.K_s



class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

        self.xv = 0 # velocity
        self.yv = 0
        self.zv = 0 # implementing velocity may be harder with 3 axis...

    def generalMovement(self):

        self.x += self.xv
        self.y += self.yv
        self.z += self.zv

        if keysPressed[right]:
                # add more checks later
            self.x += 1
        if keysPressed[left]:
            self.x -= 1
        if keysPressed[up]:
            self.z -= 1
        if keysPressed[down]:
            self.z += 1



    def doStuff(self):
        self.generalMovement()

            

player = Player()