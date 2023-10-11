from widelyUsedVariables import camera, blockSize, gravity
from controls import keysPressed, keys, mouse
from worldgen import getChunkCoord, getBlockCoord, findBlock
import pygame



class Player():
    def __init__(self):
        self.x = 0
        self.y = 10 * blockSize
        self.z = 0

        self.xv = 0 # velocity
        self.yv = 0
        self.zv = 0 # implementing velocity may be harder with 3 axis...

        self.moveSpeed = 5
        self.normalJumpForce = 10
        self.width = blockSize - 5
        self.height = blockSize - 5
        self.image = pygame.surface.Surface((self.width, self.height))
        # this is to make rendering work currently and should be removed later!
        self.image.fill((0, 255, 0))
        
        self.imageData = (self.image, (0, 0))
        #self.fixCameraPos = (self.width/2, self.height/2)

        self.position = (self.x, self.y, self.z)
        self.chunkCoord = (0, 0)
        self.blockCoord = (0, 0, 0)

    def generalMovement(self):

        left = keys[0][pygame.K_a]
        right = keys[0][pygame.K_d]
        up = keys[0][pygame.K_w]
        down = keys[0][pygame.K_s]
        space = keys[0][pygame.K_SPACE]
        
        self.chunkCoord = getChunkCoord(self.x, self.z)
        self.blockCoord = getBlockCoord(self.x, self.y, self.z)

        onGround = False
        topLeft = findBlock(self.x, self.y - blockSize, self.z)
        topRight = findBlock(self.x + self.width, self.y - blockSize, self.z)
        bottomLeft = findBlock(self.x, self.y - blockSize, self.z + self.width)
        bottomRight = findBlock(self.x + self.width, self.y - blockSize, self.z + self.width)
        if topLeft or topRight or bottomLeft or bottomRight:
            onGround = True

        blockToRight = False
        topRight = findBlock(self.x + blockSize, self.y, self.z)
        bottomRight = findBlock(self.x + blockSize, self.y, self.z + self.width)
        if topRight or bottomRight:
            blockToRight = True
        
        blockToLeft = findBlock(self.x - 3, self.y, self.z)
        blockToUp = findBlock(self.x, self.y, self.z - 3)
        blockToDown = findBlock(self.x, self.y, self.z + blockSize)




         # x and z axis movement
        if right and not blockToRight:
            self.x += self.moveSpeed
        if left and not blockToLeft:
            self.x -= self.moveSpeed
        if up and not blockToUp:
            self.z -= self.moveSpeed
        if down and not blockToDown:
            self.z += self.moveSpeed

         # y axis movement
         # replace self.blockcoord[1] with whether player is touching ground, but later
        if space and onGround:
            self.yv = self.normalJumpForce
            


         # do gravity, will need some variables to control whether it is used or not
         # and also other things like lower gravity, fun stuff like that
        if not onGround: # player isn't touching the ground
            self.yv -= gravity
        elif self.yv < 0:
            self.yv = 0

        if self.y < 0:
            self.y = 0
            self.yv = 0

        self.x += self.xv
        self.y += self.yv
        self.z += self.zv

        self.position = (self.x, self.y, self.z)


    def updateCamera(self):
        camera.x -= round((camera.x - self.x + camera.centerTheCamera[0]) / camera.smoothness)
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