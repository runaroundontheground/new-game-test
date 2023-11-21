from widelyUsedVariables import chunkSize, chunks, blockSize, totalChunkSize, camera
from widelyUsedVariables import screenHeightInChunks, screenWidthInChunks
from perlin_noise import PerlinNoise
from controls import keysPressed
import random
import math

noise = PerlinNoise(octaves = 0.5)


structures = {
    "tree 1": {}
}

def makeTree1():
    for x in range(5):
        for z in range(5):
            structures["tree 1"][(x, 3, z)] = {"type": "leaves"}
            if x != 0 and x != 4 and z != 0 and z != 4:
                structures["tree 1"][(x, 4, z)] = {"type": "leaves"}

    structures["tree 1"][(2, 3, 2)] = {"type": "log"}
    structures["tree 1"][(2, 0, 2)] = {"type": "log"}
    structures["tree 1"][(2, 1, 2)] = {"type": "log"}
    structures["tree 1"][(2, 2, 2)] = {"type": "log"}
makeTree1()
# add any additional things that all blocks require in their data automatically
# such as: render, and noBlockBelow
def fixStructuresData():
    for structureName, structureData in structures.items():
        for key, block in structures[structureName].items():
            
            structures[structureName][key]["render"] = False
            structures[structureName][key]["usesAlpha"] = False
fixStructuresData()


waterHeight = 4

def generateChunkTerrain(chunkCoords = (0, 0)):
    chunkData = {}

    def initialTerrainGeneration():

        for x in range(chunkSize[0]):
            for y in range(chunkSize[1]):
                for z in range(chunkSize[0]):
                    blockData = {
                        "type": "air",
                        "render": False,
                        "usesAlpha": False
                    }
                    
                    noiseCoordinate = [x, z]
                    noiseIntensity = 25 # is this a good name?

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
    initialTerrainGeneration()
  
    chunks[chunkCoords] = {
        "data": chunkData,
        "blocksUpdated": False,
        "structuresGenerated": False
    }

def generateChunkStructures(inputChunkCoord = (0, 0)):

    def generateStructures():

        def generateStructure(structureName, blockCoord):
            
            for structureBlockCoord, block in structures[structureName].items():

                chunkX = inputChunkCoord[0]
                chunkZ = inputChunkCoord[1]
                
                x = blockCoord[0] + structureBlockCoord[0]
                y = blockCoord[1] + structureBlockCoord[1]
                z = blockCoord[2] + structureBlockCoord[2]

                while x >= chunkSize[0]:
                    x -= chunkSize[0]
                    chunkX += 1
                while x < 0:
                    x += chunkSize[0]
                    chunkX -= 1

                while z >= chunkSize[0]:
                    z -= chunkSize[0]
                    chunkZ += 1
                while z < 0:
                    z += chunkSize[0]
                    chunkZ -= 1

                newBlockCoord = (x, y, z)
                chunkCoord = (chunkX, chunkZ)

                chunks[chunkCoord]["data"][newBlockCoord] = block


        for x in range(chunkSize[0]):
            for y in range(chunkSize[1]):
                for z in range(chunkSize[0]):
                    block = chunks[inputChunkCoord]["data"][(x, y, z)]
                    blockCoord = (x, y, z)

                    if block["type"] == "grass":
                        if random.randint(0, 20) == 0:
                            generateStructure("tree 1", blockCoord)
        chunks[inputChunkCoord]["structuresGenerated"] = True
    generateStructures()

def runBlockUpdatesAfterGeneration(chunkCoord = (0, 0)):

    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                block = chunks[chunkCoord]["data"][(x, y, z)]
                if block["type"] != "air":
                    
                    blockAbove = findBlockWithEasyCoordinates(x, y + 1, z, chunkCoord)
                    if not blockAbove:
                        block["render"] = True
                        if y != 0:
                            blockBelowThisOne = chunks[chunkCoord]["data"][(x, y - 1, z)]
                            if blockBelowThisOne["usesAlpha"]:
                                block["usesAlpha"] = True
                    
                    else: # there is a block above current one
                    
                        blockBelow = findBlockWithEasyCoordinates(x, y - 1, z, chunkCoord)
                        if not blockBelow:
                            if y != 0:
                                block["render"] = True
                                block["usesAlpha"] = True
                        
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
                                blockBelowThisOne = chunks[chunkCoord]["data"][(x, y - 1, z)]
                                if blockBelowThisOne["usesAlpha"]:
                                    block["usesAlpha"] = True
                            
                    
    chunks[chunkCoord]["blocksUpdated"] = True    


def smallScaleBlockUpdates(chunkCoord = (0, 0), blockCoord = (0, 0, 0)):
    # this is what will fix rendering and stuff when the player breaks/places blocks
    # it's a smaller scale version of runblockupdatesaftergeneration
    # we'll see how this goes
    
    pass


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
        generateChunkTerrain(chunkCoord)

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
        generateChunkTerrain(chunkCoord)
    
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
        generateChunkTerrain(chunkCoord)


                            
                            