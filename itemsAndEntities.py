from widelyUsedVariables import entities, items, chunks, listOfBlockItems, blockSize
from worldgen import findBlock, getChunkCoord, getBlockCoord, smallScaleBlockUpdates
from controls import mouse
from player import player




# basic item, default values to make it exist in player inventory properly
class Item():
    def __init__(self, name = "air"):
        self.name = name
        self.slotId = 0
    
    # drop/throw this item out as an entity
    def drop(self, x = 0, y = 0, z = 0, throwItem = False):
        droppedItem = ItemEntity(self.itemData, x, y, z)

        entities.append(droppedItem)
        
        """
        TO DO:
            on player's side, check for what the count of the item
            is for this slot, if it's one when you drop it, set the slot contents
            to "empty", otherwise just drop it and subtract one from the item count
        """

# an item that can be placed, like wood or something
class PlaceableItem(Item):
    def __init__(self, name):
        super().__init__(name)
        # IMPORTANT NOTE!
        # the name of any item that can be placed MUST correspond to an existing block
        # otherwise, game will break (maybe add a check for if the block exists?)
        # if it doesn't exist, place nothing or air i guess
        self.placedBlock = {
            "type": self.name,
            "render": False,
            "usesAlpha": False
        }

    def placeItem(self):

        x = mouse.cameraRelativeX
        y = mouse.selectedY
        z = mouse.cameraRelativeZ
        
        blockInPlacementSpot = findBlock(x, y, z)
        print(blockInPlacementSpot)
        
        if not blockInPlacementSpot:
            chunkCoord = getChunkCoord(x, z)
            blockCoord = getBlockCoord(x, y, z)

            smallScaleBlockUpdates(chunkCoord, blockCoord, self.placedBlock)



    def LMBAction(self):
        pass

    def LMBPressedAction(self):
        pass

    def RMBAction(self):
        pass
        

    def RMBPressedAction(self):
        self.placeItem()

        


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
    def __init__(self, x, y, z, name = "air"):
        super().__init__(x, y, z)
        self.name = name

    def runSelf(self):
        # all the logic for an item on the ground
        pass


# adding items to the game
def addItem(name = "air", itemType = "none"):

    if itemType == "placeable":
        item = PlaceableItem(name)
    
    if itemType == "tool":
        pass

    items[name] = item

def makeItemsExist():
    for itemName in listOfBlockItems:
        addItem(itemName, "placeable")
