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
air = 0

blockImages = [air, gray, lightGray, white]
import random as r
chunk = {
    (0, 0, 0): 0
}
def createChunk():
    for x in range(10):
        for y in range(10):
            for z in range(10):
                coord = (x,y,z)
                chunk[coord] = 0
                if y <= 2:
                    chunk[coord] = y
                    if r.randint(0, 1):
                        chunk[coord] = 0
    

createChunk()
print(chunk)
layer = 2

def render():
    global layer
    screen.fill((0, 0, 255))
    
    blocks = []
    for x in range(10):
        for z in range(10):
            block = chunk[(x, layer, z)]
            if block != air: # make sure that it renders the tile beneath if it is air
                image = blockImages[block]
                image = pygame.transform.scale_by(image, layer+1)
                imageData = (image, (x*blockSize[0], z*blockSize[1]))
                blocks.append(imageData)
    
    screen.blits(blocks)
    layer += 1
    if layer > 2: layer = 0
    

    pygame.display.flip()