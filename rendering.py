from widelyUsedVariables import screenWidth, screenHeight, totalChunkSize, blockSize, chunks
from widelyUsedVariables import chunkSize, screenWidthInChunks, screenHeightInChunks
from worldgen import createChunk, findBlock, testChunk, runBlockUpdatesAfterGeneration
from widelyUsedVariables import camera
from player import player
import pygame, random

from controls import keysPressed, mouse

pygame.font.init()

font = pygame.font.Font(size = 24)
screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill((0, 0, 0))
position = (screenWidth/2, screenHeight/2)
temporaryText = font.render("generating world", 0, (255, 255, 255))
screen.blit(temporaryText, position)
pygame.display.flip()

blockImages = {
    "air": {"data": 0, "scaled": False, "data with alpha": 0}
}

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
        #if hasAlpha:
        #    borderColor = (red, green, blue, alphaValue)
        #else:
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
        "data with alpha": block,
        "alpha'd": False
    }

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

numbers = []
def makeNumbers(thing = numbers, color = (200, 200, 200)):
    for num in range(10):
        number = font.render(str(num), 0, color)
        thing.append(number)
    minus = font.render("-", 0, (255, 0, 0))
    thing.append(minus)
makeNumbers()

def generateSpawnArea():
    chunkList = []
    cameraChunk = camera.currentChunk
    screenExtension = 1

    xRange = cameraChunk[0] - screenExtension
    maxXRange = cameraChunk[0] + screenWidthInChunks + screenExtension
    zRange = cameraChunk[1] - screenExtension
    maxZRange = cameraChunk[1] + screenHeightInChunks + screenExtension

    # make sure all the chunks plus a lil bit actually exist
    for x in range(xRange - 1, maxXRange + 2):
        for z in range(zRange - 1, maxZRange + 2):
            try:
                chunks[(x, z)]
            except:
                createChunk((x, z))

    for x in range(xRange, maxXRange + 1):
        for z in range(zRange, maxZRange + 1):
            chunkList.append((x, z))
            if not chunks[(x, z)]["blocksUpdated"]:
                runBlockUpdatesAfterGeneration((x, z))
    





def render(deltaTime):


    screen.fill((0, 0, 0))

    # get the chunks to be used for rendering
    chunkList = []
    cameraChunk = camera.currentChunk
    screenExtension = 1

    xRange = cameraChunk[0] - screenExtension
    maxXRange = cameraChunk[0] + screenWidthInChunks + screenExtension
    zRange = cameraChunk[1] - screenExtension
    maxZRange = cameraChunk[1] + screenHeightInChunks + screenExtension

    # make sure all the chunks plus a lil bit actually exist
    for x in range(xRange - 1, maxXRange + 2):
        for z in range(zRange - 1, maxZRange + 2):
            try:
                chunks[(x, z)]
            except:
                createChunk((x, z))

    for x in range(xRange, maxXRange + 1):
        for z in range(zRange, maxZRange + 1):
            chunkList.append((x, z))
            if not chunks[(x, z)]["blocksUpdated"]:
                runBlockUpdatesAfterGeneration((x, z))



    # need to separate which layers of the blocks get rendered at once, so
    # the lower layers are below the higher ones
    blocks = []
    for i in range(chunkSize[1]):
        blocks.append( [] )

    for chunkListIndex in range(len(chunkList)):
        chunkCoord = chunkList[chunkListIndex]
        for y in range(chunkSize[1]):
            def isBlock(xPos, yPos, zPos):
                chunkCoordForThis = [chunkCoord[0], chunkCoord[1]]
                x = xPos
                y = yPos
                z = zPos

                if y >= chunkSize[1]:
                    y = chunkSize[1] - 1
                elif y < 0:
                    y = 0

                if x < 0:
                    x += chunkSize[0]
                    chunkCoordForThis[0] -= 1
                elif x >= chunkSize[0]:
                    x -= chunkSize[0]
                    chunkCoordForThis[0] += 1

                if z < 0:
                    z += chunkSize[0]
                    chunkCoordForThis[1] -= 1
                elif z >= chunkSize[0]:
                    z -= chunkSize[0]
                    chunkCoordForThis[1] += 1
                
                newChunkCoord = (chunkCoordForThis[0], chunkCoordForThis[1])
                block = chunks[newChunkCoord][(x, y, z)]
                
                if block["type"] != "air":
                    return True
        
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
                thing /= (divisor)
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
                        
                        if block["noBlockBelow"]:
                            if xPos - (5*blockSize) < player.x and xPos + (5*blockSize) > player.x:
                                if zPos - (5*blockSize) < player.z and zPos + (5*blockSize) > player.z:
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
                                image.set_alpha(150)
                                scaledImages[block["type"]]["alpha'd"] = True
                                scaledImages[block["type"]]["data with alpha"] = image
                            else:
                                image = scaledImages[block["type"]]["data with alpha"]
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
    playerAddedToRendering = False
    for listOfBlocksIndex in range(chunkSize[1]):

        if not playerAddedToRendering:
            if player.blockCoord[1] == listOfBlocksIndex:
                playerAddedToRendering = True
                blocks[listOfBlocksIndex].append(player.imageData)

        renderingData += blocks[listOfBlocksIndex]

    if not playerAddedToRendering:
        renderingData.append(player.imageData)
        


    
    screen.blits(renderingData)

     # pretty much just debug after this

    debugRenderingStuff = "camera chunk: " + str(camera.currentChunk) + ", player chunk: " + str(player.chunkCoord)
    debugRenderingStuff += " player pos: " + str(round(player.position[0]))+ ", " + str(round(player.position[1])) + ", " + str(round(player.position[2]))
    debugRenderingStuff2 = "player block position " + str(player.blockCoord)
    debugRenderingStuff2 += "player yv " + str(player.yv)
    thing = font.render(debugRenderingStuff, 0, (255, 0, 0))
    thing2 = font.render(debugRenderingStuff2, 0, (255, 0, 0))
    screen.blit(thing, (100, 300))
    screen.blit(thing2, (100, 200))

    pygame.display.flip()