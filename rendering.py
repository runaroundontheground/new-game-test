from widelyUsedVariables import screenWidth, screenHeight, totalChunkSize, blockSize, chunks
from widelyUsedVariables import chunkSize, screenWidthInChunks, screenHeightInChunks
from worldgen import generateChunkTerrain, runBlockUpdatesAfterGeneration
from worldgen import generateChunkStructures, getBlockCoord
from widelyUsedVariables import camera, itemIcons
from controls import mouse
from player import player
import pygame, math

pygame.font.init()

font = pygame.font.Font(size = 24)
screen = pygame.display.set_mode((screenWidth, screenHeight))



screen.fill((0, 0, 0))
position = (screenWidth/3, screenHeight/2)
temporaryText = font.render("generating world", 0, (255, 255, 255))
screen.blit(temporaryText, position)
pygame.display.flip()

blockImages = {
    "air": {"data": 0, "scaled": False, "dataWithAlpha": 0}
}

validBlockSelectorSurface = pygame.Surface((blockSize, blockSize))
invalidBlockSelectorSurface = validBlockSelectorSurface.copy()
rect = pygame.Rect(blockSize + 5, blockSize + 5, blockSize - 10, blockSize - 10)
validBlockSelectorSurface.fill((0, 255, 0))
validBlockSelectorSurface.fill((255, 255, 255), rect)
validBlockSelectorSurface.set_colorkey((255, 255, 255))

invalidBlockSelectorSurface.fill((255, 0, 0))
invalidBlockSelectorSurface.fill((255, 255, 255), rect)
invalidBlockSelectorSurface.set_colorkey((255, 255, 255))


def addAnItemIcon():
    pass

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

    slotSize = player.otherInventoryData["slotSize"]
    blockIcon = block.copy()
    # definitely a very short variable name lol
    targetSize = slotSize - player.otherInventoryData["itemIconShift"] * 2

    scale = abs(targetSize / blockSize)

    blockIcon = pygame.transform.scale_by(blockIcon, scale)

    itemIcons[blockName] = blockIcon

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

def convertTextToStrAndRender(textValue, position, centeredOnPosition = False,
                              renderingData = []):
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
        
        renderingData.append(imageData)
        

def generateNearbyAreas(rangeOfGeneration = 1, returnChunkList = False):
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
    for x in range(xRange, maxXRange):
        for z in range(xRange, maxXRange):
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
    # that might cause some lag...
    





def render(deltaTime):


    screen.fill((0, 0, 0))

    # get the chunks to be used for rendering
    chunkList = generateNearbyAreas(2, True)


    # need to separate which layers of the blocks get rendered at once, so
    # the lower layers are below the higher ones
    blocks = []
    for i in range(chunkSize[1]):
        blocks.append( [] )

    

    for chunkCoord in chunkList:
        for y in range(chunkSize[1]):
            
        
            # scale everything besides position outside of the x and z loops
            # it runs faster that way
            
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
            


            scaledImages = blockImages.copy()
            

            for x in range(chunkSize[0]):
                for z in range(chunkSize[0]):

                    block = chunks[chunkCoord]["data"][(x, y, z)]
                    
                    if block["render"]:
                        xPos = x * blockSize
                        zPos = z * blockSize
                        
                        xPos += chunkCoord[0] * totalChunkSize
                        zPos += chunkCoord[1] * totalChunkSize

                        thisBlockHasAlpha = False
                        
                        if block["usesAlpha"]:
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

    # do special player things for rendering
    # inventory, player itself, whatever
    playerAddedToRendering = False
    for listOfBlocksIndex in range(chunkSize[1]):

        if not playerAddedToRendering:
            if player.blockCoord[1] == listOfBlocksIndex:
                playerAddedToRendering = True
                blocks[listOfBlocksIndex].append(player.imageData)

        renderingData += blocks[listOfBlocksIndex]

    if not playerAddedToRendering:
        renderingData.append(player.imageData)

    image = player.otherInventoryData["hotbarSurface"]
    position = player.otherInventoryData["hotbarRenderPosition"]
    imageData = (image, position)
    renderingData.append(imageData)
        
    # run inventory rendering and mouse interaction
    if player.otherInventoryData["open"]:
        image = player.otherInventoryData["inventorySurface"]
        position = player.otherInventoryData["inventoryRenderPosition"]
        imageData = (image, position)

        renderingData.append(imageData)
        

        mouseInInventory = player.otherInventoryData["inventoryRect"].collidepoint(mouse.x, mouse.y)
        mouseInHotbar = player.otherInventoryData["hotbarRect"].collidepoint(mouse.x, mouse.y)

        for slotId, slot in enumerate(player.inventory):
            item = slot["contents"]

            if mouseInInventory:
                
                if slot["rect"].collidepoint(mouse.x, mouse.y):
                    position = slot["selectedSlotRenderPosition"]
                    image = player.otherInventoryData["selectedSlotSurface"]
                    imageData = (image, position)

                    renderingData.append(imageData)
                    # interaction for moving around items and stuff
                    if mouse.buttons["pressed"]["left"]:
                        playerItem = player.inventory[slotId]["contents"]
                        playerItemCount = player.inventory[slotId]["count"]
                        player.inventory[slotId]["contents"] = mouse.heldItem["contents"]
                        player.inventory[slotId]["count"] = mouse.heldItem["count"]
                        mouse.heldItem["contents"] = playerItem
                        mouse.heldItem["count"] = playerItemCount
            
            if item != "empty":
                
                image = itemIcons[item.name]
                position = slot["renderPosition"]
                imageData = (image, position)

                renderingData.append(imageData)
        for slotId, slot in enumerate(player.hotbar):

            if mouseInHotbar:
                if slot["rect"].collidepoint(mouse.x, mouse.y):
                    position = slot["selectedSlotRenderPosition"]
                    image = player.otherInventoryData["selectedSlotSurface"]
                    imageData = (image, position)

                    renderingData.append(imageData)

                    if mouse.buttons["pressed"]["left"]:
                        playerItem = player.hotbar[slotId]["contents"]
                        playerItemCount = player.hotbar[slotId]["count"]
                        player.hotbar[slotId]["contents"] = mouse.heldItem["contents"]
                        player.hotbar[slotId]["count"] = mouse.heldItem["count"]
                        mouse.heldItem["contents"] = playerItem
                        mouse.heldItem["count"] = playerItemCount

    # run hotbar rendering
    for index, slot in enumerate(player.hotbar):
        item = slot["contents"]
        currentHotbarSlot = player.otherInventoryData["currentHotbarSlotSelected"]
        
        if index == currentHotbarSlot:
            image = player.otherInventoryData["selectedSlotSurface"]
            position = slot["selectedSlotRenderPosition"]
            imageData = (image, position)

            renderingData.append(imageData)

        if item != "empty":
            image = itemIcons[item.name]
            position = slot["renderPosition"]
            imageData = (image, position)

            renderingData.append(imageData)
    
    # run mouse's held item rendering
    # also figure out selecting a block in the world, highlighting it, ect
    if not player.otherInventoryData["open"]:
        # make stuff actually render over a block
        x = math.floor(mouse.cameraRelativeX / blockSize)
        z = math.floor(mouse.cameraRelativeZ / blockSize)
        x *= blockSize
        z *= blockSize

        if x < player.x + player.horizontalBlockReach * blockSize:
            pass
        # make checks so that it only renders the selection if it's within the player's
        # interaction range
        x -= camera.x
        z -= camera.z

        position = (x, z)

        renderingData.append((validBlockSelectorSurface, position))



    
    if mouse.heldItem["contents"] != "empty":
        image = itemIcons[mouse.heldItem["contents"].name]
        position = (mouse.x + 5, mouse.y + 5)
        imageData = (image, position)

        renderingData.append(imageData)
    

    # debug things
    debugRenderingStuff = "camera chunk: " + str(camera.currentChunk) + ", player chunk: " + str(player.chunkCoord)
    debugRenderingStuff += " player pos: " + str(round(player.position[0]))+ ", " + str(round(player.position[1])) + ", " + str(round(player.position[2]))
    convertTextToStrAndRender(debugRenderingStuff, (100, 300), renderingData = renderingData)

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