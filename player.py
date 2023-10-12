from widelyUsedVariables import camera, blockSize, gravity, chunkSize
from worldgen import getChunkCoord, getBlockCoord, findBlock
from controls import keysPressed, keys, mouse

import pygame



class Player():
    def __init__(self):
        self.x = 0
        self.y = chunkSize[1] * blockSize
        self.z = 0

        self.xv = 0 # velocity
        self.yv = 0
        self.zv = 0

        self.acceleration = 0.3
        self.maxHorizontalSpeed = 5
        self.slipperyness = 10
        self.normalJumpForce = 10


        self.width = blockSize - 5
        self.height = blockSize - 5
        self.image = pygame.surface.Surface((self.width, self.width))
        # this is to make rendering work currently and should be removed later!
        self.image.fill((0, 255, 0))
        
        self.imageData = (self.image, (0, 0))

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

        blockBeneath = False
        topLeft = findBlock(self.x, self.y - self.height, self.z)
        topRight = findBlock(self.x + self.width, self.y - self.height, self.z)
        bottomLeft = findBlock(self.x, self.y - self.height, self.z + self.width)
        bottomRight = findBlock(self.x + self.width, self.y - self.height, self.z + self.width)
        if topLeft or topRight or bottomLeft or bottomRight:
            blockBeneath = True
        # need to make it so that all the left right up down things check with the
        # y value of self.y + self.height / 2
        blockAbove = False
        topLeft = findBlock(self.x, self.y, self.z)
        topRight = findBlock(self.x + self.width, self.y, self.z)
        bottomLeft = findBlock(self.x, self.y, self.z + self.width)
        bottomRight = findBlock(self.x + self.width, self.y, self.z + self.width)
        if topLeft or topRight or bottomLeft or bottomRight:
            blockAbove = True

        blockToRight = False
        topRight = findBlock(self.x + self.width + 1, self.y + self.height / 2, self.z)
        bottomRight = findBlock(self.x + self.width + 1, self.y + self.height / 2, self.z + self.width)
        if topRight or bottomRight:
            blockToRight = True
        
        blockToLeft = False
        topLeft = findBlock(self.x - 1, self.y, self.z)
        bottomLeft = findBlock(self.x - 1, self.y, self.z + self.width)
        if topLeft or bottomLeft:
            blockToLeft = True

        blockToUp = False
        topLeft = findBlock(self.x, self.y, self.z - 1)
        topRight = findBlock(self.x + self.width, self.y, self.z - 1)
        if topLeft or topRight:
            blockToUp = True

        blockToDown = False
        bottomLeft = findBlock(self.x, self.y, self.z + self.width + 1)
        bottomRight = findBlock(self.x + self.width, self.y, self.z + self.width + 1)
        if bottomLeft or bottomRight:
            blockToDown = True

        insideABlock = False
        center = findBlock(self.x + self.width / 2, self.y, self.z + self.width / 2)
        if center:
            insideABlock = True




         # x and z axis movement
        if right and not blockToRight:
            if self.xv < self.maxHorizontalSpeed:
                self.xv += self.acceleration

        if left and not blockToLeft:
            if self.xv > -self.maxHorizontalSpeed:
                self.xv -= self.acceleration

        if up and not blockToUp:
            if self.zv > -self.maxHorizontalSpeed:
                self.zv -= self.acceleration

        if down and not blockToDown:
            if self.zv < self.maxHorizontalSpeed:
                self.zv += self.acceleration

         # y axis movement
        if space and blockBeneath:
            self.yv = self.normalJumpForce
            


         # do gravity
        if not blockBeneath:
            self.yv -= gravity
        elif self.yv < 0:
            self.yv = 0
            self.y = self.blockCoord[1] * blockSize
         # don't let player fall out of the world
        if self.y < blockSize:
            self.y = blockSize + 3
            self.yv = 0

         # don't let player go through ceilings
        if blockAbove:
            if self.yv > 0:
                self.yv = 0

         # don't let player go through walls
         # unless it's a non collidable? add later maybe
        if blockToRight:
            self.x -= abs(self.xv)
            self.xv = 0
        if blockToLeft:
            self.x += abs(self.xv)
            self.xv = 0
        if blockToUp:
            self.z += abs(self.zv)
            self.zv = 0
        if blockToDown:
            self.z -= abs(self.zv)
            self.zv = 0

         # do friction
    
        if self.xv > self.maxHorizontalSpeed:
            self.xv = self.maxHorizontalSpeed
        if self.xv < -self.maxHorizontalSpeed:
            self.xv = -self.maxHorizontalSpeed
        if self.zv > self.maxHorizontalSpeed:
            self.zv = self.maxHorizontalSpeed
        if self.zv < -self.maxHorizontalSpeed:
            self.zv = -self.maxHorizontalSpeed

        if (not left and not right) or (left and right):
            if self.xv > -0.1 and self.xv < 0.1:
                self.xv = 0
        if (not up and not down) or (up and down):
            if self.zv > -0.1 and self.zv < 0.1:
                self.zv = 0
        
        self.xv -= self.xv / self.slipperyness
        self.zv -= self.zv / self.slipperyness


         # don't let player get stuck inside of blocks
        if insideABlock:
            self.y += 5


         # do all the position updates that other things use
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