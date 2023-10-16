from widelyUsedVariables import chunkSize, chunks, blockSize, totalChunkSize
from perlin_noise import PerlinNoise
from controls import keysPressed
import random
import math

noise = PerlinNoise(octaves = 1)
#thing = []
#rangeThing = 100
#for i in range(rangeThing):
#    for i2 in range(rangeThing):
#        i -= 50
#        i2 -= 50
#        newThing = noise(( i / rangeThing, i2 / rangeThing))
#        newThing *= 100
#        newThing = round(abs(newThing))
#        thing.append(newThing)
#print(thing)

"""FIX THIS! NEED TO MAKE IT USE AIR AND STUFF"""
def createFirstChunk():
    chunkData = {}
    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                blockData = "stone"
                if y > 5: blockData = "air"

                chunkData[(x, y, z)] = blockData
                chunks[(0, 0)] = chunkData
    
    thing = chunks[(0, 0)]
    thing[(4, 6, 4)] = "grass"
    thing[(4, 6, 5)] = "grass"
    thing[(4, 6, 6)] = "grass"
    thing[(3, 6, 6)] = "grass"
    thing[(5, 7, 4)] = "dirt"
    chunks[(0, 0)] = thing
createFirstChunk()


def createChunk(chunkCoords = (0, 0)):
    chunkData = {}
    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                
                blockData = "air"
                # now, how do i make perlin noise work?
                noiseCoordinate = [x, z]
                noiseIntensity = 100 # is this a good name?

                noiseCoordinate[0] += chunkSize[0] * chunkCoords[0]
                noiseCoordinate[1] += chunkSize[0] * chunkCoords[1]

                noiseCoordinate[0] /= noiseIntensity
                noiseCoordinate[1] /= noiseIntensity

                

                noiseValue = noise(noiseCoordinate)
                noiseValue = round( abs( noiseValue * noiseIntensity))
                

                if y == noiseValue:
                    blockData = "grass"
                if y < noiseValue:
                    blockData = "dirt"
                

                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData




def findBlock(x = 1, y = 1, z = 1, extraInfo = False):
    
    chunkCoord = getChunkCoord(x, z)
    blockCoord = getBlockCoord(x, y, z)
    block = "air"
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
        if block != "air":
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
        x = 0
    if z == chunkSize[0]:
        z = 0

    blockCoord = (x, y, z)

    return blockCoord


