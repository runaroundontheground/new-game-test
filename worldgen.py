from widelyUsedVariables import chunkSize, chunks, blockSize, totalChunkSize
from controls import keysPressed
import random
import math



def createFirstChunk():
    chunkData = {}
    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                blockData = 5

                chunkData[(x, y, z)] = blockData
                chunks[(0, 0)] = chunkData
createFirstChunk()

def createChunk(chunkCoords = (0, 0)):
    chunkData = {}
    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                blockData = 0
                
                blockData = y + 1 # this will need to be changed later when 
                # i add more height or something
                # hmmmmm i gotta figure out perlin noise...
                if random.randint(0, 2) == 0: # this also needs to be removed, it just
                    blockData = 0 # makes a tile have a 1/3 chance to be air
                
                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData




def findBlock(x = 1, y = 1, z = 1, extraInfo = False):
    
    chunkCoord = getChunkCoord(x, z)

    blockCoord = getBlockCoord()
     # rounding might cause problems later, we'll see
    block = chunks[chunkCoord][blockCoord]

    if extraInfo:
        pass
    else:
        if block != 0:
            return True
        else:
            return False

def getChunkCoord(x = 1, z = 1):
    xPos = math.floor(x / totalChunkSize)
    zPos = math.floor(z / totalChunkSize)
    
    chunkCoord = (xPos, zPos)

    return chunkCoord

def getBlockCoord(x = 1, y = 1, z = 1):
    """use how it works from jumpy 2, but without the weird str()[-1] thing"""
    xPos = math.floor(x / blockSize)
    yPos = math.floor(y / blockSize)
    zPos = math.floor(z / blockSize)

    blockCoord = (xPos, yPos, zPos)

    return blockCoord



