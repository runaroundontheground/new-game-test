screenWidth, screenHeight = 1200, 600

blockSize = 30 # pixels
chunkSize = (10, 6) # chunkSize[0] is length and width
totalChunkSize = chunkSize[0] * blockSize

chunks = {}

import math

screenWidthInChunks = math.floor( screenWidth / totalChunkSize )
screenHeightInChunks = math.floor( screenHeight / totalChunkSize)

print(screenWidthInChunks)
print(screenHeightInChunks)