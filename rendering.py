from widelyUsedVariables import screenWidth, screenHeight, totalChunkSize, blockSize, chunks
from widelyUsedVariables import chunkSize, screenWidthInChunks, screenHeightInChunks
from widelyUsedVariables import camera
from worldgen import createChunk
from player import player
import pygame

from controls import keysPressed, mouse

pygame.font.init()

font = pygame.font.Font(size = 24)




screen = pygame.display.set_mode((screenWidth, screenHeight))

playerColor = pygame.surface.Surface((30, 30))
playerColor.fill((0, 255, 0))
colors = [
    0, # air
    pygame.surface.Surface((blockSize, blockSize)), # gray
    pygame.surface.Surface((blockSize, blockSize)), # lightGray
    pygame.surface.Surface((blockSize, blockSize)), # lighter gray
    pygame.surface.Surface((blockSize, blockSize)), # lighter lightgray
    pygame.surface.Surface((blockSize, blockSize)), # dark white
    pygame.surface.Surface((blockSize, blockSize)) # white
]
def fillColor(colorNum, colorValue):
    colors[colorNum].fill(colorValue)
    
fillColor(1, (0, 0, 0))
fillColor(2, (50, 50, 50))
fillColor(3, (100, 100, 100))
fillColor(4, (150, 150, 150))
fillColor(5, (200, 200, 200))
fillColor(6, (255, 255, 255))
numbers = []
def makeNumbers(thing = numbers, color = (200, 200, 200)):
    for num in range(10):
        number = font.render(str(num), 0, color)
        thing.append(number)
    minus = font.render("-", 0, (255, 0, 0))
    thing.append(minus)
makeNumbers()

blockImages = [colors[0], colors[1], colors[2], colors[3], colors[4], colors[5], colors[6]]






def render():


    screen.fill((0, 0, 255))

    # get the chunks to be used for rendering
    chunkList = []
    cameraChunk = camera.currentChunk
    screenExtension = 1
    for x in range(cameraChunk[0] - screenExtension, cameraChunk[0] + screenWidthInChunks + screenExtension + 1):
        for z in range(cameraChunk[1] - screenExtension, cameraChunk[1] + screenHeightInChunks + screenExtension + 1):
            try:
                chunks[(x, z)]
            except:
                createChunk((x, z))
            else:
                chunkList.append((x, z))



    # need to separate which layers of the blocks get rendered at once, so
    # the lower layers are below the higher ones
    blocks = []
    for i in range(chunkSize[1]):
        blocks.append( [] )

    for chunkListIndex in range(len(chunkList)):
        chunkCoord = chunkList[chunkListIndex]
        for y in range(chunkSize[1]):

        
             # scale everything besides position outside of the x and z loops
             # this runs soooo much faster than it does without it
            posFactor = 1
            sizeFactor = 1
            divisor = 75 # normally 100
             # scale smoother when using exact position rather than player's block coord
            thing = player.y / blockSize
            sizeFactor += (y - thing) / divisor
            posFactor = sizeFactor

            scaledImages = blockImages.copy()

            for item in scaledImages:
                
                image = item
                
                if image != 0:
                    image = pygame.transform.scale_by(image, abs(sizeFactor))

            for x in range(chunkSize[0]):
                for z in range(chunkSize[0]):

                    block = chunks[chunkCoord][(x, y, z)]

                    if block != 0:
                        xPos = x * blockSize
                        zPos = z * blockSize
                        
                        xPos += chunkCoord[0] * totalChunkSize
                        zPos += chunkCoord[1] * totalChunkSize
                        """
                        when the camera x and z were subtracted from xpos and zpos
                        BEFORE scaling, the scaling was centered around the camera
                        if the subtraction happens AFTER scaling, the scaling is centered
                        around the middle ( x = 0, z = 0)
                        subtracting the player pos before scaling, then adding it back
                        after scaling fixed the problem!!!
                        that was hard to fix
                        now i gotta do performance fixes
                        """

                        
                        xPos -= player.x
                        zPos -= player.z
                        
                        image = scaledImages[block]

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

    #if not playerAddedToRendering:
    #    renderingData.append(player.imageData)
        


    
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