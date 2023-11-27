from widelyUsedVariables import entities
from player import inventory


# basic item, default values to make it exist in player inventory properly
class Item():
    def __init__(self, itemData = {
        "name": "dirt",
        "id": 0
    }, slotId = 0):
        self.itemData = itemData
        self.slotId = slotId
    
    # drop/throw this item out as an entity
    def drop(self, x = 0, y = 0, z = 0, throwItem = False):
        droppedItem = ItemEntity(self.itemData, x, y, z)

        entities.append(droppedItem)
        

        # create an ItemEntity, append it to a list of entities?
        # set player's inventory slot that is this item to "empty" or something

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
    def __init__(self, itemData = {
        "name": "dirt",
        "id": 0
    }, x = 0, y = 0, z = 0):
        
        self.itemData = itemData
        self.x = x
        self.y = y
        self.z = z

    def runSelf(self):
        # all the logic for an item on the ground
        pass