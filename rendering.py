import pygame

screenWidth, screenHeight = 600, 400
screen = pygame.display.set_mode((screenWidth, screenHeight))
blockSize = (30, 30)
heightLimit = 10
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
                    if y == 2 and r.randint(0, 1):
                        chunk[coord] = 0
                if y > 2 and r.randint(0, 3) == 3:
                    chunk[coord] = 0

createChunk()
print(chunk)
layer = 0

def render():
    global layer
    screen.fill((0, 0, 255))
    
    blocks = []
    for x in range(10):
        for z in range(10):
            block = chunk[(x, layer, z)]
            if block != air: # make sure that it renders the tile beneath if it is air
                image = blockImages[block].copy()
                imageData = (image, (x*blockSize[0], z*blockSize[1]))
                blocks.append(imageData)
            else:
                y = layer
                while y > 0:
                    block = chunk[(x,y,z)]
                    if block != air:
                        image = blockImages[block].copy()
                        image = pygame.transform.scale_by(image, y/layer)
                        imageData = (image, (x*blockSize[0]/(y-layer), z*blockSize[1]/(y-layer)))
                        blocks.insert(0, imageData)
                        break
                    y -= 1
    
    screen.blits(blocks)

    layer += 1
    if layer >= 9: layer = 0    

    pygame.display.flip()