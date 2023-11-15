from widelyUsedVariables import chunkSize, chunks, blockSize, totalChunkSize, camera
from widelyUsedVariables import screenHeightInChunks, screenWidthInChunks
from perlin_noise import PerlinNoise
from controls import keysPressed
import random
import math

noise = PerlinNoise(octaves = 0.5)

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
                blockData = {
                    "type": "air",
                    "render": False
                }
                
                noiseCoordinate = [x, z]
                noiseIntensity = 70 # is this a good name?

                noiseCoordinate[0] += chunkSize[0] * chunkCoords[0]
                noiseCoordinate[1] += chunkSize[0] * chunkCoords[1]

                noiseCoordinate[0] /= noiseIntensity
                noiseCoordinate[1] /= noiseIntensity

                

                surfaceYLevel = noise(noiseCoordinate)
                surfaceYLevel = round( abs( surfaceYLevel * noiseIntensity))
                surfaceYLevel += 1 # make bottom layer be bedrock

                
                
                if y > surfaceYLevel: # above ground
                    if y <= waterHeight:
                        blockData["type"] = "water"
                
                if y < surfaceYLevel: # underground
                    if y < 8:
                        blockData["type"] = "dirt"
                    if y >= 8:
                        blockData["type"] = "stone"

                if y == surfaceYLevel: # surface level
                    blockData["type"] = "grass"
                    if y < 6:
                        blockData["type"] = "sand"
                        if y < waterHeight:
                            randomNumber = random.randint(0, 2)
                            if randomNumber == 0:
                                blockData["type"] = "sand"
                            elif randomNumber == 1:
                                blockData["type"] = "clay"
                            elif randomNumber == 2:
                                blockData["type"] = "gravel"
                    if y >= 8:
                        blockData["type"] = "stone"
                        if y < 10:
                            blockData["type"] = "dirt"
                    if y > 15:
                        blockData["type"] = "snowy stone"
                
                # bottom layer of world, at least have something
                if y == 0:
                    blockData["type"] = "bedrock"

                chunkData[(x, y, z)] = blockData
    
    


    chunks[chunkCoords] = {
        "data": chunkData,
        "blocksUpdated": False
    }
    

def findBlock(x = 1, y = 1, z = 1, extraInfo = False, ignoreWater = False):
    
    chunkCoord = getChunkCoord(x, z)
    blockCoord = getBlockCoord(x, y, z)
    
    if blockCoord[1] < 0 or blockCoord[1] > chunkSize[1] - 1:
        if extraInfo:
            return {
                "type": "air",
                "render": False
            }
        return False
    try:
        chunks[chunkCoord]["data"][blockCoord]
    except:
        createChunk(chunkCoord)

    block = chunks[chunkCoord]["data"][blockCoord]

    if extraInfo:
        return block
    else:
        if block["type"] != "air":
            if block["type"] == "water" and ignoreWater:
                return False
            return True
        else:
            return False

def findBlockWithEasyCoordinates(xPos = 1, yPos = 1, zPos = 1, chunkCoordInput = (0, 0)):

    x = xPos
    y = yPos
    z = zPos
    chunkX = chunkCoordInput[0]
    chunkZ = chunkCoordInput[1]

    if x < 0:
        x += chunkSize[0]
        chunkX -= 1
    if x >= chunkSize[0]:
        x -= chunkSize[0]
        chunkX += 1

    if y < 0 or y >= chunkSize[1]:
        return False

    if z < 0:
        z += chunkSize[0]
        chunkZ -= 1
    if z >= chunkSize[0]:
        z -= chunkSize[0]
        chunkZ += 1

    chunkCoord = (chunkX, chunkZ)

    try:
        chunks[chunkCoord]["data"][(x, y, z)]
    except:
        createChunk(chunkCoord)
    
    block = chunks[chunkCoord]["data"][(x, y, z)]

    if block["type"] != "air" and block["type"] != "water":
        return True
        
    

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
                block = chunks[chunkCoord]["data"][(x, y, z)]
                if block["type"] != "air":
                    
                    blockAbove = findBlockWithEasyCoordinates(x, y + 1, z, chunkCoord)
                    if not blockAbove:
                        block["render"] = True
                    
                    else: # there is a block above current one
                    
                        blockBelow = findBlockWithEasyCoordinates(x, y - 1, z, chunkCoord)
                        if not blockBelow:
                            if y != 0:
                                block["render"] = True
                        
                        else: # there is a block below current one
                            topSide = findBlockWithEasyCoordinates(x, y, z - 1, chunkCoord)
                            rightSide = findBlockWithEasyCoordinates(x + 1, y, z, chunkCoord)
                            bottomSide = findBlockWithEasyCoordinates(x, y, z + 1, chunkCoord)
                            leftSide = findBlockWithEasyCoordinates(x - 1, y, z, chunkCoord)
                            surrounded = False
                            if topSide and rightSide and leftSide and bottomSide:
                                surrounded = True
                            if not surrounded:
                                # current block has at least 1 air block next to it
                                block["render"] = True
                    
    chunks[chunkCoord]["blocksUpdated"] = True
                            
                            