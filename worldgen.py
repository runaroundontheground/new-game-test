from controls import keysPressed
import random


blockSize = 30 # pixels
chunkSize = (10, 6) # chunkSize[0] is length and width
totalChunkSize = chunkSize[0] * blockSize


chunks = {}
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
                
                if random.randint(0, 2) == 0: # this also needs to be removed, it just
                    blockData = 0 # makes a tile have a 1/3 chance to be air
                
                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData

def generateTest():
    #createChunk((-1, 0))
    createChunk((0, 0))
    createChunk((0, 1))
    createChunk((1, 0))
    createChunk((1, 1))
generateTest()

