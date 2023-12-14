from widelyUsedVariables import blockSize, gravity
from worldgen import findBlock
import math

# basic entity, no ai or anything
class Entity():
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

        self.xv = 0
        self.yv = 0
        self.zv = 0

# used for items that are on the ground, like after breaking something
class ItemEntity(Entity):
    def __init__(self, itemData, x, y, z):
        super().__init__(x, y, z)
        self = itemData
        self.maxFallingVelocity = 10

    def runSelf(self, player):
        blockBelow = findBlock(self.x, self.y - blockSize, self.z)
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

        # check for collision with player
        # probably just within same block as player

        # do stuff on collision with that

        # figure out what layer this should be rendered on, and then figure out
        # scaling in rendering 
        # probably entities[index].y to use to figure out scaling compared to player