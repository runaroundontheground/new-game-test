
import {
  chunkSize, chunks, blockSize, totalChunkSize, camera, canvasHeightInChunks, canvasWidthInChunks,
  listOfBlockNames, dictOfBlockBreakingStuff, consoleLog, random
} from "./GlobalVariables.mjs";
consoleLog("loading Worldgen.mjs");

import { noise } from "./PerlinNoise.mjs";

// set the seed for this world
noise.seed(Math.random());


structures = {
  "tree 1": {}
};

function makeTree1() {
  for (let x = 0; x < 5; x++) {
    for (let z = 0; z < 5; z++) {
      structures["tree 1"][[x, 3, z].toString()] = { "type": "leaves" };

      if (x !== 0 && x !== 4 && z !== 0 && z != 4) {
        structures["tree 1"][[x, 4, z].toString()] = { "type": "leaves" };
      };
    };
  };

  structures["tree 1"]["2,3,2"] = { "type": "log" }
  structures["tree 1"]["2,0,2"] = { "type": "log" }
  structures["tree 1"]["2,1,2"] = { "type": "log" }
  structures["tree 1"]["2,2,2"] = { "type": "log" }
}
makeTree1();



// add any additional things that all blocks require in their data automatically such as render

function fixStructureData() {
  let structureNames = Object.keys(structures);
  for (let i = 0; i < structureNames.length; i++) {
    let structureName = structureNames[i];
    let blocks = Object.keys(structures[structureName]);

    for (let i2 = 0; i2 < blocks.length; i2++) {
      let block = blocks[i2];

      block.render = false;
      block.alphaValue = 255;

      let accessedBreakingInfo = dictOfBlockBreakingStuff[block.type];
      block.hardness = accessedBreakingInfo.hardness;
      block.effectiveTool = accessedBreakingInfo.effectiveTool;
      block.dropsWithNoTool = accessedBreakingInfo.dropsWithNoTool;
      blocks[i2] = block;
    }
  }
}
fixStructureData();

let waterHeight = 4;

function generateChunkTerrain (chunkCoords) {
let chunkData = {};

  function initialTerrainGeneration() {

  for (let x = 0; x < chunkSize[0]; x++) {
    for (let y = 0; y < chunkSize[1]; y++) {
      for (let z = 0; z < chunkSize[0]; z++) {
        let blockData = {
          "type": "air",
          "render": False,
          "alphaValue": 255,
          "hardness": 0,
          "effectiveTool": "none",
          "dropsWithNoTool": false
        }

        let noiseX = x;
        let noiseZ = z;
        let noiseIntensity = 25;
        noiseX += chunkSize[0] * chunkCoords[0];
        noiseZ += chunkSize[0] * chunkCoords[1];

        noiseX /= noiseIntensity;
        noiseZ /= noiseIntensity;

        let surfaceYLevel = Math.round(Math.abs(noise.perlin2(noiseX, noiseZ) * noiseIntensity)) + 1;

        if (y > surfaceYLevel) {
          if (y <= waterHeight) {
            blockData.type = "water";
          }
        }
        if (y === surfaceYLevel) {
          blockData.type = "grass";
        }

        if (y < surfaceYLevel) {
          if (y < 8) {
            blockData.type = "dirt";
          }
          if (y >= 8) {
            blockData.type = "stone";
          }
          if (y < 6) {
            blockData.type = "sand";
          }
          if (y < waterHeight) {
            let randomNum = Math.floor(Math.random() * 3);
            switch (randomNum) {
              case randomNum === 0:
                blockData.type = "sand";
                break;
              case randomNum === 1:
                blockData.type = "clay";
                break;
              case randomNum === 2:
                blockData.type = "gravel";
                break;
              break;
            }
            
          };

        }

        if (y >= 8) {blockData.type = "stone";};
        if (y < 10) {blockData.type = "dirt";};
        if (y > 15) {blockData.type = "snowy stone";};



        if (y === 0) {blockData.type = "bedrock";};

        let accessedBreakingInfo = dictOfBlockBreakingStuff[blockData.type];

        blockData["hardness"] = accessedBreakingInfo.hardness;
        blockData["effectiveTool"] = accessedBreakingInfo.effectiveTool;
        blockData["dropsWithNoTool"] = accessedBreakingInfo.dropsWithNoTool;

        
        chunkData[[x, y, z].toString()] = blockData;

      }
    }
  }
}
initialTerrainGeneration()

chunks[chunkCoords] = {
  "data": chunkData,
  "blocksUpdated": false,
  "structuresGenerated": false
};
}


function generateChunkStructures(inputChunkCoord) {
  function generateStructure(structureName, blockCoord) {
    let thisStructure = structures[structureName];
    let thisStructureKeys = Object.keys(thisStructure);

    for (let i = 0; i < thisStructureKeys.length; i++) {
      let chunkX = inputChunkCoord[0];
      let chunkZ = inputChunkCoord[1];

      let structureBlockCoord = thisStructureKeys[i];
      let block = thisStructure[structureBlockCoord];

      let x = blockCoord[0] + structureBlockCoord[0];
      let y = blockCoord[1] + structureBlockCoord[1];
      let z = blockCoord[2] + structureBlockCoord[2];

      while (x >= chunkSize[0]) {
        x -= chunkSize;
        chunkX += 1;
      }
      while (x < 0) {
        x += chunkSize[0];
        chunkX -= 1;
      }
      while (z >= chunkSize[0]) {
        z -= chunkSize[0];
        chunkZ += 1;
      }
      while (z < 0) {
        z += chunkSize[0];
        chunkZ -= 1;
      };

      if (y <= 0) {
        y = 1
      };
      if (y >= chunkSize[1]) {
        y = chunkSize[0] - 1;
      };

      let newBlockCoord = [x, y, z].toString();
      let chunkCoord = [chunkX, chunkZ].toString();

      if (chunks[chunkCoord]["data"] === undefined) {
        generateChunkTerrain(chunkCoord);
      };

      chunks[chunkCoord]["data"][newBlockCoord] = block;
    };
  };
  for (let x = 0; x < chunkSize[0]; x++) {
    for (let y = 0; y < chunkSize[1]; y++) {
      for (let z = 0; z < chunkSize[0]; y++) {

        let blockCoord = [x, y, z].toString();
        let block = chunks[inputChunkCoord]["data"][blockCoord];

        if (block.type === "grass") {
          if (random.integer(0, 20) === 0) {
            generateStructure("tree 1", blockCoord);
          };
        };
        chunks[inputChunkCoord].structuresGenerated = true;
        

      };
    };
  };
};


function runBlockUpdatesAfterGeneration(chunkCoord) {
  for (let x = 0; x < chunkSize[0]; x++) {
    for (let y = 0; y < chunkSize[1]; y++) {
      for (let z = 0; z < chunkSize[0]; z++) {
        let blockCoord = [x, y, z].toString();
        let block = chunks[chunkCoord].data[blockCoord];

        function checkForSolidBlock(block) {
          if (block.type != "air" && block.type != "water") {
            return true;
          };
          return false;

        };

        function modifyOtherBlock(x, y, z, render = "no change", alphaValue = "no change") {
          let localBlockAndChunkCoord = getBlockAndChunkCoord(x, y, z, chunkCoord);
          let localBlockCoord = localBlockAndChunkCoord[0];
          let localChunkCoord = localBlockAndChunkCoord[1];

          if (render != "no change") {
            chunks[localChunkCoord].data[localBlockCoord].render = render;
          };
          if (alphaValue != "no change") {
            chunks[localChunkCoord].data[localBlockCoord].alphaValue = alphaValue;
          };
        };


      if (block.type == "water") {
        let hopefullyAir = findBlock(x, y + 1, z, extraInfo = true, chunkCoordInput = chunkCoord);

        if (hopefullyAir.type == "air") {
          block.alphaValue = 100;
          block.render = true;

          let didntFindWater = true;

          let subtractY = 1;

          while (didntFindWater) {
            // make sure no blocks underneath are rendered, make top water less transparent
            let hopefullyWater = findBlock(x, y - subtractY, z, extraInfo = true, chunkCoordInput = chunkCoord);

            if (hopefullyWater.type == "water") {
              block.alphaValue += 25;
            } else {didntFindWater = false;}

            if (block.alphaValue >= 255) {
              block.alphaValue = 255;
              break;
            }

            if (subtractY <= -chunkSize[1] || !didntFindWater) {
              break;
            }



            subtractY -= 1;
          }; // end of while loop
        };


          let blockAbove = findBlock(x, y + 1, z, extraInfo = True, chunkCoordInput = chunkCoord);
          let blockBelow = findBlock(x, y - 1, z, extraInfo = True, chunkCoordInput = chunkCoord);
          let blockToRight = findBlock(x + 1, y, z, extraInfo = True, chunkCoordInput = chunkCoord);
          let blockToLeft = findBlock(x - 1, y, z, extraInfo = True, chunkCoordInput = chunkCoord);
          let blockToDown = findBlock(x, y, z + 1, extraInfo = True, chunkCoordInput = chunkCoord);
          let blockToUp = findBlock(x, y, z - 1, extraInfo = True, chunkCoordInput = chunkCoord);

          let above = checkForSolidBlock(blockAbove);
          let below = checkForSolidBlock(blockBelow);
          let toRight = checkForSolidBlock(blockToRight);
          let toLeft = checkForSolidBlock(blockToLeft);
          let toUp = checkForSolidBlock(blockToUp);
          let toDown = checkForSolidBlock(blockToDown);

          let surrounded = false;
          if (toLeft && toUp && toDown && toRight) {surrounded = true;};


          if (above) {
            if (blockBelow.alphaValue < 255) {
              // current block should have alpha, hide the block underneath
              block.alphaValue = 150;
              block.render = true;
              modifyOtherBlock(x, y - 1, z, render = false);
            };

            if (!surrounded) {
              block.render = true;
            };
          } else {
            // no block is above, should probably be rendered
            block.render = true;
          };

          if (below) {
            if (!above) {block.render = true;}
            if (blockBelow.alphaValue < 255) {
              block.alphaValue = 150;
              block.render = true;
              modifyOtherBlock(x, y - 1, z, render = false);
            };
            if (block.render) {modifyOtherBlock(x, y - 1, z, render = false);};

          } else {
            // no block is under this one
            if (!above) {
            block.render = true;
            block.alphaValue = 100;
            };
          }


          };
        };
        
      };







      chunks[chunkCoord].data[blockCoord] = block;
    };
  };
};


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


