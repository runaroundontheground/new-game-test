screenWidth, screenHeight = 1000, 500

blockSize = 30 # pixels
chunkSize = (10, 6) # chunkSize[0] is length and width
totalChunkSize = chunkSize[0] * blockSize

gravity = 0.3

chunks = {}
import pygame
pygame.display.init()
keys = pygame.key.get_pressed()

import math

screenWidthInChunks = math.floor( screenWidth / totalChunkSize )
screenHeightInChunks = math.floor( screenHeight / totalChunkSize )


class Camera():
    def __init__(self):
        self.smoothness = 10
        self.centerTheCamera = (screenWidth/2, screenHeight/2)
        self.x = -self.centerTheCamera[0]
        self.y = 0
        self.z = -self.centerTheCamera[1]
        self.currentChunk = (0, 0)
        # do i want to have camera shake later?
        # self.shakeStrength = 0
        # self.shakeDuration = 0
    

camera = Camera()