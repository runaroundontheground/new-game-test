import pygame
pygame.font.init()

font = pygame.font.Font(size = 24)

screenWidth, screenHeight = 600, 400
screen = pygame.display.set_mode((screenWidth, screenHeight))

blockSize = (30, 30) # these need to be the same number
heightLimit = 6
chunkSize = (10, heightLimit, 10) # x and z need the same
totalChunkSize = chunkSize[0] * blockSize[0]

colors = [
    0, # air
    pygame.surface.Surface((blockSize[0], blockSize[1])), # gray
    pygame.surface.Surface((blockSize[0], blockSize[1])), # lightGray
    pygame.surface.Surface((blockSize[0], blockSize[1])), # white
    pygame.surface.Surface((blockSize[0], blockSize[1])), # green
    pygame.surface.Surface((blockSize[0], blockSize[1])), # red
    pygame.surface.Surface((blockSize[0], blockSize[1])) # brown
]
def fillColor(colorNum, colorValue):
    colors[colorNum].fill(colorValue)
    #colors[colorNum] = colors[colorNum].convert_alpha()
fillColor(1, (50, 50, 50))
fillColor(2, (100, 100, 100))
fillColor(3, (255, 255, 255))
fillColor(4, (0, 255, 0))
fillColor(5, (255, 0, 0))
fillColor(6, (200, 75, 0))
numbers = []
purpleNumbers = []
def makeNumbers(thing = numbers, color = (200, 200, 200)):
    for num in range(10):
        print(num)
        number = font.render(str(num), 0, color)
        thing.append(number)
makeNumbers()
makeNumbers(purpleNumbers, (128, 0, 128))
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
        for y in range(heightLimit):
            for z in range(10):
                blockData = 0
                

                if y == 0: blockData = 1
                if y == 1: blockData = 2
                if y == 2: blockData = 3
                if y == 3: blockData = 4
                if y == 4: blockData = 5
                if y == 5: blockData = 6
                if r.randint(0, 2) == 0:
                    blockData = 0
                
                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData

def generateTest():
    createChunk((0, 0))
    createChunk((0, 1))
    createChunk((1, 0))
    createChunk((1, 1))
generateTest()
layer = 0
def render(keysPressed):
    global layer
    screen.fill((0, 0, 255))
    
    if keysPressed[pygame.K_PERIOD] and layer < heightLimit - 1: layer += 1
    if keysPressed[pygame.K_COMMA] and layer > 0: layer -= 1
    if keysPressed[pygame.K_r]: generateTest()

    # get the chunks to be used for rendering

    chunkList = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1)
    ]
    blocks = []


    for chunkListIndex in range(len(chunkList)):
        chunkCoord = chunkList[chunkListIndex]
        for x in range(10):
            for y in range(heightLimit):
                for z in range(10):
                    blockCoord = (x, y, z)
                    block = chunks[chunkCoord][blockCoord]

                    if block != 0:

                        if y < heightLimit - 1:
                            if chunks[chunkCoord][(x, y + 1, z)] != 0:# or y == heightLimit:

                                if layer == y:
                                    xPos = blockCoord[0] * chunkSize[0]
                                    zPos = blockCoord[2] * chunkSize[2]
                                    
                                    xPos += chunkCoord[0] * totalChunkSize
                                    zPos += chunkCoord[1] * totalChunkSize

                                    position = (xPos, zPos)
                                    image = blockImages[block].copy()
                                    image.blit(numbers[y], (0, 0))
                                    imageData = (image, position)
                                else:
                                    factor = 1
                                    positionFactor = 1
                                    image = blockImages[block].copy()
                                    if y > layer:
                                        factor += (y - layer) / 10
                                        positionFactor += (y - layer) / 500
                                    if y < layer:
                                        factor -= (layer - y) / 10
                                        positionFactor -= (layer - y) / 500
                                    
                                    image = pygame.transform.scale_by(image, abs(factor))
                                    image.blit(numbers[y], (0, 0))
                                    xPos = x * blockSize[0]
                                    zPos = z * blockSize[1]
                                    position = (xPos, zPos)
                                    imageData = (image, position)

                                blocks.append(imageData)
    
    screen.blits(blocks)
    screen.blit(numbers[layer], (400, 300))
    
      

    pygame.display.flip()