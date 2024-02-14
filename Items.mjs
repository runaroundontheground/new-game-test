

import { entities, items, chunks,  listOfBlockNames, 
    listOfIntermediatItems, blockSize, gravity, 
    dictOfBlockBreakingStuff,
    showLoadingProgress} from "./GlobalVariables.mjs";
showLoadingProgress("loading Items.mjs")

import { mouse } from "./Controls.mjs";
import { ItemEntity } from "./Entities.mjs";


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
            if player.hotbar[self.slotId]["count"] == 1:
                player.hotbar[self.slotId]["contents"] = "empty"
            elif player.hotbar[self.slotId]["count"] >= 2:
                player.hotbar[self.slotId]["count"] -= 1

# an item that can be placed, like wood or something
class PlaceableItem(Item):
    def __init__(self, name, tooltip = "", stackable = True):
        super().__init__(name)
        self.tooltip = self.name
        if tooltip != "":
            self.tooltip = tooltip
        self.slotId = 0
        self.itemType = "PlaceableItem"
        self.stackable = stackable
        self.placedBlock = {
            "type": self.name,
            "render": False,
            "alphaValue": 255,
            "hardness": 0,
            "effectiveTool": "none"
        }
        self.placedBlock["hardness"] = dictOfBlockBreakingStuff[self.name]["hardness"]
        self.placedBlock["effectiveTool"] = dictOfBlockBreakingStuff[self.name]["effectiveTool"]

    def placeItem(self, player):

        if player.canReachSelectedBlock:
            blockType = mouse.hoveredBlock["block"]["type"]
            if blockType == "air" or blockType == "water":
                count = player.hotbar[self.slotId]["count"]
                if count > 1:
                    player.hotbar[self.slotId]["count"] -= 1
                    
                elif count == 1:
                    player.hotbar[self.slotId]["count"] = 0
                    player.hotbar[self.slotId]["contents"] = "empty"
                    
                elif count <= 0:
                    print("what the heck, how did you do that??\nthe item count is invalid or something")

                chunkCoord = mouse.hoveredBlock["chunkCoord"]
                blockCoord = mouse.hoveredBlock["blockCoord"]
                

                chunks[chunkCoord]["data"][blockCoord] = self.placedBlock.copy()

                smallScaleBlockUpdates(chunkCoord, blockCoord)



    def RMBAction(self, player):
        pass
        

    def RMBPressedAction(self, player):
        self.placeItem(player)

class ToolItem(Item):
    def __init__(self, name, toolData = {"attack": 1, "knockback": 1,
                                         "breakingPower": 1, "breakingSpeed": 1,
                                         "breakingType": "none"},
                                         tooltip = "", stackable = False):
        super().__init__(name)
        self.slotId = 0
        self.itemType = "ToolItem"
        self.tooltip = self.name
        if tooltip != "":
            self.tooltip = tooltip
        self.stackable = stackable
        
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

class IntermediateItem(Item):
    def __init__(self, name, stackable = True):
        super().__init__(name)
        self.stackable = stackable
        self.tooltip = self.name
        self.slotId = 0

# adding items to the game
def addItem(name = "air", itemType = "none", toolData = {}, stackable = False):

    if itemType == "placeable":
        item = PlaceableItem(name, stackable = True)
    
    if itemType == "tool":
        item = ToolItem(name, toolData)
    if itemType == "intermediate":
        item = IntermediateItem(name, stackable)

    items[name] = item

def makeItemsExist():
    for itemName in listOfBlockNames:
        addItem(itemName, "placeable", stackable = True)
    for itemName in listOfIntermediateItems:
        addItem(itemName, "intermediate", stackable = True)
    addItem("stone pickaxe", "tool",
            {"attack": 3, "knockback": 1, "breakingPower": 3,
            "breakingSpeed": 20, "breakingType": "pickaxe"})
    
    addItem("stone axe", "tool",
            {"attack": 7, "knockback": 1, "breakingPower": 3,
            "breakingSpeed": 20, "breakingType": "axe"})
    
    addItem("stone shovel", "tool",
            {"attack": 2, "knockback": 1, "breakingPower": 1,
            "breakingSpeed": 25, "breakingType": "shovel"})


    addItem("wood pickaxe", "tool",
            {"attack": 2, "knockback": 1, "breakingPower": 2,
            "breakingSpeed": 10, "breakingType": "pickaxe"})
    
    addItem("wood axe", "tool",
            {"attack": 6, "knockback": 1, "breakingPower": 2,
            "breakingSpeed": 10, "breakingType": "axe"})
    
    addItem("wood shovel", "tool",
            {"attack": 1, "knockback": 1, "breakingPower": 1,
            "breakingSpeed": 15, "breakingType": "shovel"})






showLoadingProgress("Items.mjs loaded");
