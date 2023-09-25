

blockSize = (30, 30) # these need to be the same number
chunkSize = (10, 6, 10) # x and z need the same
totalChunkSize = chunkSize[0] * blockSize[0]





def createChunk(chunkCoords = (0, 0)):
    chunkData = {}
    for x in range(10):
        for y in range(chunkSize[1]):
            for z in range(10):
                blockData = 0
                
                blockData = y + 1
                """if y == 0: blockData = 1
                if y == 1: blockData = 2
                if y == 2: blockData = 3
                if y == 3: blockData = 4
                if y == 4: blockData = 5
                if y == 5: blockData = 6"""
                if r.randint(0, 2) == 0:
                    blockData = 0
                
                chunkData[(x, y, z)] = blockData
                chunks[chunkCoords] = chunkData

def generateTest():
    #createChunk((-1, 0))
    createChunk((0, 0))
    createChunk((0, 1))
    createChunk((1, 0))
    createChunk((1, 1))
generateTest()

