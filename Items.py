from GlobalVariables import entities, items, chunks, listOfBlockNames, blockSize, gravity, dictOfBlockBreakingStuff
from Worldgen import findBlock, getChunkCoord, getBlockCoord, smallScaleBlockUpdates
from Controls import mouse
from Entities import ItemEntity



# basic item, default values to make it exist in player inventory properly
class Item():
    def __init__(self, name = "air"):
        self.name = name
        self.slotId = 0
        self.tooltip = "tooltip unavailable"
        
    
    # drop/throw this item out as an entity
    def drop(self, x, y, z, xv, yv, zv, player = None, count = 1):

        droppedItem = ItemEntity(self, count, x, y, z, xv, yv, zv)

        entities.append(droppedItem)

        if player != None:
            print("doing stuff to player inventory after dropping something")
            if player.hotbar[self.slotId]["count"] == 1:
                player.hotbar[self.slotId]["contents"] = "empty"
            elif player.hotbar[self.slotId]["count"] >= 2:
                player.hotbar[self.slotId]["count"] -= 1

# an item that can be placed, like wood or something
class PlaceableItem(Item):
    def __init__(self, name, tooltip = ""):
        super().__init__(name)
        self.tooltip = self.name
        if tooltip != "":
            self.tooltip = tooltip
        self.slotId = 0
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
    def __init__(self, name, toolData = {"attack": 1, "knockback": 1,
                                         "breakingPower": 1, "breakingSpeed": 1,
                                         "breakingType": "none"},
                                         tooltip = ""):
        super().__init__(name)
        self.slotId = 0
        self.itemType = "ToolItem"
        self.tooltip = self.name
        if tooltip != "":
            self.tooltip = tooltip
        self.stackable = False
        
        self.attack = toolData["attack"]
        self.knockback = toolData["knockback"]
        self.breakingPower = toolData["breakingPower"]
        self.breakingSpeed = toolData["breakingSpeed"]
        self.breakingType = toolData["breakingType"]

        self.durability = 100 # durability will exist when the game actually functions
    
    def RMBPressedAction(self, player):
        pass

    def RMBAction(self, player):
        pass


# adding items to the game
def addItem(name = "air", itemType = "none", toolData = {}):

    if itemType == "placeable":
        item = PlaceableItem(name)
    
    if itemType == "tool":
        item = ToolItem(name, toolData)

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







print("items initialized")