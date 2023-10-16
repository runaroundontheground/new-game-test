from widelyUsedVariables import screenWidth, screenHeight, totalChunkSize, blockSize, chunks
from widelyUsedVariables import chunkSize, screenWidthInChunks, screenHeightInChunks
from widelyUsedVariables import camera
from worldgen import createChunk, findBlock
from player import player
import pygame

from controls import keysPressed, mouse

pygame.font.init()

font = pygame.font.Font(size = 24)
screen = pygame.display.set_mode((screenWidth, screenHeight))

imageSize = (blockSize, blockSize)
baseSurface = pygame.surface.Surface(imageSize)
fillingRect = pygame.rect.Rect(1, 1, blockSize - 2, blockSize - 2)
grassBase = baseSurface.copy()
grassBase.fill((150, 75, 0))
dirtBase = baseSurface.copy()
dirtBase.fill((130, 45, 0))
stoneBase = baseSurface.copy()
stoneBase.fill((50, 50, 50))

blockImages = {
    "air": [0, 0],
    "grass": [grassBase, False],
    "dirt": [dirtBase, False],
    "stone": [stoneBase, False]
    
}
blockImages["grass"][0].fill((0, 255, 0), fillingRect)
blockImages["dirt"][0].fill((150, 75, 0), fillingRect)
blockImages["stone"][0].fill((75, 75, 75), fillingRect)

numbers = []
def makeNumbers(thing = numbers, color = (200, 200, 200)):
    for num in range(10):
        number = font.render(str(num), 0, color)
        thing.append(number)
    minus = font.render("-", 0, (255, 0, 0))
    thing.append(minus)
makeNumbers()







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
            def isBlock(x, y, z):
                xPos = x + (chunkSize[0] * chunkCoord[0])
                zPos = z + (chunkSize[0] * chunkCoord[1])

                xPos *= blockSize
                yPos = y * blockSize
                zPos *= blockSize
                return findBlock(xPos, yPos, zPos)
        
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
            

            for x in range(chunkSize[0]):
                for z in range(chunkSize[0]):

                    block = chunks[chunkCoord][(x, y, z)]

                    if block != "air":
                        

                    

                        xPos = x * blockSize
                        zPos = z * blockSize
                        
                        xPos += chunkCoord[0] * totalChunkSize
                        zPos += chunkCoord[1] * totalChunkSize

                        
                        xPos -= player.x
                        zPos -= player.z
                        
                        if not scaledImages[block][1]: # image has not been scaled
                            scaledImages[block][0] = pygame.transform.scale_by(scaledImages[block][0], abs(sizeFactor * 1.1))
                            scaledImages[block][1] = True
                        
                        image = scaledImages[block][0]

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