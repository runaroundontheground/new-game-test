from worldgen import getBlockCoord, getChunkCoord, generateChunkTerrain
from globalVariables import chunks, keys, keysPressed
import pygame


class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = (0, 0)
        self.cameraRelativeX = 0
        self.cameraRelativeZ = 0
        self.cameraRelativePos = (0, 0)
        # block height for mining / placing
        self.selectedY = 0
        self.selectedYChange = 0
        # detection for blocks and stuff
        self.hoveredBlock = {}
        self.hoveredSlotId = 0
        

        self.inPlayerInventory = False
        self.inPlayerHotbar = False
        self.inASlot = False
        # needs to have these two in order to tranfer item data properly
        self.heldItem = {
            "contents": "empty",
            "count": 0
        }

        self.buttons = {
            "left": False,
            "middle": False,
            "right": False,
            "pressed": {
                "left": False,
                "middle": False,
                "right": False
            },
            "held": {
                "left": False,
                "middle": False,
                "right": False
            }
        }

mouse = Mouse()


def updateMouseAndKeys():
    
    tempKeys = pygame.key.get_pressed()
        
    for keyID, thing in enumerate(tempKeys):
        keysPressed[keyID] = False
        if not keys[0][keyID] and tempKeys[keyID]:
            keysPressed[keyID] = True
    keys[0] = tempKeys

    mouse.pos = pygame.mouse.get_pos()
    mouse.x, mouse.y = mouse.pos[0], mouse.pos[1]

    mouse.buttons["pressed"]["left"] = False
    mouse.buttons["pressed"]["middle"] = False
    mouse.buttons["pressed"]["right"] = False


    mouseButtons = pygame.mouse.get_pressed()

    if not mouse.buttons["left"]:
        if mouseButtons[0]:
            mouse.buttons["pressed"]["left"] = True

    if not mouse.buttons["middle"]:
        if mouseButtons[1]:
            mouse.buttons["pressed"]["middle"] = True

    if not mouse.buttons["right"]:
        if mouseButtons[2]:
            mouse.buttons["pressed"]["right"] = True

    mouse.buttons["left"] = mouseButtons[0]
    mouse.buttons["middle"] = mouseButtons[1]
    mouse.buttons["right"] = mouseButtons[2]

    x = mouse.cameraRelativeX
    y = mouse.selectedY
    z = mouse.cameraRelativeZ
    
    chunkCoord = getChunkCoord(x, z)
    blockCoord = getBlockCoord(x, y, z)
    try:
        chunks[chunkCoord]["data"][blockCoord]
    except:
        generateChunkTerrain(chunkCoord)
    mouse.hoveredBlock["block"] = chunks[chunkCoord]["data"][blockCoord]
    mouse.hoveredBlock["chunkCoord"] = chunkCoord
    mouse.hoveredBlock["blockCoord"] = blockCoord
    
    






    


