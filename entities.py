from widelyUsedVariables import blockSize, gravity, maxStackSize
from worldgen import findBlock
import math, pygame, random

# basic entity, no ai or anything
class Entity():
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

        self.xv = 0
        self.yv = 0
        self.zv = 0
        self.deleteSelf = False

        self.width = blockSize
        self.height = self.width

        self.rect = pygame.rect.Rect(0, 0, self.width, self.width)

# used for items that are on the ground, like after breaking something
class ItemEntity(Entity):
    def __init__(self, itemData, x, y, z, xv = 0, yv = 0, zv = 0):
        super().__init__(x, y, z, xv, yv, zv)
        self.itemData = itemData
        self.count = 1

        self.width = blockSize / 2
        self.height = blockSize / 2

        self.maxFallingVelocity = -10

        self.timers = {
            "pickupDelay": 20
        }



    def positionUpdates(self, player):
        self.rect.x = self.x
        self.rect.y = self.z

        a = findBlock(self.x, self.y - self.height, self.z)
        b = findBlock(self.x, self.y - self.height, self.z + self.width)
        c = findBlock(self.x + self.width, self.y - self.height, self.z)
        d = findBlock(self.x + self.width, self.y - self.height, self.z + self.width)
        blockBelow = False
        if a or b or c or d:
            blockBelow = True
        
        if blockBelow:
            # snap to floor
            self.yv = 0
            # normalize y coordinate, should set it to on top of the block
            self.y = math.floor(self.y / blockSize) * blockSize + self.height

            # friction
            self.xv -= self.xv / 15
            self.zv -= self.zv / 15
            if self.xv > -0.1 and self.xv < 0.1:
                self.xv = 0
            if self.zv > -0.1 and self.zv < 0.1:
                self.zv = 0
        else:
            # do gravity
            if self.yv > self.maxFallingVelocity:
                self.yv -= gravity

        # do wall collision, but only if xv/zv is != 0, for performance
        if self.xv != 0:
            if self.xv > 0:
                blockToRight = findBlock(self.x + self.width + 1, self.y, self.z)
                if blockToRight:
                    self.x -= self.xv
                    self.xv = 0
            if self.xv < 0:
                blockToLeft = findBlock(self.x - 1, self.y, self.z)
                if blockToLeft:
                    self.x -= self.xv
                    self.xv = 0

        if self.zv != 0:
            if self.zv > 0:
                blockToUp = findBlock(self.x, self.y, self.z - 1)
                if blockToUp:
                    self.z -= self.zv
                    self.zv = 0
            if self.zv < 0:
                blockToDown = findBlock(self.x, self.y, self.z + self.width + 1)
                if blockToDown:
                    self.z -= self.zv
                    self.zv = 0

        
        self.x += self.xv
        self.y += self.yv
        self.z += self.zv

    def runTimers(self):
        for key, value in self.timers.items():
            if value > 0:
                value -= 1
                print("timer is in fact working? " + str(value))
            if value < 0:
                value += 1

            

    def playerInteraction(self, player):
        if self.timers["pickupDelay"] == 0:
            if self.rect.colliderect(player.rect):

                itemPickedUp = player.giveItem(self.itemData, self.count)

                if itemPickedUp:
                    self.deleteSelf = True

    def doStuff(self, player):
        
        if not self.deleteSelf:
            self.positionUpdates(player)
            self.runTimers()

            self.playerInteraction(player)
