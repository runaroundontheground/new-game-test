from widelyUsedVariables import chunkSize, chunks, blockSize, totalChunkSize
from perlin_noise import PerlinNoise
from controls import keysPressed
import random
import math

noise = PerlinNoise(octaves = 1)

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
#createFirstChunk()

waterHeight = 4

def createChunk(chunkCoords = (0, 0)):
    chunkData = {}
    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                # blockData[1] is whether this block should be rendered
                # according to block updates
                blockData = ["air", False]
                
                noiseCoordinate = [x, z]
                noiseIntensity = 70 # is this a good name?

                noiseCoordinate[0] += chunkSize[0] * chunkCoords[0]
                noiseCoordinate[1] += chunkSize[0] * chunkCoords[1]

                noiseCoordinate[0] /= noiseIntensity
                noiseCoordinate[1] /= noiseIntensity

                

                noiseValue = noise(noiseCoordinate)
                noiseValue = round( abs( noiseValue * noiseIntensity))
                
                if y > noiseValue: # above ground
                    if y <= waterHeight:
                        blockData[0] = "water"
                
                if y < noiseValue: # underground
                    if y < 8:
                        blockData[0] = "dirt"
                    if y >= 8:
                        blockData[0] = "stone"

                if y == noiseValue: # surface level
                    blockData[0] = "grass"
                    if y < 6:
                        blockData[0] = "sand"
                        if y < waterHeight:
                            randomNumber = random.randint(0, 2)
                            if randomNumber == 0:
                                blockData[0] = "sand"
                            elif randomNumber == 1:
                                blockData[0] = "clay"
                            elif randomNumber == 2:
                                blockData[0] = "gravel"
                    if y >= 8:
                        blockData[0] = "stone"
                    if y > 15:
                        blockData[0] = "snowy stone"
                
                # bottom layer of world, at least have something
                if y == 0:
                    blockData[0] = "bedrock"

                
                

                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData

    runBlockUpdatesAfterGeneration(chunkCoords)

def findBlock(x = 1, y = 1, z = 1, extraInfo = False):
    
    chunkCoord = getChunkCoord(x, z)
    blockCoord = getBlockCoord(x, y, z)
    block = ["air", False]
    if blockCoord[1] < 0 or blockCoord[1] > chunkSize[1] - 1:
        return False
    #try:
    #    chunks[chunkCoord][blockCoord]
    #except:
    #    createChunk(chunkCoord)
    #else:
    block = chunks[chunkCoord][blockCoord]

    if extraInfo:
        pass
    else:
        if block[0] != "air":
            return True
        else:
            return False

def findBlockWithEasyCoordinates(xPos = 1, yPos = 1, zPos = 1, chunkCoords = (0, 0)):
    try:
        chunks[chunkCoords][(x, y, z)]
    except:
        return ["air", False]

    x = xPos
    y = yPos
    z = zPos
    chunkX = chunkCoords[0]
    chunkZ = chunkCoords[1]

    if x >= chunkSize[0]:
        x -= chunkSize[0]
        chunkX += 1
    if x < 0:
        x += chunkSize[0]
        chunkX -= 1
    if y >= chunkSize[1] or y < 0:
        return ["air", False]
    if z >= chunkSize[0]:
        z -= chunkSize[0]
        chunkZ += 1
    if z < 0:
        z += chunkSize[0]
        chunkZ -= 1

    chunkCoord = (x, z)
    return chunks[chunkCoord][(x, y, z)]

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
    if x >= chunkSize[0]:
        while x >= chunkSize[0]:
            x -= chunkSize[0]
    if z < 0:
        while z < 0:
            z += chunkSize[0]
    if z >= chunkSize[0]:
        while z >= chunkSize[0]:
            z -= chunkSize[0]

    blockCoord = (x, y, z)

    return blockCoord

def testChunk(chunkCoord):
    try:
        chunks[chunkCoord]
    except:
        createChunk(chunkCoord)

def runBlockUpdatesAfterGeneration(chunkCoord = (0, 0)):
    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                block = chunks[chunkCoord][(x, y, z)]
                if block[0] != "air":
                    """
                    check if there's any blocks above, if there is then
                    check for blocks to the sides,
                    if there's a block on every side besides underneath
                    then don't set it to true for rendering, since it's
                    false by default
                    when i add blocks being able to be placed without anything under them
                    it'll have to check below
                    if there isn't a block below it and there is a block above it
                    don't render it, even if there is air to the sides
                    ignore that rule for the bottom layer of the world though
                    """
                    blockAbove = findBlockWithEasyCoordinates(x, y + 1, z, chunkCoord)
                    if not blockAbove:
                        block[1] = True
                    else: # there is a block above current one
                        blockBelow = findBlockWithEasyCoordinates(x, y - 1, z, chunkCoord)
                        if not blockBelow:
                            block[1] = True
                        else: # there is a block below current one
                            topSide = findBlockWithEasyCoordinates(x, y, z - 1, chunkCoord)
                            rightSide = findBlockWithEasyCoordinates(x + 1, y, z, chunkCoord)
                            bottomSide = findBlockWithEasyCoordinates(x, y, z + 1, chunkCoord)
                            leftSide = findBlockWithEasyCoordinates(x - 1, y, z, chunkCoord)
                            if not (topSide and rightSide and bottomSide and leftSide):
                                 # current block has at least 1 air block next to it
                                block[1] = True
                            
                            