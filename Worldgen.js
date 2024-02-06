/*from GlobalVariables import chunkSize, chunks, blockSize, totalChunkSize, camera
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
def fixStructureData():
    for structureName, structureData in structures.items():
        for key, block in structures[structureName].items():
            
            block["render"] = False
            block["alphaValue"] = 255
            block["hardness"] = dictOfBlockBreakingStuff[block["type"]]["hardness"]
            block["effectiveTool"] = dictOfBlockBreakingStuff[block["type"]]["effectiveTool"]
            block["dropsWithNoTool"] = dictOfBlockBreakingStuff[block["type"]]["dropsWithNoTool"]
fixStructureData()

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
                        "alphaValue": 255,
                        "hardness": 0,
                        "effectiveTool": "none",
                        "dropsWithNoTool": False
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
                    dropsWithNoTool = dictOfBlockBreakingStuff[blockData["type"]]["dropsWithNoTool"]

                    blockData["hardness"] = hardness
                    blockData["effectiveTool"] = effectiveTool
                    blockData["dropsWithNoTool"] = dropsWithNoTool

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

            if newBlockCoord not in chunks[chunkCoord]["data"]:
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
                    
                    def modifyOtherBlock(x, y, z, render = "no change", alphaValue = "no change"):
                        localBlockCoord, localChunkCoord = getBlockAndChunkCoord(x, y, z, chunkCoord)

                        if render != "no change":
                            chunks[localChunkCoord]["data"][localBlockCoord]["render"] = render
                        if alphaValue != "no change":
                            chunks[localChunkCoord]["data"][localBlockCoord]["alphaValue"] = alphaValue

                    if block["type"] == "water":
                        
                        blockAbove = findBlock(x, y + 1, z, extraInfo = True, chunkCoordInput = chunkCoord)
                        if blockAbove["type"] == "air":

                            # don't render water that's underneath other water, instead make
                            # the top water harder to see through
                            # and also in scale make sure water becomes bigger as a fix to this
                            # or just actually figure out how to make the scale and rendering work correctly
                            
                            block["alphaValue"] = 100
                            block["render"] = True
                            foundNotWater = False
                            subtracYy = 1
                            while not foundNotWater:
                                blockBelow = findBlock(x, y - subtracYy, z, extraInfo = True, chunkCoordInput = chunkCoord)
                                
                                if blockBelow["type"] == "water":
                                    block["alphaValue"] += 25
                                else:
                                    foundNotWater = True

                                if block["alphaValue"] >= 255:
                                    block["alphaValue"] = 255
                                    break


                                subtracYy -= 1

                                if subtracYy < -100 or foundNotWater:
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
                        
                        if above: # there's a block above this one
                            if below: # there's a block below this one

                                if blockBelow["alphaValue"] < 255:
                                    block["alphaValue"] = 100
                                    block["render"] = True
                                    modifyOtherBlock(x, y - 1, z, render = False)

                                if not surrounded:
                                    block["render"] = True

                            else: # no block below this one

                                block["alphaValue"] = 100
                                block["render"] = True

                        else: # there's no block above this one

                            block["render"] = True
                            if below: # there's a block under this one
                                if blockBelow["alphaValue"] < 255:
                                    block["alphaValue"] = 100
                                    block["render"] = True
                                    modifyOtherBlock(x, y - 1, z, render = False)

                            else: # no block under this one
                                block["alphaValue"] = 100
                                block["render"] = True
                            


                        

                chunks[chunkCoord]["data"][(x, y, z)] = block
                                
                    
    chunks[chunkCoord]["blocksUpdated"] = True
*/ 
// here is our break for next thing

/*
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

                if blockBelow["alphaValue"] < 255:
                    block["alphaValue"] = 100
                    modifyOtherBlock(x, y - 1, z, render = False)

                else:

                    belowSurrounded = checkSidesOfBlock(x, y - 1, z)
                    if belowSurrounded:
                        modifyOtherBlock(x, y - 1, z, render = False)
            else:
                block["alphaValue"] = 100
        
        if not above: # no block above this one
            block["render"] = True
            if below:

                if blockBelow["alphaValue"] < 255:
                    block["alphaValue"] = 100
                    modifyOtherBlock(x, y - 1, z, render = False)
                else:

                    belowSurrounded = checkSidesOfBlock(x, y - 1, z)
                    if belowSurrounded:
                        modifyOtherBlock(x, y - 1, z, render = False)

            else:
                block["alphaValue"] = 100
    else: # this current block is air

        if below:
            modifyOtherBlock(x, y - 1, z, render = True)

            blockBelow2 = findBlock(x, y - 2, z, True, chunkCoordInput = chunkCoord)
            below2 = checkForSolidBlock(blockBelow2)
            
            if not below2:
                modifyOtherBlock(x, y - 1, z, render = True, alphaValue = 100)
            else: # theres a block 2 blocks below
                if blockBelow2["alphaValue"] < 255:
                    modifyOtherBlock(x, y - 2, z, render = False)
                    modifyOtherBlock(x, y - 1, z, alphaValue = 100)


    

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
    

    if blockCoord not in chunks[chunkCoord]["data"]:
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





print("worldgen initialized")
*/



// part one of the thing

// Import statements are not applicable in this context

const chunkSize = [16, 16, 16]; // Assuming chunkSize is a 3-element array
const chunks = {};
const blockSize = 1; // Assuming blockSize is a single value
const totalChunkSize = 16; // Assuming totalChunkSize is a single value
const camera = {}; // Assuming camera is an object
const screenHeightInChunks = 16; // Assuming screenHeightInChunks is a single value
const screenWidthInChunks = 16; // Assuming screenWidthInChunks is a single value
const listOfBlockNames = []; // Assuming listOfBlockNames is an array
const dictOfBlockBreakingStuff = {}; // Assuming dictOfBlockBreakingStuff is an object

class PerlinNoise {
  constructor(octaves) {
    // Implementation of PerlinNoise class (not provided)
  }
}

const noise = new PerlinNoise(0.5);

const structures = {
  "tree 1": {}
};

function makeTree1() {
  for (let x = 0; x < 5; x++) {
    for (let z = 0; z < 5; z++) {
      structures["tree 1"][`${x},${3},${z}`] = { type: "leaves" };
      if (x !== 0 && x !== 4 && z !== 0 && z !== 4) {
        structures["tree 1"][`${x},${4},${z}`] = { type: "leaves" };
      }
    }

    structures["tree 1"][`${2},${3},${2}`] = { type: "log" };
    structures["tree 1"][`${2},${0},${2}`] = { type: "log" };
    structures["tree 1"][`${2},${1},${2}`] = { type: "log" };
    structures["tree 1"][`${2},${2},${2}`] = { type: "log" };
  }
}

makeTree1();

const copiedStructures = { ...structures };

function fixStructureData() {
  for (const [structureName, structureData] of Object.entries(copiedStructures)) {
    for (const [, block] of Object.entries(copiedStructures[structureName])) {
      block.render = false;
      block.alphaValue = 255;
      block.hardness = dictOfBlockBreakingStuff[block.type].hardness;
      block.effectiveTool = dictOfBlockBreakingStuff[block.type].effectiveTool;
      block.dropsWithNoTool = dictOfBlockBreakingStuff[block.type].dropsWithNoTool;
    }
  }
}

fixStructureData();

const waterHeight = 4;

function generateChunkTerrain(chunkCoords = [0, 0]) {
  const chunkData = {};

  function initialTerrainGeneration() {
    for (let x = 0; x < chunkSize[0]; x++) {
      for (let y = 0; y < chunkSize[1]; y++) {
        for (let z = 0; z < chunkSize[0]; z++) {
          const blockData = {
            type: "air",
            render: false,
            alphaValue: 255,
            hardness: 0,
            effectiveTool: "none",
            dropsWithNoTool: false
          };

          const noiseCoordinate = [x, z];
          const noiseIntensity = 25;

          noiseCoordinate[0] += chunkSize[0] * chunkCoords[0];
          noiseCoordinate[1] += chunkSize[0] * chunkCoords[1];

          noiseCoordinate[0] /= noiseIntensity;
          noiseCoordinate[1] /= noiseIntensity;

          let surfaceYLevel = noise(noiseCoordinate);
          surfaceYLevel = Math.round(Math.abs(surfaceYLevel * noiseIntensity));
          surfaceYLevel += 1;

          if (y > surfaceYLevel) {
            if (y <= waterHeight) {
              blockData.type = "water";
            }
          }

          if (y < surfaceYLevel) {
            if (y < 8) {
              blockData.type = "dirt";
            }
            if (y >= 8) {
              blockData.type = "stone";
            }
          }

          if (y === surfaceYLevel) {
            blockData.type = "grass";
            if (y < 6) {
              blockData.type = "sand";
              if (y < waterHeight) {
                const randomNumber = Math.floor(Math.random() * 3);
                if (randomNumber === 0) {
                  blockData.type = "sand";
                } else if (randomNumber === 1) {
                  blockData.type = "clay";
                } else if (randomNumber === 2) {
                  blockData.type = "gravel";
                }
              }
            }
            if (y >= 8) {
              blockData.type = "stone";
              if (y < 10) {
                blockData.type = "dirt";
              }
            }
            if (y > 15) {
              blockData.type = "snowy stone";
            }
          }

          if (y === 0) {
            blockData.type = "bedrock";
          }

          const hardness = dictOfBlockBreakingStuff[blockData.type].hardness;
          const effectiveTool = dictOfBlockBreakingStuff[blockData.type].effectiveTool;
          const dropsWithNoTool = dictOfBlockBreakingStuff[blockData.type].dropsWithNoTool;

          blockData.hardness = hardness;
          blockData.effectiveTool = effectiveTool;
          blockData.dropsWithNoTool = dropsWithNoTool;

          chunkData[`${x},${y},${z}`] = blockData;
        }
      }
    }
  }

  initialTerrainGeneration();

  chunks[`${chunkCoords[0]},${chunkCoords[1]}`] = {
    data: chunkData,
    blocksUpdated: false,
    structuresGenerated: false
  };
}

function generateChunkStructures(inputChunkCoord = [0, 0]) {
  function generateStructure(structureName, blockCoord) {
    const thisStructure = copiedStructures[structureName];

    for (const [structureBlockCoord, block] of Object.entries(thisStructure)) {
      const [x, y, z] = structureBlockCoord.split(",").map(Number);

      let chunkX = inputChunkCoord[0];
      let chunkZ = inputChunkCoord[1];

      let newX = blockCoord[0] + x;
      let newY = blockCoord[1] + y;
      let newZ = blockCoord[2] + z;

      while (newX >= chunkSize[0]) {
        newX -= chunkSize[0];
        chunkX += 1;
      }
      while (newX < 0) {
        newX += chunkSize[0];
        chunkX -= 1;
      }

      while (newZ >= chunkSize[0]) {
        newZ -= chunkSize[0];
        chunkZ += 1;
      }
      while (newZ < 0) {
        newZ += chunkSize[0];
        chunkZ -= 1;
      }

      if (newY <= 0) {
        newY = 1;
      }
      if (newY >= chunkSize[1]) {
       
// part two of the thing


function smallScaleBlockUpdates(chunkCoord = [0, 0], blockCoord = [0, 0, 0]) {
    const x = blockCoord[0];
    const y = blockCoord[1];
    const z = blockCoord[2];
  
    const block = chunks[`${chunkCoord[0]},${chunkCoord[1]}`].data[`${x},${y},${z}`];
  
    function checkForSolidBlock(block) {
      return block.type !== "water" && block.type !== "air";
    }
  
    const blockAbove = findBlock(x, y + 1, z, true, chunkCoord);
    const blockBelow = findBlock(x, y - 1, z, true, chunkCoord);
    const blockToRight = findBlock(x + 1, y, z, true, chunkCoord);
    const blockToLeft = findBlock(x - 1, y, z, true, chunkCoord);
    const blockToUp = findBlock(x, y, z - 1, true, chunkCoord);
    const blockToDown = findBlock(x, y, z + 1, true, chunkCoord);
  
    const above = checkForSolidBlock(blockAbove);
    const below = checkForSolidBlock(blockBelow);
    const toRight = checkForSolidBlock(blockToRight);
    const toLeft = checkForSolidBlock(blockToLeft);
    const toUp = checkForSolidBlock(blockToUp);
    const toDown = checkForSolidBlock(blockToDown);
  
    const surrounded = toRight && toLeft && toUp && toDown;
  
    function modifyOtherBlock(x, y, z, render = "no change", alphaValue = "no change") {
      const [localBlockCoord, localChunkCoord] = getBlockAndChunkCoord(x, y, z, chunkCoord);
  
      if (render !== "no change") {
        chunks[`${localChunkCoord[0]},${localChunkCoord[1]}`].data[`${localBlockCoord[0]},${localBlockCoord[1]},${localBlockCoord[2]}`].render = render;
      }
      if (alphaValue !== "no change") {
        chunks[`${localChunkCoord[0]},${localChunkCoord[1]}`].data[`${localBlockCoord[0]},${localBlockCoord[1]},${localBlockCoord[2]}`].alphaValue = alphaValue;
      }
    }
  
    function checkSidesOfBlock(x, y, z) {
      const left = findBlock(x - 1, y, z, chunkCoord);
      const right = findBlock(x + 1, y, z, chunkCoord);
      const down = findBlock(x, y, z + 1, chunkCoord);
      const up = findBlock(x, y, z - 1, chunkCoord);
      return left && right && down && up;
    }
  
    if (block.type !== "air") {
      if (above) { // there's a block above this one
        if (!surrounded) {
          block.render = true;
        }
  
        if (below) {
          if (blockBelow.alphaValue < 255) {
            block.alphaValue = 100;
            modifyOtherBlock(x, y - 1, z, false);
          } else {
            const belowSurrounded = checkSidesOfBlock(x, y - 1, z);
            if (belowSurrounded) {
              modifyOtherBlock(x, y - 1, z, false);
            }
          }
        } else {
          block.alphaValue = 100;
        }
      }
  
      if (!above) { // no block above this one
        block.render = true;
        if (below) {
          if (blockBelow.alphaValue < 255) {
            block.alphaValue = 100;
            modifyOtherBlock(x, y - 1, z, false);
          } else {
            const belowSurrounded = checkSidesOfBlock(x, y - 1, z);
            if (belowSurrounded) {
              modifyOtherBlock(x, y - 1, z, false);
            }
          }
        } else {
          block.alphaValue = 100;
        }
      }
    } else { // this current block is air
      if (below) {
        modifyOtherBlock(x, y - 1, z, true);
        const blockBelow2 = findBlock(x, y - 2, z, true, chunkCoord);
        const below2 = checkForSolidBlock(blockBelow2);
  
        if (!below2) {
          modifyOtherBlock(x, y - 1, z, true, 100);
        } else { // there's a block 2 blocks below
          if (blockBelow2.alphaValue < 255) {
            modifyOtherBlock(x, y - 2, z, false);
            modifyOtherBlock(x, y - 1, z, 100);
          }
        }
      }
    }
  
    chunks[`${chunkCoord[0]},${chunkCoord[1]}`].data[`${x},${y},${z}`] = block;
  }
  
  function findBlock(xPos, yPos, zPos, extraInfo = false, ignoreWater = false, chunkCoordInput = null) {
    let x, y, z, chunkX, chunkZ;
  
    if (chunkCoordInput !== null) {
      x = xPos;
      y = yPos;
      z = zPos;
  
      chunkX = chunkCoordInput[0];
      chunkZ = chunkCoordInput[1];
  
      while (x >= chunkSize[0]) {
        x -= chunkSize[0];
        chunkX
  