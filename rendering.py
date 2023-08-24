import pygame

screenWidth, screenHeight = 600, 400
screen = pygame.display.set_mode((screenWidth, screenHeight))
blockSize = (30, 30)
heightLimit = 6
gray = pygame.surface.Surface((blockSize[0], blockSize[1])); gray.fill((50,50,50))
lightGray = pygame.surface.Surface((blockSize[0], blockSize[1])); lightGray.fill((100,100,100))
white = pygame.surface.Surface((blockSize[0], blockSize[1])); white.fill((255,255,255))
air = 0
green = pygame.surface.Surface((blockSize[0], blockSize[1])); green.fill((0, 255, 0))
red = pygame.surface.Surface((blockSize[0], blockSize[1])); red.fill((255, 0, 0))
brown = pygame.surface.Surface((blockSize[0], blockSize[1])); brown.fill((200, 75, 0))

blockImages = [air, gray, lightGray, white, green, red, brown]
import random as r
chunk = {
    (0, 0, 0): 0
}
def createChunk():
    for x in range(10):
        for y in range(heightLimit):
            for z in range(10):
                coord = (x,y,z)
                chunk[coord] = 0

                if y == 0: chunk[coord] = 1
                if y == 1:
                    if x > 2:
                        chunk[coord] = 2
                if y == 2:
                    if x > 4:
                        chunk[coord] = 3
                if y == 3:
                    if x > 5:
                        chunk[coord] = 4
                if y == 4:
                    if x > 6:
                        chunk[coord] = 5
                if y == 5:
                    if x > 8:
                        chunk[coord] = 6

                

createChunk()
print(chunk)
layer = 0

def render():
    global layer
    screen.fill((0, 0, 255))
    
    blocks = []
    for x in range(10):
        for y in range(heightLimit):
            for z in range(10):
                block = chunk[(x, y, z)]
                if block:
                    image = blockImages[block].copy()
                    if layer-y != 0:
                        factor = 1*(y-layer)
                    else: factor = 1
                    print(factor)
                    image = pygame.transform.scale_by(image, abs(factor))
                    imageData = (image, (x*blockSize[0], z*blockSize[1]))
                """
                if block:
                    image = blockImages[block].copy()
                    imageData = (image, (x*blockSize[0], z*blockSize[1]))
                    blocks.append(imageData)
                else:
                    y = heightLimit - 1
                    while y >= 0:
                        block = chunk[(x,y,z)]
                        if block:
                            image = blockImages[block].copy()
                            image = pygame.transform.scale_by(image, 1/(layer-y))
                            print(1/(layer-y)*1.5)
                            imageData = (image, (x*blockSize[0], z*blockSize[1]))
                            blocks.insert(0, imageData)
                            
                        y -= 1
                """
    
    screen.blits(blocks)
    layer += 1
    if layer >= heightLimit - 1: layer = 0  
    
      

    pygame.display.flip()