import pygame
pygame.font.init()

font = pygame.font.Font(size = 24)

screenWidth, screenHeight = 1200, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

blockSize = (30, 30) # these need to be the same number
chunkSize = (10, 6, 10) # x and z need the same
totalChunkSize = chunkSize[0] * blockSize[0]
testColor = pygame.surface.Surface((totalChunkSize, blockSize[1]))
testColor.fill((255, 255, 255))
colors = [
    0, # air
    pygame.surface.Surface((blockSize[0], blockSize[1])), # gray
    pygame.surface.Surface((blockSize[0], blockSize[1])), # lightGray
    pygame.surface.Surface((blockSize[0], blockSize[1])), # lighter gray
    pygame.surface.Surface((blockSize[0], blockSize[1])), # lighter lightgray
    pygame.surface.Surface((blockSize[0], blockSize[1])), # dark white
    pygame.surface.Surface((blockSize[0], blockSize[1])) # white
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
        print(num)
        number = font.render(str(num), 0, color)
        thing.append(number)
makeNumbers()

blockImages = [colors[0], colors[1], colors[2], colors[3], colors[4], colors[5], colors[6]]
import random as r
chunks = {
    (0, 0): {
        (0, 1, 0): 0 # currently would be air
    }
} # wow, this actually worked with a very small amount of testing

def createChunk(chunkCoords = (0, 0)):
    chunkData = {}
    for x in range(10):
        for y in range(chunkSize[1]):
            for z in range(10):
                blockData = 0
                
                blockData = y + 1
                """if y == 0: blockData = 1
                if y == 1: blockData = 2
                if y == 2: blockData = 3
                if y == 3: blockData = 4
                if y == 4: blockData = 5
                if y == 5: blockData = 6"""
                if r.randint(0, 2) == 0:
                    blockData = 0
                
                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData

def generateTest():
    #createChunk((-1, 0))
    createChunk((0, 0))
    createChunk((0, 1))
    createChunk((1, 0))
    createChunk((1, 1))
generateTest()
layer = 5
def render(keysPressed):
    global layer
    screen.fill((0, 0, 255))
    
    if keysPressed[pygame.K_PERIOD] and layer < chunkSize[1] - 1: layer += 1
    if keysPressed[pygame.K_COMMA] and layer > 0: layer -= 1
    if keysPressed[pygame.K_r]: generateTest()

    # get the chunks to be used for rendering

    chunkList = [
        #(-1, 0),
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1)
    ]
    blocks = []


    for chunkListIndex in range(len(chunkList)):
        chunkCoord = chunkList[chunkListIndex]
        for x in range(chunkSize[0]):
            for y in range(chunkSize[1]):
                for z in range(chunkSize[2]):
                    blockCoord = (x, y, z)
                    block = chunks[chunkCoord][blockCoord]

                    if block != 0:
                        xPos = x * blockSize[0]#chunkSize[0]
                        zPos = z * blockSize[1]#chunkSize[2]
                        
                        xPos += chunkCoord[0] * totalChunkSize
                        zPos += chunkCoord[1] * totalChunkSize

                        #xPos += x * (blockSize[0] - chunkSize[0])
                        #zPos += z * (blockSize[1] - chunkSize[2])
                
                        if layer == y:
                            position = (xPos, zPos)
                            imageData = (blockImages[block], position)
                        else:
                            factor = 1
                            divisor = 1
                            image = blockImages[block].copy()
                            if y > layer:
                                factor += (y - layer) / 10
                                #factor /= divisor
                                #if factor == 0:
                                #    factor = 1.1
                            if y < layer:
                                factor -= (layer - y) / 10
                                #factor /= divisor
                                #if factor == 0:
                                #    factor = 0.9
                            
                            
                            image = pygame.transform.scale_by(image, abs(factor))

                            xPos *= factor
                            zPos *= factor

                            xPos /= divisor
                            zPos /= divisor


                            position = (xPos, zPos)
                            imageData = (image, position)

                        blocks.append(imageData)
    blocks.reverse()
    screen.blits(blocks)
    screen.blit(numbers[layer], (500, 300))
    
      

    pygame.display.flip()