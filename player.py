from widelyUsedVariables import camera, blockSize, gravity
from controls import keysPressed, keys, mouse
from worldgen import getChunkCoord, getBlockCoord
import pygame



class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

        self.xv = 0 # velocity
        self.yv = 0
        self.zv = 0 # implementing velocity may be harder with 3 axis...

        self.moveSpeed = 5
        self.normalJumpForce = 20

        self.width = blockSize
        self.height = blockSize
        self.image = pygame.surface.Surface((self.width, self.height))
        # this is to make rendering work currently and should be removed later!
        self.image.fill((0, 255, 0))
        
        self.imageData = (self.image, (0, 0))
        self.fixCameraPos = (self.width/2, self.height/2)

        self.position = (self.x, self.y, self.z)
        self.chunkCoord = (0, 0)
        self.blockCoord = (0, 0, 0)

    def generalMovement(self):

        left = keys[0][pygame.K_a]
        right = keys[0][pygame.K_d]
        up = keys[0][pygame.K_w]
        down = keys[0][pygame.K_s]
        space = keys[0][pygame.K_SPACE]


        self.x += self.xv
        self.y += self.yv
        self.z += self.zv

        self.position = (self.x, self.y, self.z)
        """VERY IMPORTANT
        if the player's position is changed somewhere like to force them out of a wall,
        make sure to change the position attribute or maybe i can put it at the end of
        all the player's movement thingies, just in case
        """
        self.chunkCoord = getChunkCoord(self.x, self.z)
        self.blockCoord = getBlockCoord(self.x, self.y, self.z)
         # add more checks to the movement later
         # x and z axis movement
        if right:
            self.x += self.moveSpeed
        if left:
            self.x -= self.moveSpeed
        if up:
            self.z -= self.moveSpeed
        if down:
            self.z += self.moveSpeed

         # y axis movement
         # replace self.blockcoord[1] with whether player is touching ground, but later
        if space and self.blockCoord[1] <= 5:
            self.yv = self.normalJumpForce
            self.y += 1


         # do gravity, will need some variables to control whether it is used or not
         # and also other things like lower gravity, fun stuff like that
        if self.y > blockSize * 5: # player isn't touching the ground
            self.yv -= gravity
        else:
            # keep player from falling out of the world
            self.yv = 0
            self.y = blockSize * 5

        self.position = (self.x, self.y, self.z)


    def updateCamera(self):
        camera.x -= round((camera.x - self.x + camera.centerTheCamera[0]) / camera.smoothness)
        # idk how smoothing should work for vertical, i'll figure it out later
        camera.y = self.y
        camera.z -= round((camera.z - self.z + camera.centerTheCamera[1]) / camera.smoothness)
        
        camera.currentChunk = getChunkCoord(camera.x, camera.z)

    def updateImageThings(self):
        imageX = self.x - camera.x
        imageY = self.z - camera.z
        
        coordinate = (imageX, imageY)
        self.imageData = (self.image, coordinate)

    def doStuff(self):
        
        self.generalMovement()
        
        self.updateCamera()

        self.updateImageThings()




            

player = Player()