import pygame

screenWidth, screenHeight = 600, 400
screen = pygame.display.set_mode((screenWidth, screenHeight))
blockSize = (100, 100)
gray = pygame.surface.Surface((blockSize[0], blockSize[1]))
gray.fill((50,50,50))
lightGray = pygame.surface.Surface((blockSize[0], blockSize[1]))
lightGray.fill((100,100,100))
white = pygame.surface.Surface((blockSize[0], blockSize[1]))
white.fill((255, 255, 255))
blockImages = [gray, lightGray, white]
import random as r
chunk = {
    (0, 0, 0): 0
}
def createChunk():
    for x in range(10):
        for y in range(3):
            for z in range(10):
                
                chunk[(x,y,z)] = r.randint(0, 1)

print(chunk)
layer = 1

def render():
    screen.fill((255, 255, 255))
    createChunk()
    blocks = []
    for x in range(10):
        for z in range(10):
            block = chunk[(x, layer, z)]
            if block == 1:
                imageData = (lightGray, (x*blockSize[0], z*blockSize[1]))
            elif block == 0:
                imageData = (gray, (x*blockSize[0], z*blockSize[1]))
            blocks.append(imageData)
    
    screen.blits(blocks)
    layer += 1
    if layer > 3: layer = 0

    pygame.display.flip()