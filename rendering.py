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





layer = 5 
"""layer will later be replaced with the player's y position"""
def render():
    global layer
    screen.fill((0, 0, 255))
    
    if keysPressed[pygame.K_PERIOD] and layer < chunkSize[1] - 1: layer += 1
    if keysPressed[pygame.K_COMMA] and layer > 0: layer -= 1

    # get the chunks to be used for rendering
    chunkList = []
    cameraChunk = camera.currentChunk
    screenExtension = 1
    for x in range(cameraChunk[0] - screenExtension, cameraChunk[0] + screenWidthInChunks + screenExtension):
        for z in range(cameraChunk[1] - screenExtension, cameraChunk[1] + screenHeightInChunks + screenExtension):
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
        for x in range(chunkSize[0]):
            for y in range(chunkSize[1]):
                for z in range(chunkSize[0]):
                    blockCoord = (x, y, z)
                    block = chunks[chunkCoord][blockCoord]

                    if block != 0:
                        xPos = x * blockSize
                        zPos = z * blockSize
                        
                        xPos += chunkCoord[0] * totalChunkSize
                        zPos += chunkCoord[1] * totalChunkSize

                        xPos -= camera.x
                        zPos -= camera.z
                        
                        
                        if layer == y:
                            position = (xPos, zPos)
                            imageData = (blockImages[block], position)


                        else:
                            factor = 1
                            divisor = 100
                            image = blockImages[block].copy()


                            # a test
                            factor += (y - layer) / divisor



                            #if y > layer:
                            #    factor += (y - layer) / divisor

                            #if y < layer:
                            #    factor -= (layer - y) / divisor
                            
                            
                            image = pygame.transform.scale_by(image, abs(factor * 1.1))
                                            # multiply by 1.1 to remove gaps in blocks            
                            
                            
                            xPos *= factor
                            zPos *= factor

                            


                            position = (xPos, zPos)
                            imageData = (image, position)
                        
                        blocks[y].append(imageData)
    blockRenderData = []
    
    for listOfBlocksIndex in range(chunkSize[1]):
        blockRenderData += blocks[listOfBlocksIndex]

     # so here's a problem:
       # when rendering anything that isn't a block, i'll probably
       # need to append it to whatever list it's layer corresponds to
    screen.blits(blockRenderData)

     # pretty much just debug after this
    screen.blit(numbers[layer], (mouse.x + 10, mouse.y))
    screen.blit(playerColor, (player.x - camera.x, player.z - camera.z))

    debugRenderingStuff = "camera chunk: " + str(camera.currentChunk) + ", player chunk: " + str(player.currentChunk)
    thing = font.render(debugRenderingStuff, 0, (255, 0, 0))
    screen.blit(thing, (400, 400))

    pygame.display.flip()