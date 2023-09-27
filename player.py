from controls import keysPressed, keys, mouse
from widelyUsedVariables import camera
from worldgen import getChunkCoord
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

        if keys[0][right]:
                # add more checks later
            self.x += 1
        if keys[0][left]:
            self.x -= 1
        if keys[0][up]:
            self.z -= 1
        if keys[0][down]:
            self.z += 1

    def updateCamera(self):
        camera.x -= round((camera.x - self.x + camera.centerTheCamera[0]) / camera.smoothness)
        camera.z -= round((camera.z - self.z + camera.centerTheCamera[1]) / camera.smoothness)
        camera.currentChunk = getChunkCoord(camera.x, camera.z)



    def doStuff(self):
        self.generalMovement()
        
        self.updateCamera()




            

player = Player()