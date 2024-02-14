import { canvasWidth, canvasHeight, totalChunkSize, blockSize, chunks, keys,
chunkSize, canvasWidthInChunks, canvasHeightInChunks, entities, keysPressed,
itemEntitySize, camera, itemIcons, consoleLog, canvas, ctx, images, showLoadingProgress } from "./GlobalVariables.mjs";
showLoadingProgress("loading Rendering.mjs");

import { generateChunkTerrain, runBlockUpdatesAfterGeneration,
generateChunkStructures, findBlock } from "./Worldgen.mjs";
import { mouse } from "./Controls.mjs";
import { player } from "./Player.mjs";




let blockRenderingData = {
    "air": {"color": "black", "widthAndHeight": blockSize, "alpha": 255}
};
let itemEntityIcons = {}


let blockHighlightData = {"color": "black", "widthAndHeight": blockSize, "alpha": 255}


let itemIconSize = player.inventoryRenderingData.slotSize - player.inventoryRenderingData.itemIconShift * 2



function loadImage(path, name) {
    let image = new Image()
    
    images[name] = image;

    itemEntityImage = image.copy()
    size = (itemEntitySize, itemEntitySize)
    itemEntityImage = pygame.transform.scale(itemEntityImage, size)
    itemEntityIcons[name] = itemEntityImage

    return image;
}
images = {
    "stick": loadImage("stick.png", "stick"),
    "stone pickaxe": loadImage("tools/stone pickaxe.png", "stone pickaxe"),
    "stone axe": loadImage("tools/stone axe.png", "stone axe"),
    "wood pickaxe": loadImage("tools/wood pickaxe.png", "wood pickaxe"),
    "wood axe": loadImage("tools/wood axe.png", "wood axe")
}


def addABlock(blockName, blockColor, blockBorderColor = "unassigned",
              hasAlpha = False, alphaValue = 255):
    imageSize = (blockSize, blockSize)
    baseSurface = pygame.surface.Surface(imageSize)
    fillingRect = pygame.rect.Rect(2, 2, blockSize - 4, blockSize - 4)

    block = baseSurface.copy()
    
    if blockBorderColor == "unassigned":
        red = blockColor[0] - 10
        if red < 0:
            red = 0
        green = blockColor[1] - 10
        if green < 0:
            green = 0
        blue = blockColor[2] - 10
        if blue < 0:
            blue = 0
        borderColor = (red, green, blue)
    else:
        borderColor = blockBorderColor

    block.fill(borderColor)
    
    block.fill(blockColor, fillingRect)

    if hasAlpha:
        block.set_alpha(alphaValue)




    
    blockImages[blockName] = {
        "data": block,
        "scaled": False,
        # alphaData: if there are blocks with multiple different alpha values, then 
        # it'll append another thing to the list for that specific alpha value
        # the key is the same as the alpha value, so for instance, that's 0 alpha
        "alphaData": {
            #0: block just the image data, but with alpha in it
            }
    }

    # adding item icons for blocks specifically

    slotSize = player.inventoryRenderingData["slotSize"]
    blockIcon = block.copy()
    targetSize = slotSize - player.inventoryRenderingData["itemIconShift"] * 2

    scale = abs(targetSize / blockSize)

    blockIcon = pygame.transform.scale_by(blockIcon, scale)
    
    itemIcons[blockName] = blockIcon

    itemEntityIcon = block.copy()
    scale = itemEntitySize / blockSize

    itemEntityIcon = pygame.transform.scale_by(itemEntityIcon, scale)
    itemEntityIcons[blockName] = itemEntityIcon

addABlock("grass", (0, 200, 0), (150, 75, 0))
addABlock("dirt", (150, 75, 0))
addABlock("stone", (125, 125, 125))
addABlock("cobblestone", (150, 150, 150))
addABlock("snowy dirt", (220, 220, 220), (150, 75, 0))
addABlock("snowy stone", (220, 220, 220), (125, 125, 125))
addABlock("sand", (232, 228, 118))
addABlock("clay", (196, 152, 94))
addABlock("gravel", (150, 150, 150))
addABlock("water", (0, 0, 255), (0, 0, 255))
addABlock("bedrock", (0, 255, 255))
addABlock("log", (110, 79, 38), (110, 79, 38))
addABlock("planks", (140, 109, 68))
addABlock("leaves", (29, 64, 17))

imageData = convertTextToImageData("block images generated", (100, 75))
screen.blits([imageData])
pygame.display.flip()



        

def generateNearbyAreas(rangeOfGeneration = 2, returnChunkList = False):
    chunkList = []
    cameraChunk = camera.currentChunk
    screenExtension = 1

    xRange = cameraChunk[0] - screenExtension
    maxXRange = cameraChunk[0] + canvasWidthInChunks + screenExtension + 1
    zRange = cameraChunk[1] - screenExtension
    maxZRange = cameraChunk[1] + canvasHeightInChunks + screenExtension + 1

    # initial generation in a larger area
    for x in range(xRange - rangeOfGeneration, maxXRange + rangeOfGeneration):
        for z in range(zRange - rangeOfGeneration, maxZRange + rangeOfGeneration):
            if (x, z) not in chunks:
                generateChunkTerrain((x, z))

    # generate structures
    for x in range(xRange - (rangeOfGeneration - 1), maxXRange + (rangeOfGeneration - 1)):
        for z in range(zRange - (rangeOfGeneration - 1), maxZRange + (rangeOfGeneration - 1)):
        
            if not chunks[(x, z)]["structuresGenerated"]:
                generateChunkStructures((x, z))

    # prepare the chunks for being rendered when all generation is (probably) done
    for x in range(xRange, maxXRange):
        for z in range(zRange, maxZRange):
            chunkList.append((x, z))
            if not chunks[(x, z)]["blocksUpdated"]:
                runBlockUpdatesAfterGeneration((x, z))

    if returnChunkList:
        return chunkList


def generateSpawnArea():
    chunkList = []
    cameraChunk = camera.currentChunk
    screenExtension = 1

    xRange = cameraChunk[0] - screenExtension
    maxXRange = cameraChunk[0] + canvasWidthInChunks + screenExtension + 1
    zRange = cameraChunk[1] - screenExtension
    maxZRange = cameraChunk[1] + canvasHeightInChunks + screenExtension + 1

    rangeOfGeneration = 3

    # initial generation in a larger area
    for x in range(xRange - rangeOfGeneration, maxXRange + rangeOfGeneration):
        for z in range(zRange - rangeOfGeneration, maxZRange + rangeOfGeneration):
            if (x, z) not in chunks:
                generateChunkTerrain((x, z))

    imageData = convertTextToImageData("chunk terrain generated", (100, 100))
    screen.blits([imageData])
    pygame.display.flip()

    # generate structures
    for x in range(xRange - (rangeOfGeneration - 1), maxXRange + (rangeOfGeneration - 1)):
        for z in range(zRange - (rangeOfGeneration - 1), maxZRange + (rangeOfGeneration - 1)):
            if not chunks[(x, z)]["structuresGenerated"]:
                generateChunkStructures((x, z))

    imageData = convertTextToImageData("chunk structures generated", (100, 150))
    screen.blits([imageData])
    pygame.display.flip()

    # prepare the chunks for being rendered when all generation is (probably) done
    for x in range(xRange, maxXRange):
        for z in range(zRange, maxZRange):
            chunkList.append((x, z))
            if not chunks[(x, z)]["blocksUpdated"]:
                runBlockUpdatesAfterGeneration((x, z))

    imageData = convertTextToImageData("chunk blocks have been updated", (100, 200))
    screen.blits([imageData])
    pygame.display.flip()
    





def render(deltaTime):



    screen.fill((0, 0, 0))
    # get the chunks to be used for rendering
    chunkList = generateNearbyAreas(2, True)


    # separate the blocks into layers, so they get rendered in the right order
    # also, keep track of the scale for each y layer
    blocks = []
    scaleFactors = []
    for i in range(chunkSize[1]):
        blocks.append( [] )
        scaleFactors.append( [] )

    
    

    for chunkCoord in chunkList:
        for y in range(chunkSize[1]):
            
        
            # scale images outside of x/z loop, better performance
            
            scaleFactor = 1
            
            # scale smoother when using exact position rather than player's block coord
            playerYInBlocks = player.y / blockSize


            if y > playerYInBlocks:
                differenceInBlocks = y - playerYInBlocks
                differenceInBlocks /= blockSize
                scaleFactor += differenceInBlocks
                

            if y < playerYInBlocks:
                differenceInBlocks = playerYInBlocks - y
                differenceInBlocks /= blockSize
                scaleFactor -= differenceInBlocks
                

            if scaleFactor < 0.1:
                scaleFactor = 0.1

            



            
            scaleFactors[y] = scaleFactor

            scaledImages = blockImages.copy()
            

            for x in range(chunkSize[0]):
                for z in range(chunkSize[0]):

                    block = chunks[chunkCoord]["data"][(x, y, z)]
                    
                    if block["render"] and block["type"] != "air":
                        xPos = x * blockSize
                        zPos = z * blockSize
                        
                        xPos += chunkCoord[0] * totalChunkSize
                        zPos += chunkCoord[1] * totalChunkSize

                        thisBlockHasAlpha = False
                        
                        if block["alphaValue"] < 255:
                            if block["type"] != "water":
                                if player.blockCoord[1] < y: # player is underneath this block
                                    fiveBlocks = 5 * blockSize

                                    if xPos - fiveBlocks < player.x and xPos + fiveBlocks > player.x:
                                        if zPos - fiveBlocks < player.z and zPos + fiveBlocks > player.z:
                                            thisBlockHasAlpha = True

                            if block["type"] == "water":
                                thisBlockHasAlpha = True
                                    

                        
                        
                        
                        if not scaledImages[block["type"]]["scaled"]: # image has not been scaled
                            if scaleFactor != 1:

                                newImageData = scaledImages[block["type"]]["data"]
                                #if scaleFactor > 1:
                                #    newImageData = pygame.transform.scale_by(newImageData, scaleFactor * 1.1)
                                if True:#scaleFactor < 1:
                                    newImageData = pygame.transform.scale_by(newImageData, scaleFactor)
                                scaledImages[block["type"]]["data"] = newImageData
                                
                            scaledImages[block["type"]]["scaled"] = True

                        if thisBlockHasAlpha:
                            
                            blockType = block["type"]
                            alphaValue = block["alphaValue"]


                            imageExists = scaledImages[blockType]["alphaData"].get(alphaValue, False)
                            
                            if imageExists == False:
                                
                                newImage = scaledImages[blockType]["data"].copy()
                                newImage.set_alpha(alphaValue)

                                scaledImages[blockType]["alphaData"][alphaValue] = newImage

                                
                            image = scaledImages[blockType]["alphaData"][alphaValue]

                        else:
                            image = scaledImages[block["type"]]["data"]

                        
                        xPos -= player.x
                        zPos -= player.z

                        xPos *= scaleFactor
                        zPos *= scaleFactor
                        
                        xPos -= camera.x - player.x
                        zPos -= camera.z - player.z

                        position = (xPos, zPos)
                        imageData = (image, position)

                        blocks[y].append(imageData)

    renderingData = []


        
    

    # add player to rendering
    if player.blockCoord[1] < chunkSize[1]:
        blocks[player.blockCoord[1]].append(player.imageData)
    else:
        renderingData.append(player.imageData)

    i = -1
    if len(entities) != 0:
        while i >= -len(entities):
            entity = entities[i]
            
            image = itemEntityIcons[entity.itemData.name]
            
            y = math.floor(entity.y / blockSize)

            if y >= chunkSize[1]:
                y = chunkSize[1] - 1
            if y < 0:
                y = 0

            
            x = entity.x - camera.x
            z = entity.z - camera.z

            position = (x, z)
            imageData = (image, position)
            
            blocks[y].append(imageData)
            
            
            i -= 1
    
    # add blocks to rendering
    for y in range(chunkSize[1]):
        renderingData += blocks[y]


    image = player.inventoryRenderingData["hotbarSurface"]
    position = player.inventoryRenderingData["hotbarRenderPosition"]
    imageData = (image, position)
    renderingData.append(imageData)
        
    # run inventory rendering
    if player.otherInventoryData["open"]:
        # render the base part of the inventory
        image = player.inventoryRenderingData["inventorySurface"]
        position = player.inventoryRenderingData["inventoryRenderPosition"]
        imageData = (image, position)

        renderingData.append(imageData)

        # render the 2x2 crafting grid and armor slots (if they're visible)
        if player.otherInventoryData["showCraftingAndArmor"]:
            image = player.inventoryRenderingData["craftingAndArmorSurface"]
            position = player.inventoryRenderingData["craftingAndArmorRenderPosition"]
            imageData = (image, position)

            renderingData.append(imageData)

        # render the 3x3 crafting ui if its visible
        if player.otherInventoryData["showCraftingTable"]:
            image = player.inventoryRenderingData["craftingTableSurface"]
            position = player.inventoryRenderingData["craftingTableRenderPosition"]
            
            imageData = (image, position)
            renderingData.append(imageData)

        # draw a rect thingy over the hovered slot, highlights it
        if mouse.inPlayerInventory and mouse.inASlot:
            image = player.inventoryRenderingData["selectedSlotSurface"]
            slot = player.inventory[mouse.hoveredSlotId]
            position = slot["selectedSlotRenderPosition"]
            
            imageData = (image, position)
            renderingData.append(imageData)

        # highlight selected slots in crafting table
        if mouse.inASlot and mouse.inPlayerCraftingTable and player.otherInventoryData["showCraftingTable"]:
            image = player.inventoryRenderingData["selectedSlotSurface"]
            slot = player.crafting[player.crafting["gridSize"]]["slots"][mouse.hoveredSlotId]
            position = slot["selectedSlotRenderPosition"]

            imageData = (image, position)
            renderingData.append(imageData)

        # also highlight hovered slots, but only in the crafting and armor slots, if they're visible
        if mouse.inPlayerCraftingAndArmor and mouse.inASlot and player.otherInventoryData["showCraftingAndArmor"]:
            image = player.inventoryRenderingData["selectedSlotSurface"]
            slot = player.crafting[player.crafting["gridSize"]]["slots"][mouse.hoveredSlotId]
            position = slot["selectedSlotRenderPosition"]
            
            imageData = (image, position)
            renderingData.append(imageData)

        # render all the items of the base player inventory
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

        # render items in 2x2 crafting and armor, only if they're visible
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
                #whoops, no armor exists, neither do the slots
                pass
            
        # render stuff in the 3x3 crafting grid if its visible
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

        

    # run hotbar rendering
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

    # fix to selectedHotbarSlot thingy being rendered over the item counts
            
    for slotId, slot in enumerate(player.hotbar):
        if slot["count"] > 1:
            imageData = convertTextToImageData(slot["count"], slot["itemCountRenderPosition"])
            renderingData.append(imageData)


    
    # run mouse's held item rendering
    # also highlights and tells what block you're hovering over
    if not player.otherInventoryData["open"]:
        x = math.floor(mouse.cameraRelativeX / blockSize)
        z = math.floor(mouse.cameraRelativeZ / blockSize)
        x *= blockSize
        z *= blockSize
        player.canReachSelectedBlock = False

        if x < player.x + (player.horizontalBlockReach * blockSize):
            if x > player.x - (player.horizontalBlockReach * blockSize):
                if z < player.z + (player.horizontalBlockReach * blockSize):
                    if z > player.z - (player.horizontalBlockReach * blockSize):
                        player.canReachSelectedBlock = True
                        x -= camera.x
                        z -= camera.z

                        position = (x, z)

                        renderingData.append((blockHighlightSurface, position))
                        

                        # do stuff so it displays the mouse's y selection and 
                        # the block that the mouse is theoretically currently
                        # selecting
                        position = (mouse.x, mouse.y + blockSize * 1.5)

                        string = mouse.hoveredBlock["block"]["type"] + ", " + str(mouse.selectedYChange)
                        string += " blocks up/down"
                        
                        imageData = convertTextToImageData(string, position)
                        renderingData.append(imageData)
        
                        


    
    if mouse.heldItem["contents"] != "empty":
        image = itemIcons[mouse.heldItem["contents"].name]
        position = (mouse.x + 5, mouse.y + 5)
        imageData = (image, position)

        renderingData.append(imageData)

        shift = player.inventoryRenderingData["slotSize"] - 10


        if mouse.heldItem["count"] > 1:
            
            position = (mouse.x + shift, mouse.y + shift)
            imageData = convertTextToImageData(mouse.heldItem["count"], position)
            renderingData.append(imageData)

    

    # debug things
    debugRenderingStuff = "camera chunk: " + str(camera.currentChunk) + ", player chunk: " + str(player.chunkCoord)
    debugRenderingStuff += " player pos: " + str(round(player.position[0]))+ ", " + str(round(player.position[1])) + ", " + str(round(player.position[2]))
    imageData = convertTextToImageData(debugRenderingStuff, (100, 300))
    renderingData.append(imageData)

    
    screen.blits(renderingData)

    # pretty much just debug after this
    
    debugRenderingStuff2 = "player block position " + str(player.blockCoord)
    debugRenderingStuff2 += "player yv " + str(player.yv)
    debugRenderingStuff3 = "mouse pos: " + str(mouse.pos) + ", mouseRelativePos: " + str(mouse.cameraRelativePos)

    
    thing2 = font.render(debugRenderingStuff2, 0, (255, 0, 0))
    thing3 = font.render(debugRenderingStuff3, 0, (255, 0, 0))
    
    screen.blit(thing2, (100, 200))
    screen.blit(thing3, (100, 100))

    pygame.display.flip()

def doCommandStuff(commandString, previousCommandString, submitCommand):


    if previousCommandString != commandString or keysPressed[pygame.K_BACKSPACE]:

        imageData = convertTextToImageData(commandString, (30, canvasHeight - 100))
        size = font.size(commandString + "       ")
        rect = pygame.rect.Rect(30, canvasHeight - 100, size[0], size[1])
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(imageData[0], imageData[1])
        pygame.display.flip()

    if keysPressed[pygame.K_RETURN]:
        submitCommand = True

    return submitCommand

def showInvalidCommand():
    string = "invalid command"
    imageData = convertTextToImageData(string, (30, canvasHeight - 100))
    size = font.size(string)
    rect = pygame.rect.Rect(30, canvasHeight - 100, size[0], size[1])
    pygame.draw.rect(screen, (0, 0, 0), rect)
    screen.blit(imageData[0], imageData[1])
    pygame.display.flip()




showLoadingProgress("rendering initialized")


