from GlobalVariables import chunkSize, chunks, blockSize, totalChunkSize, camera
from GlobalVariables import screenHeightInChunks, screenWidthInChunks, listOfBlockNames, dictOfBlockBreakingStuff
from perlin_noise import PerlinNoise
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

structures = structures.copy()

# add any additional things that all blocks require in their data automatically
# such as render
def fixStructuresData():
    for structureName, structureData in structures.items():
        for key, block in structures[structureName].items():
            
            block["render"] = False
            block["alphaValue"] = 0
            block["hardness"] = dictOfBlockBreakingStuff[block["type"]]["hardness"]
            block["effectiveTool"] = dictOfBlockBreakingStuff[block["type"]]["effectiveTool"]
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
                        "alphaValue": 0,
                        "hardness": 0,
                        "effectiveTool": "none"
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

                    hardness = dictOfBlockBreakingStuff[blockData["type"]]["hardness"]
                    effectiveTool = dictOfBlockBreakingStuff[blockData["type"]]["effectiveTool"]
                    blockData["hardness"] = hardness
                    blockData["effectiveTool"] = effectiveTool

                    chunkData[(x, y, z)] = blockData
    initialTerrainGeneration()
  
    chunks[chunkCoords] = {
        "data": chunkData,
        "blocksUpdated": False,
        "structuresGenerated": False
    }

def generateChunkStructures(inputChunkCoord = (0, 0)):

    def generateStructure(structureName, blockCoord):
        thisStructure = structures[structureName]
        
        for structureBlockCoord, block in thisStructure.items():


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

            if y <= 0:
                y = 1
            if y >= chunkSize[1]:
                y = chunkSize[1] - 1

            newBlockCoord = (x, y, z)
            chunkCoord = (chunkX, chunkZ)

            try:
                chunks[chunkCoord]["data"]
            except:
                generateChunkTerrain(chunkCoord)

            chunks[chunkCoord]["data"][newBlockCoord] = block.copy()


    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                block = chunks[inputChunkCoord]["data"][(x, y, z)]
                blockCoord = (x, y, z)

                if block["type"] == "grass":
                    if random.randint(0, 20) == 0:
                        generateStructure("tree 1", blockCoord)
    chunks[inputChunkCoord]["structuresGenerated"] = True

def runBlockUpdatesAfterGeneration(chunkCoord = (0, 0)):

    for x in range(chunkSize[0]):
        for y in range(chunkSize[1]):
            for z in range(chunkSize[0]):
                block = chunks[chunkCoord]["data"][(x, y, z)]

                if block["type"] != "air":
                    
                    def checkForSolidBlock(block):
                        if block["type"] != "water" and block["type"] != "air":
                            return True
                        return False
                    

                    if block["type"] == "water":
                        
                        blockAbove = findBlock(x, y + 1, z, extraInfo = True, chunkCoordInput = chunkCoord)
                        if blockAbove["type"] == "air":

                            # don't render water that's underneath other water, instead make
                            # the top water darker
                            # and also in scale make sure water becomes bigger as a fix to this
                            # or just actually figure out how to make the scale and rendering work correctly
                            
                            block["alphaValue"] = 150
                            block["render"] = True
                            foundNotWater = False
                            subtracYy = 1
                            while not foundNotWater:
                                blockBelow = findBlock(x, y - subtracYy, z, extraInfo = True, chunkCoordInput = chunkCoord)
                                
                                if blockBelow["type"] == "water":
                                    block["alphaValue"] -= 25

                                if blockBelow["type"] != "water":
                                    foundNotWater = True

                                if block["alphaValue"] <= 0:
                                    block["alphaValue"] = 0
                                    break


                                subtracYy -= 1
                                if subtracYy < -100:
                                    break

                                if foundNotWater:
                                    break
                        

                    else: # this block isn't water
                        blockAbove = findBlock(x, y + 1, z, extraInfo = True, chunkCoordInput = chunkCoord)
                        blockBelow = findBlock(x, y - 1, z, extraInfo = True, chunkCoordInput = chunkCoord)
                        blockToRight = findBlock(x + 1, y, z, extraInfo = True, chunkCoordInput = chunkCoord)
                        blockToLeft = findBlock(x - 1, y, z, extraInfo = True, chunkCoordInput = chunkCoord)
                        blockToDown = findBlock(x, y, z + 1, extraInfo = True, chunkCoordInput = chunkCoord)
                        blockToUp = findBlock(x, y, z - 1, extraInfo = True, chunkCoordInput = chunkCoord)

                        above = checkForSolidBlock(blockAbove)
                        below = checkForSolidBlock(blockBelow)
                        toRight = checkForSolidBlock(blockToRight)
                        toLeft = checkForSolidBlock(blockToLeft)
                        toUp = checkForSolidBlock(blockToUp)
                        toDown = checkForSolidBlock(blockToDown)
                        surrounded = False
                        if toRight and toLeft and toUp and toDown:
                            surrounded = True

                        def setAlpha(alphaValue):
                            block["alphaValue"] = alphaValue
                            block["render"] = True
                        
                        if above: # there's a block above this one
                            if below: # there's a block below this one
                                if blockBelow["alphaValue"] != 0:
                                    setAlpha(250)
                                if not surrounded:
                                    block["render"] = True
                            else: # no block below this one
                                setAlpha(150)
                        else: # there's no block above this one
                            block["render"] = True
                            if below: # there's a block under this one
                                if blockBelow["alphaValue"] != 0:
                                    setAlpha(250)
                            


                        

                    chunks[chunkCoord]["data"][(x, y, z)] = block
                    if block["type"] == "water" and block["render"]:
                        print(block["alphaValue"])
                                
                    
    chunks[chunkCoord]["blocksUpdated"] = True    

def smallScaleBlockUpdates(chunkCoord = (0, 0), blockCoord = (0, 0, 0)):
   
    x = blockCoord[0]
    y = blockCoord[1]
    z = blockCoord[2]

    block = chunks[chunkCoord]["data"][blockCoord]

    def checkForSolidBlock(block):
        if block["type"] != "water" and block["type"] != "air":
            return True
        return False

    blockAbove = findBlock(x, y + 1, z, extraInfo = True, chunkCoordInput = chunkCoord)
    blockBelow = findBlock(x, y - 1, z, extraInfo = True, chunkCoordInput = chunkCoord)
    blockToRight = findBlock(x + 1, y, z, extraInfo = True, chunkCoordInput = chunkCoord)
    blockToLeft = findBlock(x - 1, y, z, extraInfo = True, chunkCoordInput = chunkCoord)
    blockToUp = findBlock(x, y, z - 1, extraInfo = True, chunkCoordInput = chunkCoord)
    blockToDown = findBlock(x, y, z + 1, extraInfo = True, chunkCoordInput = chunkCoord)

    above = checkForSolidBlock(blockAbove)
    below = checkForSolidBlock(blockBelow)
    toRight = checkForSolidBlock(blockToRight)
    toLeft = checkForSolidBlock(blockToLeft)
    toUp = checkForSolidBlock(blockToUp)
    toDown = checkForSolidBlock(blockToDown)
    surrounded = False
    if toRight and toLeft and toUp and toDown:
        surrounded = True

    def setAlpha(alphaValue):
        block["alphaValue"] = alphaValue
        block["render"] = True
    
    def modifyOtherBlock(x, y, z, render = "no change", alphaValue = "no change"):
        localBlockCoord, localChunkCoord = getBlockAndChunkCoord(x, y, z, chunkCoord)

        if render != "no change":
            chunks[localChunkCoord]["data"][localBlockCoord]["render"] = render
        if alphaValue != "no change":
            chunks[localChunkCoord]["data"][localBlockCoord]["alphaValue"] = alphaValue

    def checkSidesOfBlock(x, y, z):
        left = findBlock(x - 1, y, z, chunkCoordInput = chunkCoord)
        right = findBlock(x + 1, y, z, chunkCoordInput = chunkCoord)
        down = findBlock(x, y, z + 1, chunkCoordInput = chunkCoord)
        up = findBlock(x, y, z - 1, chunkCoordInput = chunkCoord)
        if left and right and down and up:
            return True
        return False



    if block["type"] != "air":
        if above: # there's a block above this one
            if not surrounded:
                block["render"] = True
            if below:
                if blockBelow["alphaValue"] != 0:
                    block["alphaValue"] = 200
                else:
                    belowSurrounded = checkSidesOfBlock(x, y - 1, z)
                    if belowSurrounded:
                        modifyOtherBlock(x, y - 1, z, False)
            else:
                block["alphaValue"] = 150
        
        if not above: # no block above this one
            block["render"] = True
            if below:
                if blockBelow["alphaValue"] != 0:
                    block["alphaValue"] = 200
                else:
                    belowSurrounded = checkSidesOfBlock(x, y - 1, z)
                    if belowSurrounded:
                        modifyOtherBlock(x, y - 1, z, False)

            else:
                block["alphaValue"] = 150
    else: # this current block is air
        if below:
            modifyOtherBlock(x, y - 1, z, True)
            blockBelow2 = findBlock(x, y - 2, z, True, chunkCoordInput = chunkCoord)
            below2 = checkForSolidBlock(blockBelow2)
            
            if not below2:
                modifyOtherBlock(x, y - 1, z, True, 150)


    

    chunks[chunkCoord]["data"][blockCoord] = block

def findBlock(xPos, yPos, zPos, extraInfo = False, ignoreWater = False, 
              chunkCoordInput = None):
    
    if chunkCoordInput != None:
        x = xPos
        y = yPos
        z = zPos
    
        chunkX = chunkCoordInput[0]
        chunkZ = chunkCoordInput[1]
        
        while x >= chunkSize[0]:
            x -= chunkSize[0]
            chunkX += 1
        while x < 0:
            x += chunkSize[0]
            chunkX -= 1

        if y >= chunkSize[1]:
            y = chunkSize[1] - 1
        if y < 0:
            y = 0

        while z >= chunkSize[0]:
            z -= chunkSize[0]
            chunkZ += 1
        while z < 0:
            z += chunkSize[0]
            chunkZ -= 1

        blockCoord = (x, y, z)
        chunkCoord = (chunkX, chunkZ)
    else:
        blockCoord = getBlockCoord(xPos, yPos, zPos)
        chunkCoord = getChunkCoord(xPos, zPos)
    

    try:
        chunks[chunkCoord]["data"][blockCoord]
    except:
        generateChunkTerrain(chunkCoord)

    block = chunks[chunkCoord]["data"][blockCoord]

    if extraInfo:
        return block
    
    if block["type"] != "air":
        if block["type"] == "water" and ignoreWater:
            return False
        return True
    
    return False
        
def getChunkCoord(xPos = 1, zPos = 1):
    
    x = math.floor(xPos / totalChunkSize)
    z = math.floor(zPos / totalChunkSize)
    
    chunkCoord = (x, z)

    return chunkCoord

def getBlockCoord(xPos = 1, yPos = 1, zPos = 1, usesSimpleInputs = False):
    
    if not usesSimpleInputs:
        x = math.floor(xPos / blockSize)
        y = math.floor(yPos / blockSize)
        z = math.floor(zPos / blockSize)
    else:
        x = xPos
        y = yPos
        z = zPos


    while x < 0:
        x += chunkSize[0]
    while x >= chunkSize[0]:
        x -= chunkSize[0]
    
    if y >= chunkSize[1]:
        y = chunkSize[1] - 1
    if y < 0:
        y = 0

    while z < 0:
        z += chunkSize[0]
    while z >= chunkSize[0]:
        z -= chunkSize[0]

    blockCoord = (x, y, z)

    return blockCoord

def getBlockAndChunkCoord(xPos, yPos, zPos, inputChunkCoord):
    x = xPos
    y = yPos
    z = zPos
    chunkX = inputChunkCoord[0]
    chunkZ = inputChunkCoord[1]

    while x < 0:
        x += chunkSize[0]
        chunkX -= 1
    while x >= chunkSize[0]:
        x -= chunkSize[0]
        chunkX += 1
    
    if y >= chunkSize[1]:
        y = chunkSize[1] - 1
    if y < 0:
        y = 0

    while z < 0:
        z += chunkSize[0]
        chunkZ -= 1
    while z >= chunkSize[0]:
        z -= chunkSize[0]
        chunkZ += 1

    blockCoord = (x, y, z)
    chunkCoord = (chunkX, chunkZ)

    return blockCoord, chunkCoord

