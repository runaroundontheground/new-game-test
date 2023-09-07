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
fillColor(1, (50, 50, 50))
fillColor(2, (100, 100, 100))
fillColor(3, (255, 255, 255))
fillColor(4, (0, 255, 0))
fillColor(5, (255, 0, 0))
fillColor(6, (200, 75, 0))
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
    (0, 0): (0, 1, 0)
}

def createChunk(chunkCoords = (0, 0)):
    for x in range(10):
        for y in range(heightLimit):
            for z in range(10):
                chunkCoord = chunkCoords
                blockCoord = (x,y,z)
                block = 0
                

                if y == 0: block = 1
                if y == 1: block = 2
                if y == 2: block = 3
                if y == 3: block = 4
                if y == 4: block = 5
                if y == 5: block = 6
                if r.randint(0, 3) == 0:
                    block =
                
                chunks[chunkCoord][blockCoord] = block

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
    blocks = []

    # get the chunks to be used for rendering




    for x in range(10):
        for y in range(heightLimit):
            for z in range(10):
                block = chunk[(x, y, z)]
                if block:
                    if layer == y:
                        imageData = (blockImages[block], (x*blockSize[0], z*blockSize[1]))
                    else:
                        factor = 1
                        if y > layer:
                            factor += (y - layer) / 10
                        if y < layer:
                            factor -= (layer - y) / 10
                        
                        
                        image = blockImages[block].copy()
                        image = pygame.transform.scale_by(image, abs(factor))
                        image.blit(numbers[y], (0, 0))
                        imageData = (image, (x*blockSize[0], z*blockSize[1]))

                    blocks.append(imageData)
    
    screen.blits(blocks)
    
    
      

    pygame.display.flip()