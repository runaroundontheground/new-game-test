from widelyUsedVariables import blockSize, gravity
from worldgen import findBlock
import math, pygame

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
    def __init__(self, itemData, x, y, z):
        super().__init__(x, y, z)
        self.itemData = itemData.__dict__
        self.yv = 10

        self.width = blockSize / 2
        self.height = blockSize / 2

        self.maxFallingVelocity = 10
        

    def doStuff(self, player):

        self.rect.x = self.x
        self.rect.y = self.z

        a = findBlock(self.x, self.y - self.height, self.z)
        b = findBlock(self.x, self.y - self.height, self.z + self.width)
        c = findBlock(self.x + self.width, self.y - self.height, self.z)
        d = findBlock(self.x + self.width, self.y - self.height, self.z + self.width)
        blockBelow = False
        if a or b or c or d:
            blockBelow = True
        # gravity
        if blockBelow:
            self.yv = 0
            # normalize y coordinate, should set it to on top of the block
            self.y = math.floor(self.y / blockSize) * blockSize
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

        if self.rect.colliderect(player.rect):
            print("give player an item")
            self.deleteSelf = True

        self.x += self.xv
        self.y += self.yv
        self.z += self.zv