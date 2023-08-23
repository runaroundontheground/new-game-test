import pygame

screenWidth, screenHeight = 600, 400
screen = pygame.display.set_mode((screenWidth, screenHeight))
blockSize = (30, 30)
gray = pygame.surface.Surface((blockSize[0], blockSize[1]))
gray.fill((50,50,50))
lightGray = pygame.surface.Surface((blockSize[0], blockSize[1]))
lightGray.fill((100,100,100))
white = pygame.surface.Surface((blockSize[0], blockSize[1]))
white.fill((255, 255, 255))
air = pygame.surface.Surface((blockSize[0], blockSize[1]))
air.fill((0, 255, 0, 255))
blockImages = [air, gray, lightGray, white]
import random as r
chunk = {
    (0, 0, 0): 0
}
def createChunk():
    for x in range(10):
        for y in range(3):
            for z in range(10):
                
                chunk[(x,y,z)] = r.randint(1, 2)
    chunk[(r.randint(0, 10), 2, r.randint(0, 10))] = 0
    chunk[(r.randint(0, 10), 2, r.randint(0, 10))] = 0


print(chunk)
layer = 3

def render():
    global layer
    screen.fill((0, 0, 0))
    
    blocks = []
    for x in range(10):
        for z in range(10):
            block = chunk[(x, layer, z)]
            image = blockImages[block]
            image = pygame.transform.scale_by(image, layer+1)
            imageData = (image, (x*blockSize[0], z*blockSize[1]))
            blocks.append(imageData)
    
    screen.blits(blocks)
    

    pygame.display.flip()