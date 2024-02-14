

import { entities, items, chunks,  listOfBlockNames, 
    listOfIntermediatItems, blockSize, gravity, 
    dictOfBlockBreakingStuff,
    showLoadingProgress} from "./GlobalVariables.mjs";
showLoadingProgress("loading Items.mjs")

import { mouse } from "./Controls.mjs";
import { ItemEntity } from "./Entities.mjs";


class Item {
    constructor (name) {


        this.name = name || "air";
        this.slotId = 0;
        this.tooltip = "tooltip unavailable";
        this.stackable = false;
        
    
        this.drop = function (x, y, z, xv, yv, zv, player = undefined, count = 1) {

        let droppedItem = new ItemEntity(x, y, z, xv, yv, zv, count, this);

        entities.push(droppedItem);

        if (player !== undefined) {
            if (player.hotbar[this.slotId]["count"] == 1) {
                player.hotbar[this.slotId]["contents"] = "empty";
            } else {
                if (player.hotbar[this.slotId].count >= 2) {
                    player.hotbar[this.slotId]["count"] -= 1
                };
            };  
        };
    };

    };
};


class PlaceableItem extends Item {
    constructor (stackable) {
        super(); 
        
        this.stackable = stackable || true;
        this.itemType = "PlaceableItem";

        this.placedBlock = {
            "type": this.name,
            "render": false,
            "alphaValue": 255,
            "hardness": 0,
            "effectiveTool": "none"
        };

        this.placedBlock.hardness = dictOfBlockBreakingStuff[this.name].hardness;
        this.placedBlock.effectiveTool = dictOfBlockBreakingStuff[this.name].effectiveTool;

    this.placeItem = function (player) {

        if (player.canReachSelectedBlock) {
            let blockType = mouse.hoveredBlock.block.type;
            if (blockType == "air" || blockType == "water") {
                let count = player.hotbar[this.slotId].count;

                switch (count) {
                    case count > 1:
                        player.hotbar[this.slotId].count -= 1; break;
                    case count == 1:
                        player.hotbar[this.slotId].count = 0;
                        player.hotbar[this.slotId].contents = "empty";
                        break;
                    case count <= 0:
                        consooeLog("how'd you do that??");
                }
                

                let chunkCoord = mouse.hoveredBlock.chunkCoord;
                let blockCoord = mouse.hoveredBlock.blockCoord;
                

                chunks[chunkCoord].data[blockCoord] = this.placedBlock;

                smallScaleBlockUpdates(chunkCoord, blockCoord)
            };
        };

    };

    def RMBAction(this, player):
        pass
        

    def RMBPressedAction(this, player):
        this.placeItem(player)
    };
};

class ToolItem(Item):
    def __init__(this, name, toolData = {"attack": 1, "knockback": 1,
                                         "breakingPower": 1, "breakingSpeed": 1,
                                         "breakingType": "none"},
                                         tooltip = "", stackable = false):
        super().__init__(name)
        this.slotId = 0
        this.itemType = "ToolItem"
        this.tooltip = this.name
        if tooltip != "":
            this.tooltip = tooltip
        this.stackable = stackable
        
        this.attack = toolData["attack"]
        this.knockback = toolData["knockback"]
        this.breakingPower = toolData["breakingPower"]
        this.breakingSpeed = toolData["breakingSpeed"]
        this.breakingType = toolData["breakingType"]

        this.durability = 100 # durability will exist when the game actually functions
    
    def RMBPressedAction(this, player):
        pass

    def RMBAction(this, player):
        pass

class IntermediateItem(Item):
    def __init__(this, name, stackable = true):
        super().__init__(name)
        this.stackable = stackable
        this.tooltip = this.name
        this.slotId = 0

# adding items to the game
def addItem(name = "air", itemType = "none", toolData = {}, stackable = false):

    if itemType == "placeable":
        item = PlaceableItem(name, stackable = true)
    
    if itemType == "tool":
        item = ToolItem(name, toolData)
    if itemType == "intermediate":
        item = IntermediateItem(name, stackable)

    items[name] = item

def makeItemsExist():
    for itemName in listOfBlockNames:
        addItem(itemName, "placeable", stackable = true)
    for itemName in listOfIntermediateItems:
        addItem(itemName, "intermediate", stackable = true)
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
