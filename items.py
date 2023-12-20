from widelyUsedVariables import entities, items, chunks, listOfBlockNames, blockSize, gravity, dictOfBlockBreakingStuff
from worldgen import findBlock, getChunkCoord, getBlockCoord, smallScaleBlockUpdates
from controls import mouse
from entities import ItemEntity



# basic item, default values to make it exist in player inventory properly
class Item():
    def __init__(self, name = "air"):
        self.name = name
        self.slotId = 0
        
    
    # drop/throw this item out as an entity
    def drop(self, x = 0, y = 0, z = 0, throwItem = False, player = None):

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
        self.stackable = True
        self.placedBlock = {
            "type": self.name,
            "render": False,
            "alphaValue": 0,
            "hardness": 0,
            "effectiveTool": "none"
        }
        self.placedBlock["hardness"] = dictOfBlockBreakingStuff[self.name]["hardness"]
        self.placedBlock["effectiveTool"] = dictOfBlockBreakingStuff[self.name]["effectiveTool"]

    def placeItem(self, player):

        
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


    def RMBAction(self, player):
        pass
        

    def RMBPressedAction(self, player):
        self.placeItem(player)

class ToolItem(Item):
    def __init__(self, name, attack = 1, knockback = 1, breakingPower = 1,
                 breakingSpeed = 1, breakingType = "none"):
        super().__init__(name)
        self.itemType = "ToolItem"
        self.stackable = False
        
        self.attack = attack
        self.knockback = knockback
        self.breakingPower = breakingPower
        self.breakingSpeed = breakingSpeed
        self.breakingType = breakingType

        self.durability = 100 # durability will exist when the game actually functions
    
    def RMBPressedAction(self, player):
        pass

    def RMBAction(self, player):
        pass


# adding items to the game
def addItem(name = "air", itemType = "none", toolData = "none"):

    if itemType == "placeable":
        item = PlaceableItem(name)
    
    if itemType == "tool":
        item = ToolItem(name)

    items[name] = item

def makeItemsExist():
    for itemName in listOfBlockNames:
        addItem(itemName, "placeable")
    addItem("stone pickaxe", "tool",
            {"attack": 3, "knockback": 1, "breakingPower": 3,
            "breakingSpeed": 20, "breakingType": "pickaxe"})
    
    addItem("stone axe", "tool",
            {"attack": 7, "knockback": 1, "breakingPower": 3,
            "breakingSpeed": 20, "breakingType": "axe"})
    
    addItem("stone shovel", "tool",
            {"attack": 2, "knockback": 1, "breakingPower": 1,
            "breakingSpeed": 20, "breakingType": "shovel"})