from widelyUsedVariables import entities, items

# basic item, default values to make it exist in player inventory properly
class Item():
    def __init__(self, itemData = {
        "name": "air",
        "id": 0
    }, slotId = 0):
        self.itemData = itemData
        self.slotId = slotId
    
    # drop/throw this item out as an entity
    def drop(self, x = 0, y = 0, z = 0, throwItem = False):
        droppedItem = ItemEntity(self.itemData, x, y, z)

        entities.append(droppedItem)
        
        # set player's inventory slot that is this item to "empty" or something

# an item that can be placed, like wood or something
class PlaceableItem(Item):
    def __init__(self):
        # IMPORTANT NOTE!
        # the name of any item that can be placed MUST correspond to an existing block
        # otherwise, game will break (maybe add a check for if the block exists?)
        # if it doesn't exist, place nothing or air i guess
        self.placedItem = self.itemData["name"]

def addItem(name = "air"):
    
    id = len(items) - 1
    itemData = {
        "name": name,
        "id": id
    }

    item = Item(itemData, id)

    items.append(item)

airItem = Item()
items.append(airItem)
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
        "name": "air",
        "id": 0
    }, x = 0, y = 0, z = 0):
        
        self.itemData = itemData
        self.x = x
        self.y = y
        self.z = z

    def runSelf(self):
        # all the logic for an item on the ground
        pass