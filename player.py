from widelyUsedVariables import camera, blockSize, gravity, chunkSize
from worldgen import getChunkCoord, getBlockCoord, findBlock
from controls import keysPressed, keys, mouse
import pygame, math



class Player():
    def __init__(self):
        self.x = 0
        self.y = chunkSize[1] * blockSize
        self.z = 0
         # velocity
        self.xv = 0
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

        self.collision = {
            "blockBelow": False,
            "blockAbove": False,

            "blockToRight": False,
            "blockToLeft": False,
            "blockToUp": False,
            "blockToDown": False,

            "blockAboveToRight": False,
            "blockAboveToLeft": False,
            "blockAboveToUp": False,
            "blockAboveToDown": False,
            
            "insideOfBlock": "air"
        }

    def generalMovement(self, deltaTime):

        left = keys[0][pygame.K_a]
        right = keys[0][pygame.K_d]
        up = keys[0][pygame.K_w]
        down = keys[0][pygame.K_s]
        space = keys[0][pygame.K_SPACE]
        
        self.chunkCoord = getChunkCoord(self.x, self.z)
        self.blockCoord = getBlockCoord(self.x, self.y, self.z)

        def doPlayerCollision():
            
            for dictKey in self.collision.keys():
                self.collision[dictKey] = False

         # faster? access to variables that need to be used a lot in collision
            rightSide = self.x + self.width
            bottomSide = self.z + self.width
            underSide = self.y - self.height

            topLeft = findBlock(self.x, underSide - 3, self.z, ignoreWater = True)
            topRight = findBlock(rightSide, underSide - 3, self.z, ignoreWater = True)
            bottomLeft = findBlock(self.x, underSide - 3, bottomSide, ignoreWater = True)
            bottomRight = findBlock(rightSide, underSide - 3, bottomSide, ignoreWater = True)
            if topLeft or topRight or bottomLeft or bottomRight:
                self.collision["blockBelow"] = True
            
            topLeft = findBlock(self.x, self.y, self.z, ignoreWater = True)
            topRight = findBlock(rightSide, self.y, self.z, ignoreWater = True)
            bottomLeft = findBlock(self.x, self.y, bottomSide, ignoreWater = True)
            bottomRight = findBlock(rightSide, self.y, bottomSide, ignoreWater = True)
            if topLeft or topRight or bottomLeft or bottomRight:
                self.collision["blockAbove"] = True
            

            temporaryNumber = rightSide + 1
            aboveTopRight = findBlock(temporaryNumber, self.y, self.z, ignoreWater = True)
            aboveBottomRight = findBlock(temporaryNumber, self.y, bottomSide, ignoreWater = True)
            belowBottomRight = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = True)
            belowTopRight = findBlock(temporaryNumber, underSide, self.z, ignoreWater = True)
            if aboveTopRight or aboveBottomRight or belowBottomRight or aboveBottomRight:
                self.collision["blockToRight"] = True
                    
            
            temporaryNumber = self.x - 1
            aboveTopLeft = findBlock(temporaryNumber, self.y, self.z, ignoreWater = True)
            aboveBottomLeft = findBlock(temporaryNumber, self.y, bottomSide, ignoreWater = True)
            belowBottomLeft = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = True)
            belowTopLeft = findBlock(temporaryNumber, underSide, self.z, ignoreWater = True)
            if aboveBottomLeft or aboveTopLeft or belowBottomLeft or belowTopLeft:
                self.collision["blockToLeft"] = True

            aboveTopLeft = findBlock(self.x, self.y, self.z - 1, ignoreWater = True)
            aboveTopRight = findBlock(rightSide, self.y, self.z - 1, ignoreWater = True)
            belowTopRight = findBlock(rightSide, underSide, self.z - 1, ignoreWater = True)
            belowTopLeft = findBlock(self.x, underSide, self.z - 1, ignoreWater = True)
            if aboveTopLeft or aboveTopRight or belowTopLeft or belowTopRight:
                self.collision["blockToUp"] = True

            aboveBottomLeft = findBlock(self.x, self.y, bottomSide + 1, ignoreWater = True)
            aboveBottomRight = findBlock(rightSide, self.y, bottomSide + 1, ignoreWater = True)
            belowBottomRight = findBlock(rightSide, underSide, bottomSide + 1, ignoreWater = True)
            belowBottomLeft = findBlock(self.x, underSide, bottomSide + 1, ignoreWater = True)
            if aboveBottomLeft or aboveBottomRight or belowBottomRight or belowBottomLeft:
                self.collision["blockToDown"] = True

            center = findBlock(self.x + self.width/2, self.y - self.height/2, self.z + self.width/2, extraInfo = True)
            self.collision["insideOfBlock"] = center["type"]


            aboveToTopRight = findBlock(rightSide + 3, self.y + 3, self.z, ignoreWater = True)
            aboveToBottomRight = findBlock(rightSide + 3, self.y + 3, bottomSide, ignoreWater = True)
            if aboveToTopRight or aboveToBottomRight:
                self.collision["blockAboveToRight"] = True

            aboveToTopLeft = findBlock(self.x - 3, self.y + 3, self.z, ignoreWater = True)
            aboveToBottomLeft = findBlock(self.x - 3, self.y + 3, bottomSide, ignoreWater = True)
            if aboveToTopLeft or aboveToBottomLeft:
                self.collision["blockAboveToLeft"] = True

            aboveToLeftUp = findBlock(self.x, self.y + 3, self.z - 3, ignoreWater = True)
            aboveToRightUp = findBlock(rightSide, self.y + 3, self.z - 3, ignoreWater = True)
            if aboveToLeftUp or aboveToRightUp:
                self.collision["blockAboveToUp"] = True
            # need to write out that fourth side (bottom/down)



        doPlayerCollision()

        currentMaxHorizontalSpeed = self.maxHorizontalSpeed
        if self.collision["insideOfBlock"] == "water":
            currentMaxHorizontalSpeed = self.maxHorizontalSpeed / 2

         # x and z axis movement
        if right and not self.collision["blockToRight"]:
            if self.xv < currentMaxHorizontalSpeed:
                self.xv += self.acceleration

        if left and not blockToLeft:
            if self.xv > -currentMaxHorizontalSpeed:
                self.xv -= self.acceleration

        if up and not blockToUp:
            if self.zv > -currentMaxHorizontalSpeed:
                self.zv -= self.acceleration

        if down and not blockToDown:
            if self.zv < currentMaxHorizontalSpeed:
                self.zv += self.acceleration

         # y axis movement
        if space:
            if self.collision["insideOfBlock"] == "water":
                # do water stuff
                jumpForce = self.normalJumpForce / 3

                self.yv = jumpForce
            else:
                if blockBelow:
                    # do jump stuff
                    jumpForce = self.normalJumpForce

                    self.yv = jumpForce
            


         # do gravity
        if not blockBelow:
            yvChange = gravity
            if self.collision["insideOfBlock"] == "water":
                yvChange /= 5
            self.yv -= yvChange
        elif self.yv < 0:
            self.yv = 0
            self.y = self.blockCoord[1] * blockSize + self.height
         # don't let player fall out of the world
        if self.y < blockSize:
            self.yv = 100

         # don't let player go through ceilings
        if blockAbove:
            if self.yv > 0:
                self.yv = 0

         # don't let player go through walls
         # unless it's a non collidable? add later maybe
        if self.collision["blockToRight"]:
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

         
        # force player speed cap
        if self.xv > currentMaxHorizontalSpeed:
            self.xv = currentMaxHorizontalSpeed
        if self.xv < -currentMaxHorizontalSpeed:
            self.xv = -currentMaxHorizontalSpeed

        if self.zv > currentMaxHorizontalSpeed:
            self.zv = currentMaxHorizontalSpeed
        if self.zv < -currentMaxHorizontalSpeed:
            self.zv = -currentMaxHorizontalSpeed
        
         # friction is handled below
        if (not left and not right) or (left and right):
            self.xv -= self.xv / self.slipperyness
            if self.xv > -0.01 and self.xv < 0.01:
                self.xv = 0
        if (not up and not down) or (up and down):
            self.zv -= self.zv / self.slipperyness
            if self.zv > -0.01 and self.zv < 0.01:
                self.zv = 0
        


         # don't let player get stuck inside of blocks
        if self.collision["insideOfBlock"] != "air":
            if self.collision["insideOfBlock"] != "water":
                self.y += 5

         # do all the position updates that other things use
        self.xv = round(self.xv * 100) / 100
        self.yv = round(self.yv * 100) / 100
        self.zv = round(self.zv * 100) / 100

        self.x += (self.xv * deltaTime)
        self.y += (self.yv * deltaTime)
        self.z += (self.zv * deltaTime)

        
        

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