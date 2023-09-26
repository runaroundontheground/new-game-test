from controls import keysPressed
from main import screenWidth, screenHeight, totalChunkSize
import random
import math


# need to find the size of the screen, for deciding how many chunks to render at once

screenWidthInChunks = math.floor( screenWidth / totalChunkSize )
screenHeightInChunks = math.floor( screenHeight / totalChunkSize)
print(screenWidthInChunks)
print(screenHeightInChunks)
chunks = {} # t
#    (0, 0): {
#        (0, 1, 0): 0 # currently would be air
#    }
#}




def createChunk(chunkCoords = (0, 0)):
    chunkData = {}
    for x in range(10):
        for y in range(chunkSize[1]):
            for z in range(10):
                blockData = 0
                
                blockData = y + 1 # this will need to be changed later when 
                # i add more height or something
                # hmmmmm i gotta figure out perlin noise...
                if random.randint(0, 2) == 0: # this also needs to be removed, it just
                    blockData = 0 # makes a tile have a 1/3 chance to be air
                
                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData




def getBlockFromPos(x = 1, y = 1, z = 1, extraInfo = False):
    
    chunkX = math.floor(x / blockSize)
    chunkZ = math.foor(z / blockSize)
    chunkCoord = (chunkX, chunkZ)

    blockCoord = (x, y, z)

    block = chunks[chunkCoord][blockCoord]

    if extraInfo:
        pass
    else:
        if block != 0:
            return True
        else:
            return False
