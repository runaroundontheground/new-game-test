import pygame
pygame.font.init()

font = pygame.font.Font(size = 24)

screenWidth, screenHeight = 600, 400
screen = pygame.display.set_mode((screenWidth, screenHeight))

blockSize = (30, 30)
heightLimit = 6
chunkSize = (10, heightLimit, 10)

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
    colors[colorNum] = colors[colorNum].convert_alpha()
fillColor(1, (50, 50, 50))
fillColor(2, (100, 100, 100))
fillColor(3, (255, 255, 255))
fillColor(4, (0, 255, 0))
fillColor(5, (255, 0, 0))
fillColor(6, (200, 75, 0, 200))
numbers = []
print(colors[0])
def makeNumbers():
    for num in range(10):
        print(num)
        number = font.render(str(num), 0, (200, 200, 200))
        numbers.append(number)
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
        for y in range(heightLimit):
            for z in range(10):
                chunkCoord = chunkCoords
                blockCoord = (x,y,z)
                blockData = 0
                

                if y == 0: blockData = 1
                if y == 1: blockData = 2
                if y == 2: blockData = 3
                if y == 3: blockData = 4
                if y == 4: blockData = 5
                if y == 5: blockData = 6
                if r.randint(0, int(y/3)) == 0:
                    blockData = 0
                
                chunkData[blockCoord] = blockData
                chunks[chunkCoord] = chunkData

createChunk((0, 0))
createChunk((0, 1))
createChunk((1, 0))
createChunk((1, 1))

layer = 0
def render(keysPressed):
    global layer
    screen.fill((0, 0, 255))
    
    if keysPressed[pygame.K_PERIOD] and layer < heightLimit - 1: layer += 1
    if keysPressed[pygame.K_COMMA] and layer > 0: layer -= 1


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
                    block = chunks[chunkCoord][(x, y, z)]
                    if block:
                        if layer == y:
                            if chunkCoord[0] == 0: xThingy = 1
                            else: xThingy = chunkCoord[0]
                            if chunkCoord[1] == 0: yThingy = 1
                            else: yThingy = chunkCoord[1]
                            xPosition = (x * blockSize[0])# * xThingy)
                            yPosition = (y * blockSize[1])# * yThingy)
                            position = (xPosition, yPosition)
                            imageData = (blockImages[block], position)
                        else:
                            factor = 1
                            image = blockImages[block].copy()
                            if y > layer:
                                factor += (y - layer) / 10
                            if y < layer:
                                factor -= (layer - y) / 10
                            
                            
                            
                            image = pygame.transform.scale_by(image, abs(factor))
                            image.blit(numbers[y], (0, 0))
                            imageData = (image, (x*blockSize[0], z*blockSize[1]))

                        blocks.append(imageData)
    
    screen.blits(blocks)
    
    
      

    pygame.display.flip()