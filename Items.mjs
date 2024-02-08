


/*from GlobalVariables import entities, items, chunks, listOfBlockNames, listOfIntermediateItems, blockSize, gravity, dictOfBlockBreakingStuff
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







print("items initialized")
*/



// Assume you have equivalent implementations for entities, items, chunks, 
// listOfBlockNames, listOfIntermediateItems, blockSize, gravity, and dictOfBlockBreakingStuff
// Also, assume you have equivalent implementations for findBlock, getChunkCoord, 
// getBlockCoord, smallScaleBlockUpdates, and mouse
// Also, assume you have equivalent implementations for ItemEntity, PlaceableItem, ToolItem, 
// IntermediateItem, and any required utility functions
import {
    entities, items, chunks, blockSize, gravity, dictOfBlockBreakingStuff,
    listOfBlockNames, listOfIntermediateItems, consoleLog
} from "./GlobalVariables.mjs";
consoleLog("loading Items.mjs")

import { findBlock, getChunkCoord, getBlockCoord, smallScaleBlockUpdates } from "./Worldgen.mjs";



class Item {
    constructor(name = "air") {
        this.name = name;
        this.slotId = 0;
        this.tooltip = "tooltip unavailable";
    }

    drop(x, y, z, xv, yv, zv, player = null, count = 1) {
        const droppedItem = new ItemEntity(this, count, x, y, z, xv, yv, zv);
        entities.push(droppedItem);

        if (player !== null) {
            if (player.hotbar[this.slotId]["count"] === 1) {
                player.hotbar[this.slotId]["contents"] = "empty";
            } else if (player.hotbar[this.slotId]["count"] >= 2) {
                player.hotbar[this.slotId]["count"] -= 1;
            }
        }
    }
}

class PlaceableItem extends Item {
    constructor(name, tooltip = "", stackable = true) {
        super(name);
        this.tooltip = name;
        if (tooltip !== "") {
            this.tooltip = tooltip;
        }
        this.slotId = 0;
        this.itemType = "PlaceableItem";
        this.stackable = stackable;
        this.placedBlock = {
            "type": name,
            "render": false,
            "alphaValue": 255,
            "hardness": 0,
            "effectiveTool": "none",
        };
        this.placedBlock["hardness"] = dictOfBlockBreakingStuff[name]["hardness"];
        this.placedBlock["effectiveTool"] = dictOfBlockBreakingStuff[name]["effectiveTool"];
    }

    placeItem(player) {
        if (player.canReachSelectedBlock) {
            const blockType = mouse.hoveredBlock.block.type;
            if (blockType === "air" || blockType === "water") {
                const count = player.hotbar[this.slotId].count;
                if (count > 1) {
                    player.hotbar[this.slotId].count -= 1;
                } else if (count === 1) {
                    player.hotbar[this.slotId].count = 0;
                    player.hotbar[this.slotId].contents = "empty";
                } else if (count <= 0) {
                    consoleLog("what the heck, how did you do that??<br />the item count is invalid or something");
                }

                const chunkCoord = mouse.hoveredBlock.chunkCoord;
                const blockCoord = mouse.hoveredBlock.blockCoord;

                chunks[chunkCoord].data[blockCoord] = this.placedBlock;

                smallScaleBlockUpdates(chunkCoord, blockCoord);
            }
        }
    }

    RMBAction(player) {
        // Your implementation here
    }

    RMBPressedAction(player) {
        this.placeItem(player);
    }
}

class ToolItem extends Item {
    constructor(name, toolData = { "attack": 1, "knockback": 1, "breakingPower": 1, "breakingSpeed": 1, "breakingType": "none" },
        tooltip = "", stackable = false) {
        super(name);
        this.slotId = 0;
        this.itemType = "ToolItem";
        this.tooltip = name;
        if (tooltip !== "") {
            this.tooltip = tooltip;
        }
        this.stackable = stackable;
        this.attack = toolData.attack;
        this.knockback = toolData.knockback;
        this.breakingPower = toolData.breakingPower;
        this.breakingSpeed = toolData.breakingSpeed;
        this.breakingType = toolData.breakingType;
        this.durability = 100; // durability will exist when the game actually functions
    }

    RMBPressedAction(player) {
        // Your implementation here
    }

    RMBAction(player) {
        // Your implementation here
    }
}

class IntermediateItem extends Item {
    constructor(name, stackable = true) {
        super(name);
        this.stackable = stackable;
        this.tooltip = name;
        this.slotId = 0;
    }
}

function addItem(name = "air", itemType = "none", toolData = {}, stackable = false) {
    let item;

    if (itemType === "placeable") {
        item = new PlaceableItem(name, true);
    }

    if (itemType === "tool") {
        item = new ToolItem(name, toolData);
    }

    if (itemType === "intermediate") {
        item = new IntermediateItem(name, true);
    }

    items[name] = item;
}

function makeItemsExist() {
    for (const itemName of listOfBlockNames) {
        addItem(itemName, "placeable", {}, true);
    }

    for (const itemName of listOfIntermediateItems) {
        addItem(itemName, "intermediate", {}, true);
    }

    addItem("stone pickaxe", "tool", {
        "attack": 3, "knockback": 1, "breakingPower": 3,
        "breakingSpeed": 20, "breakingType": "pickaxe"
    }, false);

    addItem("stone axe", "tool", {
        "attack": 7, "knockback": 1, "breakingPower": 3,
        "breakingSpeed": 20, "breakingType": "axe"
    }, false);

    addItem("stone shovel", "tool", {
        "attack": 2, "knockback": 1, "breakingPower": 1,
        "breakingSpeed": 25, "breakingType": "shovel"
    }, false);

    addItem("wood pickaxe", "tool", {
        "attack": 2, "knockback": 1, "breakingPower": 2,
        "breakingSpeed": 10, "breakingType": "pickaxe"
    }, false);

    addItem("wood axe", "tool", {
        "attack": 6, "knockback": 1, "breakingPower": 2,
        "breakingSpeed": 10, "breakingType": "axe"
    }, false);

    addItem("wood shovel", "tool", {
        "attack": 1, "knockback": 1, "breakingPower": 1,
        "breakingSpeed": 15, "breakingType": "shovel"
    }, false);
}

consoleLog("items initialized");
