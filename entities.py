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
    def __init__(self, itemData, x, y, z):
        super().__init__(x, y, z)
        self.itemData = itemData
        self.xv = random.randint(-5, 5)
        self.zv = random.randint(-5, 5)
        self.y += 5
        self.yv = random.randint(1, 10)

        self.width = blockSize / 2
        self.height = blockSize / 2

        self.maxFallingVelocity = -10



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

    def playerInteraction(self, player):
        if self.rect.colliderect(player.rect):

            def checkStackables(slot):
                if slot["contents"] != "empty":
                    if slot["contents"].stackable:
                        if slot["contents"].name == self.itemData.name:
                            if slot["count"] < maxStackSize:
                                slot["count"] += 1
                                self.deleteSelf = True
                                print("added 1 item to the slot")

            def checkEmptySlots(slot):
                if slot["contents"] == "empty":
                    slot["count"] = 1
                    slot["contents"] = self.itemData
                    self.deleteSelf = True
                    print("put an item in an empty slot")
                    
            if self.itemData.stackable:
                for slot in player.hotbar:
                    checkStackables(slot)
                    if self.deleteSelf: break

            if not self.deleteSelf:
                for slot in player.hotbar:
                    checkEmptySlots(slot)
                    if self.deleteSelf: break

            if not self.deleteSelf and self.itemData.stackable:
                for slot in player.inventory:
                    checkStackables(slot)
                    if self.deleteSelf: break

            if not self.deleteSelf:
                for slot in player.inventory:
                    checkEmptySlots(slot)
                    if self.deleteSelf: break

    def doStuff(self, player):

        self.positionUpdates(player)

        self.playerInteraction(player)
