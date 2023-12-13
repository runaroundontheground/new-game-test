from widelyUsedVariables import entities, items, chunks, listOfBlockNames, blockSize, gravity
from worldgen import findBlock, getChunkCoord, getBlockCoord, smallScaleBlockUpdates
from controls import mouse
from player import player
import math



# basic item, default values to make it exist in player inventory properly
class Item():
    def __init__(self, name = "air"):
        self.name = name
        self.slotId = 0
    
    # drop/throw this item out as an entity
    def drop(self, x = 0, y = 0, z = 0, throwItem = False):

        droppedItem = ItemEntity(self, x, y, z)

        entities.append(droppedItem)
        
        if player.inventory[self.slotId]["count"] == 1:
            player.inventory[self.slotId]["contents"] = "empty"
        elif player.inventory[self.slotId]["count"] >= 2:
            player.inventory[self.slotId]["count"] -= 1

# an item that can be placed, like wood or something
class PlaceableItem(Item):
    def __init__(self, name):
        super().__init__(name)
        self.itemType = "PlaceableItem"
        self.placedBlock = {
            "type": self.name,
            "render": False,
            "alphaValue": 0
        }

    def placeItem(self):

        
        blockType = mouse.hoveredBlock["block"]["type"]
        if blockType == "air" or blockType == "water":
            count = player.hotbar[self.slotId]["count"]
            if count > 1:
                player.hotbar[self.slotId]["count"] -= 1
                
            elif count == 1:
                player.hotbar[self.slotId]["count"] = 0
                player.hotbar[self.slotId]["contents"] = "empty"
                
            elif count <= 0:
                print("what the heck, how did you do that??")

            chunkCoord = mouse.hoveredBlock["chunkCoord"]
            blockCoord = mouse.hoveredBlock["blockCoord"]

            chunks[chunkCoord]["data"][blockCoord] = self.placedBlock

            smallScaleBlockUpdates(chunkCoord, blockCoord)


    def RMBAction(self):
        pass
        

    def RMBPressedAction(self):
        self.placeItem()

class ToolItem(Item):
    def __init__(self, name):
        super().__init__(name)
        self.itemType = "ToolItem"
        
        self.attack = 1 # damage value of player's fist
        self.knockback = 1 # knockback of player's fist
        self.breakingPower = 1 # player's fist power, or what's allowed to be broken w/ fist
        self.breakingSpeed = 1 # speed of player's fist
        self.breakingType = "none"

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

    def runSelf(self):
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

test = PlaceableItem("dirt")
test.drop(100, 300, 100)
# adding items to the game
def addItem(name = "air", itemType = "none"):

    if itemType == "placeable":
        item = PlaceableItem(name)
    
    if itemType == "tool":
        pass

    items[name] = item

def makeItemsExist():
    for itemName in listOfBlockNames:
        addItem(itemName, "placeable")
