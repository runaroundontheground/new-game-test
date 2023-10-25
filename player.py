from widelyUsedVariables import camera, blockSize, gravity, chunkSize
from worldgen import getChunkCoord, getBlockCoord, findBlock
from controls import keysPressed, keys, mouse
import pygame, math



class Player():
    def __init__(self):
        self.x = 0
        self.y = chunkSize[1] * blockSize
        self.z = 0

        self.xv = 0 # velocity
        self.yv = 0
        self.zv = 0

        self.acceleration = 0.6
        self.maxHorizontalSpeed = 5
        self.slipperyness = 5
        self.normalJumpForce = 10


        self.width = blockSize - 5
        self.height = blockSize - 5
        self.image = pygame.surface.Surface((self.width, self.width))
        # this is to make rendering work currently and should be removed later!
        self.image.fill((255, 0, 0))
        
        self.imageData = (self.image, (0, 0))

        self.position = (self.x, self.y, self.z)
        self.chunkCoord = (0, 0)
        self.blockCoord = (0, 0, 0)

    def generalMovement(self, deltaTime):

        left = keys[0][pygame.K_a]
        right = keys[0][pygame.K_d]
        up = keys[0][pygame.K_w]
        down = keys[0][pygame.K_s]
        space = keys[0][pygame.K_SPACE]
        
        self.chunkCoord = getChunkCoord(self.x, self.z)
        self.blockCoord = getBlockCoord(self.x, self.y, self.z)

         # faster? access to variables that need to be used a lot in collision
        rightSide = self.x + self.width
        bottomSide = self.z + self.width
        underSide = self.y - self.height

        blockBelow = False
        topLeft = findBlock(self.x, underSide, self.z)
        topRight = findBlock(rightSide, underSide, self.z)
        bottomLeft = findBlock(self.x, underSide, bottomSide)
        bottomRight = findBlock(rightSide, underSide, bottomSide)
        if topLeft or topRight or bottomLeft or bottomRight:
            blockBelow = True
        
        blockAbove = False
        topLeft = findBlock(self.x, self.y, self.z)
        topRight = findBlock(rightSide, self.y, self.z)
        bottomLeft = findBlock(self.x, self.y, bottomSide)
        bottomRight = findBlock(rightSide, self.y, bottomSide)
        if topLeft or topRight or bottomLeft or bottomRight:
            blockAbove = True
         # so this mess of if statements may or may not be faster?
         # it'll skip all the other operations if it finds one first
        blockToRight = False
        temporaryNumber = rightSide + 1
        aboveTopRight = findBlock(temporaryNumber, self.y, self.z)
        if not aboveTopRight:
            aboveBottomRight = findBlock(temporaryNumber, self.y, bottomSide)
            if not aboveBottomRight:
                belowBottomRight = findBlock(temporaryNumber, underSide + 3, bottomSide)
                if not belowBottomRight:
                    belowTopRight = findBlock(temporaryNumber, underSide + 3, self.z)
                    if belowTopRight:
                        blockToRight = True
                else:
                    blockToRight = True
            else:
                blockToRight = True
        else:
            blockToRight = True
                    
                
        
        blockToLeft = False
        temporaryNumber = self.x - 1
        aboveTopLeft = findBlock(temporaryNumber, self.y, self.z)
        aboveBottomLeft = findBlock(temporaryNumber, self.y, bottomSide)
        belowBottomLeft = findBlock(temporaryNumber, underSide, bottomSide)
        belowTopLeft = findBlock(temporaryNumber, underSide, self.z)
        if topLeft or bottomLeft:
            blockToLeft = True

        blockToUp = False
        topLeft = findBlock(self.x, self.y, self.z - 1)
        topRight = findBlock(rightSide, self.y, self.z - 1)
        if topLeft or topRight:
            blockToUp = True

        blockToDown = False
        bottomLeft = findBlock(self.x, self.y, bottomSide + 1)
        bottomRight = findBlock(rightSide, self.y, bottomSide + 1)
        if bottomLeft or bottomRight:
            blockToDown = True

        insideABlock = False
        center = findBlock(rightSide / 2, self.y, bottomSide / 2)
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
        if space and blockBelow:
            self.yv = self.normalJumpForce
            


         # do gravity
        if not blockBelow:
            self.yv -= gravity
        elif self.yv < 0:
            self.yv = 0
            self.y = self.blockCoord[1] * blockSize + self.height
         # don't let player fall out of the world
        if self.y < blockSize:
            self.y = chunkSize * blockSize + self.height
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

         
    
        if self.xv > self.maxHorizontalSpeed:
            self.xv = self.maxHorizontalSpeed
        if self.xv < -self.maxHorizontalSpeed:
            self.xv = -self.maxHorizontalSpeed
        if self.zv > self.maxHorizontalSpeed:
            self.zv = self.maxHorizontalSpeed
        if self.zv < -self.maxHorizontalSpeed:
            self.zv = -self.maxHorizontalSpeed
         # friction is handled below
        if (not left and not right) or (left and right):
            self.xv -= self.xv / self.slipperyness
            if self.xv > -0.1 and self.xv < 0.1:
                self.xv = 0
        if (not up and not down) or (up and down):
            self.zv -= self.zv / self.slipperyness
            if self.zv > -0.1 and self.zv < 0.1:
                self.zv = 0
        


         # don't let player get stuck inside of blocks
        if insideABlock:
            self.y += 5

        
         # do all the position updates that other things use
        self.x += self.xv * deltaTime
        self.y += self.yv * deltaTime
        self.z += self.zv * deltaTime
        

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

    def doStuff(self, deltaTime):
        
        self.generalMovement(deltaTime)
        
        self.updateCamera()

        self.updateImageThings()




            

player = Player()