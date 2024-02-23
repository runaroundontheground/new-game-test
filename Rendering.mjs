import { canvasWidth, canvasHeight, totalChunkSize, blockSize, chunks, keys, 
chunkSize, canvasWidthInChunks, canvasHeightInChunks, entities, keysPressed, mouse,
itemEntitySize, camera, itemIcons, consoleLog, canvas, ctx, showLoadingProgress } from "./GlobalVariables.mjs";
showLoadingProgress("loading Rendering.mjs");

import { images } from "./ImageLoader.mjs";

import { generateChunkTerrain, runBlockUpdatesAfterGeneration,
generateChunkStructures, findBlock } from "./Worldgen.mjs";
import { player } from "./Player.mjs";




/*
huge rework needed here, probably just delete most of the code, besides the Math i suppose




renderData, how stuff should be rendered
{   first thing accessed should be drawType, if it's none, do not do anything else
    "drawType": "none",
    next should be position, [x, y]
    "position": [x, y],
    then size (width/height)
    "size": [width, height],
    and a dict that contains specified stylings for stuff, which has to be name exact with the context
    properties
    "drawStyles" {
        all should have this
        "globalAlpha": self explanatory
        if the drawType was fill rect
        "fillStyle": color, gradient, etc,
        if the drawType was stroke rect
        "strokeStyle": same values as fillStyle,
        "lineWidth": self explanatory
    }
}


*/


let blockRenderData = {
    "air": {"drawType": "block", "color": undefined, "borderColor": undefined,
            "globalAlpha": 255, "length": blockSize}
};


let itemEntityRenderData = {}


let blockHighlightData = {"color": "black", "widthAndHeight": blockSize, "alpha": 255, "drawType": "strokeRect",
                        "lineWidth": "3px"}


let itemIconSize = player.inventoryRenderingData.slotSize - player.inventoryRenderingData.itemIconShift * 2;

let newCanvas = document.createElement("canvas");
newCanvas.id = "temporary canvas";
let context = newCanvas.getContext("2d");

function addABlock (blockType, color, borderColor, alpha = 255) {

    let data = {
        "drawType": "block",
        "color": color,
        "borderColor": borderColor || color,
        "globalAlpha": alpha,
        "length": blockSize
    }
    

    function nameToRgba(name) {
        context.fillStyle = name;
        context.fillRect(0,0,1,1);
        return context.getImageData(0,0,1,1).data;
    }

    

    if (borderColor === undefined) {
        let newBorderColor = nameToRgba(color);
        consoleLog(newBorderColor)
    }

    newCanvas.width = data.length;
    newCanvas.height = data.length;
    context.fillStyle = data.color;
    context.strokeStyle = data.borderColor;
    context.globalAlpha = data.globalAlpha;
    context.fillRect(0, 0, newCanvas.width, newCanvas.height);
    context.strokeRect(0, 0, newCanvas.width, newCanvas.height);
    let image = newCanvas.getImageData();
    images[blockType] = image;
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);


    blockRenderData[blockType] = data;

};

addABlock("grass", "darkgreen", "brown")
addABlock("dirt", "brown")
addABlock("stone", rgb(125, 125, 125))
addABlock("cobblestone", (150, 150, 150))
addABlock("snowy dirt", (220, 220, 220), "brown")
addABlock("snowy stone", (220, 220, 220), (125, 125, 125))
addABlock("sand", (232, 228, 118))
addABlock("clay", (196, 152, 94))
addABlock("gravel", (150, 150, 150))
addABlock("water", (0, 0, 255), (0, 0, 255))
addABlock("bedrock", (0, 255, 255))
addABlock("log", (110, 79, 38), (110, 79, 38))
addABlock("planks", (140, 109, 68))
addABlock("leaves", (29, 64, 17))



function generateNearbyAreas (rangeOfGeneration = 2, returnChunkList = false) {
    let chunkList = [];
    let cameraChunk = camera.currentChunk;
    let screenExtension = 1;

    let terrainGenRange = {
        "x": {
        "min": cameraChunk[0] - screenExtension - rangeOfGeneration,
        "max": cameraChunk[0] + canvasWidthInChunks + screenExtension + 1 + rangeOfGeneration
        },
        "z": {
            "min": cameraChunk[1] - screenExtension - rangeOfGeneration,
            "max": cameraChunk[1] + canvasHeightInChunks + screenExtension + 1 + rangeOfGeneration
        }
    };

    let structureGenRange = {
        "x": {
        "min": cameraChunk[0] - screenExtension - (rangeOfGeneration - 1),
        "max": cameraChunk[0] + canvasWidthInChunks + screenExtension + 1 + (rangeOfGeneration - 1)
        },
        "z": {
            "min": cameraChunk[1] - screenExtension - (rangeOfGeneration - 1),
            "max": cameraChunk[1] + canvasHeightInChunks + screenExtension + 1 + (rangeOfGeneration - 1)
        }
    };

    let blockUpdateRange = {
        "x": {
        "min": cameraChunk[0] - screenExtension,
        "max": cameraChunk[0] + canvasWidthInChunks + screenExtension + 1
        },
        "z": {
            "min": cameraChunk[1] - screenExtension,
            "max": cameraChunk[1] + canvasHeightInChunks + screenExtension + 1
        }
    };


    for (let x = terrainGenRange.x.min; x < terrainGenRange.x.max; x++) {
        for (let z = terrainGenRange.z.min; z < terrainGenRange.z.max; z++) {
            if (chunks[[x, z].toString] === undefined) {generateChunkTerrain([x, z]);};
        };
    };


    for (let x = structureGenRange.x.min; x < structureGenRange.x.max; x++) {
        for (let z = structureGenRange.z.min; z < structureGenRange.z.max; z++) {
            if (!chunks[[x, z].toString()].structuresGenerated) {generateChunkStructures([x, z]);};
        }
    }

    for (let x = blockUpdateRange.x.min; x < blockUpdateRange.x.max; x++) {
        for (let z = blockUpdateRange.z.min; z < blockUpdateRange.z.max; z++) {
            chunkList.push([x, z]);
            if (!chunks[[x, z].toString()].blocksUpdated) {
                runBlockUpdatesAfterGeneration([x, z]);
            }
        }
    }

    if (returnChunkList) {return chunkList;};
};


export function generateSpawnArea() {
    let chunkList = [];
    let cameraChunk = camera.currentChunk;
    let screenExtension = 1;

    let rangeOfGeneration = 3;


    let terrainGenRange = {
        "x": {
        "min": cameraChunk[0] - screenExtension - rangeOfGeneration,
        "max": cameraChunk[0] + canvasWidthInChunks + screenExtension + 1 + rangeOfGeneration
        },
        "z": {
            "min": cameraChunk[1] - screenExtension - rangeOfGeneration,
            "max": cameraChunk[1] + canvasHeightInChunks + screenExtension + 1 + rangeOfGeneration
        }
    };

    let structureGenRange = {
        "x": {
        "min": cameraChunk[0] - screenExtension - (rangeOfGeneration - 1),
        "max": cameraChunk[0] + canvasWidthInChunks + screenExtension + 1 + (rangeOfGeneration - 1)
        },
        "z": {
            "min": cameraChunk[1] - screenExtension - (rangeOfGeneration - 1),
            "max": cameraChunk[1] + canvasHeightInChunks + screenExtension + 1 + (rangeOfGeneration - 1)
        }
    };

    let blockUpdateRange = {
        "x": {
        "min": cameraChunk[0] - screenExtension,
        "max": cameraChunk[0] + canvasWidthInChunks + screenExtension + 1
        },
        "z": {
            "min": cameraChunk[1] - screenExtension,
            "max": cameraChunk[1] + canvasHeightInChunks + screenExtension + 1
        }
    };


    for (let x = terrainGenRange.x.min; x < terrainGenRange.x.max; x++) {
        for (let z = terrainGenRange.z.min; z < terrainGenRange.z.max; z++) {
            if (chunks[[x, z].toString] === undefined) {generateChunkTerrain([x, z]);};
        };
    };
    ctx.fillText("chunk terrain generated", 100, 100);


    for (let x = structureGenRange.x.min; x < structureGenRange.x.max; x++) {
        for (let z = structureGenRange.z.min; z < structureGenRange.z.max; z++) {
            if (!chunks[[x, z].toString()].structuresGenerated) {generateChunkStructures([x, z]);};
        }
    }
    ctx.fillText("chunk structures generated", 100, 150)

    for (let x = blockUpdateRange.x.min; x < blockUpdateRange.x.max; x++) {
        for (let z = blockUpdateRange.z.min; z < blockUpdateRange.z.max; z++) {
            chunkList.push([x, z]);
            if (!chunks[[x, z].toString()].blocksUpdated) {
                runBlockUpdatesAfterGeneration([x, z]);
            }
        }
    }
    
    ctx.fillText("chunk blocks have been updated", 100, 200)
};
    





export function render(deltaTime) {


    
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // get the chunks to be used for rendering
    let chunkList = generateNearbyAreas(2, true)


    // separate the blocks into layers, so they get rendered in the right order
    // also, keep track of the scale for each y layer
    let yLayer = [];
    let scaleFactors = [];
    for (let i = 0; i < chunkSize[1]; i++) {
        yLayer.push( [] );
        scaleFactors.push( [] );
    };

    
    
    for (const chunkCoord of chunkList) {
        for (let y = 0; y < chunkSize[1]; y++) {
            
        
            // scale images outside of x/z loop, better performance
            
            let scaleFactor = 1
            
            // scale smoother when using exact position rather than player's block coord
            let playerYInBlocks = player.y / blockSize


            if (y > playerYInBlocks) {
                let differenceInBlocks = y - playerYInBlocks;
                differenceInBlocks /= blockSize;
                scaleFactor += differenceInBlocks;
            };
                

            if (y < playerYInBlocks) {
                let differenceInBlocks = playerYInBlocks - y;
                differenceInBlocks /= blockSize;
                scaleFactor -= differenceInBlocks;
            };
                

            if (scaleFactor < 0.1) {scaleFactor = 0.1;};
            if (scaleFactor > 5) {scaleFactor = 5;};

            



            

            let scaledRenderData = blockRenderData;
            

            for (let x = 0; x < chunkSize[0]; x++) {
                for (let z = 0; z < chunkSize[0]; z++) {

                    let block = chunks[chunkCoord.toString()].data[[x, y, z].toString()];
                    
                    if (block.render && block.type != "air")
                        xPos = x * blockSize;
                        zPos = z * blockSize;
                        
                        xPos += chunkCoord[0] * totalChunkSize;
                        zPos += chunkCoord[1] * totalChunkSize;
                        block.useAlpha = false;
                        
                        if (block.globalAlpha < 255 && block.type != "water" && player.blockCoord[1] < y) {
                            let fiveBlocks = 5 * blockSize;

                            if (xPos - fiveBlocks < player.x && xPos + fiveBlocks > player.x) {
                                if (zPos - fiveBlocks < player.z && zPos + fiveBlocks > player.z) {
                                    block.useAlpha = true;
                                };
                            };
                        };

                        if (block.type == "water") {thisBlockHasAlpha = true;};
                                    

                        
                        
                        
                        if (!scaledRenderData[block.type].scaled) {
                            if (scaleFactor != 1) {

                                let scaledLength = scaledImages[block.type].length * scaleFactor;

                                scaledImages[block.type].length = scaledLength;
                                
                            scaledImages[block.type].scaled = true;
                            };
                        };

                        
                        xPos -= player.x
                        zPos -= player.z

                        xPos *= scaleFactor
                        zPos *= scaleFactor
                        
                        xPos -= camera.x - player.x
                        zPos -= camera.z - player.z

                        position = (xPos, zPos)

                        yLayer[y].push()
                };
            };
        };
    };

    renderingData = []


        
    

    // add player to rendering
    if player.blockCoord[1] < chunkSize[1] {
        yLayer[player.blockCoord[1]].push(player.imageData);
    } else {
        renderingData.push(player.imageData);
    }

    i = -1
    if (entities.length > 0) {
        for (let i = -1; i >= -entities.length; i--) {
            let entityRenderData = entities[i].renderData;
            
            yLayer[y].append(entityRenderData);
            
            
        };
    };
    
    // add blocks to rendering
    for y in range(chunkSize[1]):
        renderingData += blocks[y]


    image = player.inventoryRenderingData["hotbarSurface"]
    position = player.inventoryRenderingData["hotbarRenderPosition"]
    imageData = (image, position)
    renderingData.append(imageData)
        
    // run inventory rendering
    if player.otherInventoryData["open"]:
        // render the base part of the inventory
        image = player.inventoryRenderingData["inventorySurface"]
        position = player.inventoryRenderingData["inventoryRenderPosition"]
        imageData = (image, position)

        renderingData.append(imageData)

        // render the 2x2 crafting grid and armor slots (if they're visible)
        if player.otherInventoryData["showCraftingAndArmor"]:
            image = player.inventoryRenderingData["craftingAndArmorSurface"]
            position = player.inventoryRenderingData["craftingAndArmorRenderPosition"]
            imageData = (image, position)

            renderingData.append(imageData)

        // render the 3x3 crafting ui if its visible
        if player.otherInventoryData["showCraftingTable"]:
            image = player.inventoryRenderingData["craftingTableSurface"]
            position = player.inventoryRenderingData["craftingTableRenderPosition"]
            
            imageData = (image, position)
            renderingData.append(imageData)

        // draw a rect thingy over the hovered slot, highlights it
        if mouse.inPlayerInventory and mouse.inASlot:
            image = player.inventoryRenderingData["selectedSlotSurface"]
            slot = player.inventory[mouse.hoveredSlotId]
            position = slot["selectedSlotRenderPosition"]
            
            imageData = (image, position)
            renderingData.append(imageData)

        // highlight selected slots in crafting table
        if mouse.inASlot and mouse.inPlayerCraftingTable and player.otherInventoryData["showCraftingTable"]:
            image = player.inventoryRenderingData["selectedSlotSurface"]
            slot = player.crafting[player.crafting["gridSize"]]["slots"][mouse.hoveredSlotId]
            position = slot["selectedSlotRenderPosition"]

            imageData = (image, position)
            renderingData.append(imageData)

        // also highlight hovered slots, but only in the crafting and armor slots, if they're visible
        if mouse.inPlayerCraftingAndArmor and mouse.inASlot and player.otherInventoryData["showCraftingAndArmor"]:
            image = player.inventoryRenderingData["selectedSlotSurface"]
            slot = player.crafting[player.crafting["gridSize"]]["slots"][mouse.hoveredSlotId]
            position = slot["selectedSlotRenderPosition"]
            
            imageData = (image, position)
            renderingData.append(imageData)

        // render all the items of the base player inventory
        for slot in player.inventory:
            item = slot["contents"]
            if item != "empty":
                image = itemIcons[item.name]
                position = slot["renderPosition"]

                imageData = (image, position)
                renderingData.append(imageData)

                if mouse.inPlayerInventory and mouse.inASlot:
                    if player.inventory[mouse.hoveredSlotId]["contents"] == item:
                        tooltip = item.tooltip
                        if tooltip != "":
                            position = (mouse.x + 10, mouse.y + 5)

                            imageData = convertTextToImageData(tooltip, position)
                            renderingData.append(imageData)


                if slot["count"] > 1:
                    imageData = convertTextToImageData(slot["count"], slot["itemCountRenderPosition"])
                    renderingData.append(imageData)

        // render items in 2x2 crafting and armor, only if they're visible
        if player.otherInventoryData["showCraftingAndArmor"]:
            for slot in player.crafting[player.crafting["gridSize"]]["slots"].values():
                item = slot["contents"]
                if item != "empty":
                    image = itemIcons[item.name]
                    position = slot["renderPosition"]

                    imageData = (image, position)
                    renderingData.append(imageData)

                    if mouse.inPlayerInventory and mouse.inASlot:
                        if player.inventory[mouse.hoveredSlotId]["contents"] == item:
                            tooltip = item.tooltip
                            if tooltip != "":
                                position = (mouse.x + 10, mouse.y + 5)

                                imageData = convertTextToImageData(tooltip, position)
                                renderingData.append(imageData)


                    if slot["count"] > 1:
                        imageData = convertTextToImageData(slot["count"], slot["itemCountRenderPosition"])
                        renderingData.append(imageData)


        

            for slot in player.armor.values():
                //whoops, no armor exists, neither do the slots
                pass
            
        // render stuff in the 3x3 crafting grid if its visible
        if player.otherInventoryData["showCraftingTable"]:
            for slot in player.crafting[player.crafting["gridSize"]]["slots"].values():
                item = slot["contents"]
                if item != "empty":
                    image = itemIcons[item.name]
                    position = slot["renderPosition"]

                    imageData = (image, position)
                    renderingData.append(imageData)

                    if mouse.inPlayerInventory and mouse.inASlot:
                        if player.inventory[mouse.hoveredSlotId]["contents"] == item:
                            tooltip = item.tooltip
                            if tooltip != "":
                                position = (mouse.x + 10, mouse.y + 5)

                                imageData = convertTextToImageData(tooltip, position)
                                renderingData.append(imageData)


                    if slot["count"] > 1:
                        imageData = convertTextToImageData(slot["count"], slot["itemCountRenderPosition"])
                        renderingData.append(imageData)

        

    // run hotbar rendering
    for slotId, slot in enumerate(player.hotbar):
        
        item = slot["contents"]
        currentHotbarSlot = player.otherInventoryData["currentHotbarSlot"]

    
        if slotId == currentHotbarSlot:
            image = player.inventoryRenderingData["selectedSlotSurface"]
            position = slot["selectedSlotRenderPosition"]

            imageData = (image, position)
            renderingData.append(imageData)

            if mouse.inPlayerHotbar and mouse.inASlot:
                image = player.inventoryRenderingData["selectedSlotSurface"]
                position = player.hotbar[mouse.hoveredSlotId]["selectedSlotRenderPosition"]

                imageData = (image, position)
                renderingData.append(imageData)
                if item != "empty" and player.otherInventoryData["open"]:
                    if player.hotbar[mouse.hoveredSlotId]["contents"] == item:
                        tooltip = item.tooltip
                        if tooltip != "":
                            position = (mouse.x + 10, mouse.y + 5)

                            imageData = convertTextToImageData(tooltip, position)
                            renderingData.append(imageData)

        if item != "empty":
            image = itemIcons[item.name]
            position = slot["renderPosition"]

            imageData = (image, position)
            renderingData.append(imageData)

    // fix to selectedHotbarSlot thingy being rendered over the item counts
            
    for slotId, slot in enumerate(player.hotbar):
        if slot["count"] > 1:
            imageData = convertTextToImageData(slot["count"], slot["itemCountRenderPosition"])
            renderingData.append(imageData)


    
    // run mouse's held item rendering
    // also highlights and tells what block you're hovering over
    if not player.otherInventoryData["open"]:
        x = Math.floor(mouse.cameraRelativeX / blockSize)
        z = Math.floor(mouse.cameraRelativeZ / blockSize)
        x *= blockSize
        z *= blockSize
        player.canReachSelectedBlock = false

        if x < player.x + (player.horizontalBlockReach * blockSize):
            if x > player.x - (player.horizontalBlockReach * blockSize):
                if z < player.z + (player.horizontalBlockReach * blockSize):
                    if z > player.z - (player.horizontalBlockReach * blockSize):
                        player.canReachSelectedBlock = true
                        x -= camera.x
                        z -= camera.z

                        position = (x, z)

                        renderingData.append((blockHighlightSurface, position))
                        

                        // do stuff so it displays the mouse's y selection and 
                        // the block that the mouse is theoretically currently
                        // selecting
                        position = (mouse.x, mouse.y + blockSize * 1.5)

                        string = mouse.hoveredBlock["block"]["type"] + ", " + str(mouse.selectedYChange)
                        string += " blocks up/down"
                        
                        imageData = convertTextToImageData(string, position)
                        renderingData.append(imageData)
        
                        


    
    if mouse.heldSlot["contents"] != "empty":
        image = itemIcons[mouse.heldSlot["contents"].name]
        position = (mouse.x + 5, mouse.y + 5)
        imageData = (image, position)

        renderingData.append(imageData)

        shift = player.inventoryRenderingData["slotSize"] - 10


        if mouse.heldSlot["count"] > 1:
            
            position = (mouse.x + shift, mouse.y + shift)
            imageData = convertTextToImageData(mouse.heldSlot["count"], position)
            renderingData.append(imageData)

    

    // debug things
    debugRenderingStuff = "camera chunk: " + str(camera.currentChunk) + ", player chunk: " + str(player.chunkCoord)
    debugRenderingStuff += " player pos: " + str(round(player.position[0]))+ ", " + str(round(player.position[1])) + ", " + str(round(player.position[2]))
    imageData = convertTextToImageData(debugRenderingStuff, (100, 300))
    renderingData.append(imageData)

    
    screen.blits(renderingData)

    // pretty much just debug after this
    
    debugRenderingStuff2 = "player block position " + str(player.blockCoord)
    debugRenderingStuff2 += "player yv " + str(player.yv)
    debugRenderingStuff3 = "mouse pos: " + str(mouse.pos) + ", mouseRelativePos: " + str(mouse.cameraRelativePos)

    
    thing2 = font.render(debugRenderingStuff2, 0, (255, 0, 0))
    thing3 = font.render(debugRenderingStuff3, 0, (255, 0, 0))
    
    screen.blit(thing2, (100, 200))
    screen.blit(thing3, (100, 100))

    pygame.display.flip()

};


showLoadingProgress("rendering initialized")


