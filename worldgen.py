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
                if y > 5: blockData = 0

                chunkData[(x, y, z)] = blockData
                chunks[(0, 0)] = chunkData
createFirstChunk()

def createChunk(chunkCoords = (0, 0)):
    chunkData = {}
    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                # by default, the tile will be air
                blockData = 0 # air
                blockData = y + 1 
                # change above line once i actually add textures and better worldgen
                # hmmmmm i gotta figure out perlin noise...
                if random.randint(0, 2) == 0: # this also needs to be removed, it just
                    blockData = 0 # makes a tile have a 1/3 chance to be air
                if y > 5: blockData = 0
                if y == 0: blockData = 1
                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData




def findBlock(x = 1, y = 1, z = 1, extraInfo = False):
    
    chunkCoord = getChunkCoord(x, z)
    blockCoord = getBlockCoord(x, y, z)
    block = 0
    if blockCoord[1] < 0 or blockCoord[1] > chunkSize[1] - 1:
        return False
    try:
        chunks[chunkCoord][blockCoord]
    except:
        createChunk(chunkCoord)
    else:
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
    
    x = math.floor(x / blockSize)
    y = math.floor(y / blockSize)
    z = math.floor(z / blockSize)

    if x < 0:
        while x < 0:
            x += chunkSize[0]
    if x > chunkSize[0]:
        while x > chunkSize[0]:
            x -= chunkSize[0]
    if z < 0:
        while z < 0:
            z += chunkSize[0]
    if z > chunkSize[0]:
        while z > chunkSize[0]:
            z -= chunkSize[0]
    
    if x == chunkSize[0]:
        x -= 1
    if z == chunkSize[0]:
        z -= 1

    blockCoord = (x, y, z)

    return blockCoord


