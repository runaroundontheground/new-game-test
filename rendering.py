from globalVariables import screenWidth, screenHeight, totalChunkSize, blockSize, chunks
from globalVariables import chunkSize, screenWidthInChunks, screenHeightInChunks, entities
from globalVariables import itemEntitySize, camera, itemIcons, font, rotatePoint, typingCommands
from worldgen import generateChunkTerrain, runBlockUpdatesAfterGeneration
from worldgen import generateChunkStructures, findBlock
from controls import mouse
from player import player
import pygame, math

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))



screen.fill((0, 0, 0))
position = (screenWidth/3, screenHeight/2)
temporaryText = font.render("generating world", 0, (255, 255, 255))
screen.blit(temporaryText, position)
pygame.display.flip()

blockImages = {
    "air": {"data": 0, "scaled": False, "dataWithAlpha": 0}
}
itemEntityIcons = {}

blockHighlightSurface = pygame.Surface((blockSize, blockSize))
blockHighlightSurface.fill((255, 255, 150)) # yellow?

rect = pygame.Rect(5, 5, blockSize - 10, blockSize - 10)
blockHighlightSurface.fill((255, 255, 255), rect)
blockHighlightSurface.set_colorkey((255, 255, 255))


itemIconSize = player.inventoryRenderingData["slotSize"] - player.inventoryRenderingData["itemIconShift"] * 2



baseToolSurface = pygame.Surface((itemIconSize, itemIconSize)) # a wooden stick
baseToolSurface.fill((255, 255, 255))
baseToolSurface.set_colorkey((255, 255, 255))
line = pygame.draw.line(baseToolSurface, (150, 75, 0), (0, itemIconSize), (itemIconSize - 5, 5), 3)

uneditedTools = {
"pickaxe": baseToolSurface.copy(),
"axe": baseToolSurface.copy(),
"shovel": baseToolSurface.copy()
}


pickaxeHead = pygame.Surface((itemIconSize, itemIconSize))
rect = pygame.Rect(itemIconSize/2 - (itemIconSize/2)/2, itemIconSize/2 - (5)/2, itemIconSize, itemIconSize/10)
pickaxeHead.fill((51, 52, 53), rect)
rotatedImage, rect = rotatePoint(pickaxeHead, 45, [itemIconSize/2, itemIconSize/2], pygame.math.Vector2([-7, -10]))
rotatedImage.set_colorkey((255, 255, 255))
rotatedImage.set_colorkey((0, 0, 0))
uneditedTools["pickaxe"].blit(rotatedImage, rect)

axeHead = pygame.Surface((itemIconSize/2, itemIconSize/2))
rect = pygame.Rect(0, 5, (itemIconSize/3), (itemIconSize/3))
axeHead.fill((255, 255, 255)); axeHead.set_colorkey((255, 255, 255))
axeHead.fill((51, 52, 53), rect)
rect = pygame.Rect((itemIconSize/3), 0, (itemIconSize/3), itemIconSize/3)
axeHead.fill((51, 52, 53), rect)



def addAToolIcon(toolName, toolType, toolHeadColor = (100, 100, 100)):
    
    toolIcon = uneditedTools[toolType].copy()

    for x in range(math.floor(itemIconSize)):
        for y in range(math.floor(itemIconSize)):
            color = pygame.Surface.get_at(toolIcon, (x, y))
            c, d, e, hasAlpha = False, False, False, False
            r, g, b = color[0], color[1], color[2]

            if len(color) >= 4:
                hasAlpha = True
            if r - 5 < 51 and r + 5 > 51:
                c = True
            if g - 5 < 52 and g + 5 > 52:
                d = True
            if b - 5 < 53 and b + 5 > 53:
                e = True
            
            if (c or d or e) and not hasAlpha:
                pygame.Surface.set_at(toolIcon, (x, y), toolHeadColor)

    
    itemIcons[toolName] = toolIcon

    itemEntityIcon = toolIcon.copy()
    scale = itemEntitySize / blockSize

    itemEntityIcon = pygame.transform.scale_by(itemEntityIcon, scale)
    itemEntityIcons[toolName] = itemEntityIcon

addAToolIcon("stone pickaxe", "pickaxe", (200, 200, 200))
addAToolIcon("stone axe", "axe", (200, 200, 200))
#addAToolIcon("stone shovel", "shovel", (200, 200, 200))

def addABlock(blockName, blockColor, blockBorderColor = "unassigned",
              hasAlpha = False, alphaValue = 0):
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
        "dataWithAlpha": block,
        "alpha'd": False
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
addABlock("snowy dirt", (220, 220, 220), (150, 75, 0))
addABlock("snowy stone", (220, 220, 220), (125, 125, 125))
addABlock("sand", (232, 228, 118))
addABlock("clay", (196, 152, 94))
addABlock("gravel", (150, 150, 150))
addABlock("water", (0, 0, 255), (0, 0, 255), True, 100)
addABlock("bedrock", (0, 255, 255))
addABlock("log", (110, 79, 38), (110, 79, 38))
addABlock("leaves", (29, 64, 17))




characters = {}

defaultTextColor = (255, 255, 255)
def addACharacter(character):
    characters[character] = {
        "text": font.render(character, 0, defaultTextColor),
        "size": font.size(character)
    }
def addMostCharacters():
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    ]
    otherChars = [
             ".", "-", "_", ",", "<", ">", "/", "?", ":", ";", "'", '"', " ",
             "(", ")", "[", "]", "{", "}", "+", "="
    ]

    for numericalCharacter in range(10):
        addACharacter(str(numericalCharacter))

    for letter in letters:
        characters[letter] = {
            "text": font.render(letter, 0, defaultTextColor),
            "size": font.size(letter)
        }
        characters[letter.upper()] = {
            "text": font.render(letter.upper(), 0, defaultTextColor),
            "size": font.size(letter.upper())
        }
    for character in otherChars:
        characters[character] = {
            "text": font.render(character, 0, defaultTextColor),
            "size": font.size(character)
        }
addMostCharacters()

def convertTextToImageData(textValue, position, centeredOnPosition = False,):
    text = str(textValue)

    x = 0
    y = 0
    
    for character in text:
        size = characters[character]["size"]
        x += size[0]
        if size[1] > y:
            y = size[1]

    temporarySurface = pygame.Surface((x, y))
    temporarySurface.fill((0, 0, 0))
    temporarySurface.set_colorkey((0, 0, 0))
    
    if centeredOnPosition:
        for character in text:
            pass
    else:
        x = 0
        for character in text:
            renderedText = characters[character]["text"]
            temporarySurface.blit(renderedText, (x, 0))

            x += characters[character]["size"][0]
        imageData = (temporarySurface, position)
        
        return imageData
        

def generateNearbyAreas(rangeOfGeneration = 2, returnChunkList = False):
    chunkList = []
    cameraChunk = camera.currentChunk
    screenExtension = 1

    xRange = cameraChunk[0] - screenExtension
    maxXRange = cameraChunk[0] + screenWidthInChunks + screenExtension + 1
    zRange = cameraChunk[1] - screenExtension
    maxZRange = cameraChunk[1] + screenHeightInChunks + screenExtension + 1

    # initial generation in a larger area
    for x in range(xRange - rangeOfGeneration, maxXRange + rangeOfGeneration):
        for z in range(zRange - rangeOfGeneration, maxZRange + rangeOfGeneration):
            try:
                chunks[(x, z)]
            except:
                generateChunkTerrain((x, z))

    # generate structures
    for x in range(xRange - (rangeOfGeneration - 1), maxXRange + (rangeOfGeneration - 1)):
        for z in range(zRange - (rangeOfGeneration - 1), maxZRange + (rangeOfGeneration - 1)):
            try:
                chunks[(x, z)]
            except:
                generateChunkTerrain((x, z))
            else:
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
    generateNearbyAreas(rangeOfGeneration = 3)
    





def render(deltaTime):


    screen.fill((0, 0, 0))

    # get the chunks to be used for rendering
    chunkList = generateNearbyAreas(2, True)


    # separate the blocks into layers, so they get rendered in the right order
    # also, keep track of the scale for each y layer
    blocks = []
    positionAndScaleFactors = []
    for i in range(chunkSize[1]):
        blocks.append( [] )
        positionAndScaleFactors.append( [] )

    
    

    for chunkCoord in chunkList:
        for y in range(chunkSize[1]):
            
        
            # scale images outside of x/z loop, better performance
            
            posFactor = 1
            sizeFactor = 1
            divisor = 50
            # scale smoother when using exact position rather than player's block coord
            playerYInBlocks = player.y / blockSize
            thing2 = y - playerYInBlocks
            posFactor += thing2 / divisor


            divisor *= 2

            if y > playerYInBlocks:
                thing = y - playerYInBlocks
                thing /= (divisor / 1.1)
                sizeFactor += thing

            if y < playerYInBlocks:
                thing = playerYInBlocks - y
                thing /= (divisor * 2)
                sizeFactor -= thing
                

            if sizeFactor < 0.1:
                sizeFactor = 0.1
            
            positionAndScaleFactors[y] = posFactor

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
                        
                        if block["alphaValue"] != 0:
                            if player.blockCoord[1] <= y:
                                fiveBlocks = 5 * blockSize
                                if xPos - fiveBlocks < player.x and xPos + fiveBlocks > player.x:
                                    if zPos - fiveBlocks < player.z and zPos + fiveBlocks > player.z:
                                        thisBlockHasAlpha = True
                                    

                        
                        xPos -= player.x
                        zPos -= player.z
                        
                        if not scaledImages[block["type"]]["scaled"]: # image has not been scaled
                            if sizeFactor != 1:

                                newImageData = scaledImages[block["type"]]["data"]
                                newImageData = pygame.transform.scale_by(newImageData, sizeFactor)
                                scaledImages[block["type"]]["data"] = newImageData
                                
                            scaledImages[block["type"]]["scaled"] = True

                        if thisBlockHasAlpha:

                            if not scaledImages[block["type"]]["alpha'd"]:
                                image = scaledImages[block["type"]]["data"].copy()
                                image.set_alpha(block["alphaValue"])
                                scaledImages[block["type"]]["alpha'd"] = True
                                scaledImages[block["type"]]["dataWithAlpha"] = image
                            else:
                                image = scaledImages[block["type"]]["dataWithAlpha"]
                        else:
                            image = scaledImages[block["type"]]["data"]

                        
                        

                        xPos *= posFactor
                        zPos *= posFactor
                        
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
        image = player.inventoryRenderingData["inventorySurface"]
        position = player.inventoryRenderingData["inventoryRenderPosition"]
        imageData = (image, position)

        renderingData.append(imageData)

        if mouse.inPlayerInventory and mouse.inASlot:
                image = player.inventoryRenderingData["selectedSlotSurface"]
                slot = player.inventory[mouse.hoveredSlotId]
                position = slot["selectedSlotRenderPosition"]
                
                imageData = (image, position)
                renderingData.append(imageData)

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

            if slot["count"] > 1:
                imageData = convertTextToImageData(slot["count"], slot["itemCountRenderPosition"])
                renderingData.append(imageData)


    
    # run mouse's held item rendering
    # also figure out selecting a block in the world, highlighting it, ect
    if not player.otherInventoryData["open"]:
        x = math.floor(mouse.cameraRelativeX / blockSize)
        z = math.floor(mouse.cameraRelativeZ / blockSize)
        x *= blockSize
        z *= blockSize

        if x < player.x + (player.horizontalBlockReach * blockSize):
            if x > player.x - (player.horizontalBlockReach * blockSize):
                if z < player.z + (player.horizontalBlockReach * blockSize):
                    if z > player.z - (player.horizontalBlockReach * blockSize):
                        x -= camera.x
                        z -= camera.z

                        position = (x, z)

                        renderingData.append((blockHighlightSurface, position))

                        # do stuff so it displays the mouse's y selection and 
                        # the block that the mouse is theoretically currently
                        # selecting
                        position = (mouse.x, mouse.y + blockSize * 1.5)
                        
                        imageData = convertTextToImageData(mouse.hoveredBlock["block"]["type"], position)
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


    
    imageData = (axeHead, (400, 250))
    renderingData.append(imageData)
    

    # debug things
    debugRenderingStuff = "camera chunk: " + str(camera.currentChunk) + ", player chunk: " + str(player.chunkCoord)
    debugRenderingStuff += " player pos: " + str(round(player.position[0]))+ ", " + str(round(player.position[1])) + ", " + str(round(player.position[2]))
    imageData = convertTextToImageData(debugRenderingStuff, (100, 300))
    renderingData.append(imageData)


    screen.blits(renderingData)

     # pretty much just debug after this

    if typingCommands:
        pass

    
    debugRenderingStuff2 = "player block position " + str(player.blockCoord)
    debugRenderingStuff2 += "player yv " + str(player.yv)
    debugRenderingStuff3 = "mouse pos: " + str(mouse.pos) + ", mouseRelativePos: " + str(mouse.cameraRelativePos)
    
    thing2 = font.render(debugRenderingStuff2, 0, (255, 0, 0))
    thing3 = font.render(debugRenderingStuff3, 0, (255, 0, 0))
    
    screen.blit(thing2, (100, 200))
    screen.blit(thing3, (100, 100))

    pygame.display.flip()
