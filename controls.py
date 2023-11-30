from widelyUsedVariables import camera
import pygame
pygame.display.init()
keys = []
keys.append(pygame.key.get_pressed())
keysPressed = []
for num in range(len(keys[0])):
    keysPressed.append(False)

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = (0, 0)

mouse = Mouse()


def updateMouseAndKeys():
    
    tempKeys = pygame.key.get_pressed()
        
    for keyID in range(len(tempKeys)):
        keysPressed[keyID] = False
        if not keys[0][keyID] and tempKeys[keyID]:
            keysPressed[keyID] = True
    keys[0] = tempKeys

    mouse.pos = pygame.mouse.get_pos()
    mouse.x, mouse.y = mouse.pos[0], mouse.pos[1]

    mouse.cameraRelativeX = mouse.x - camera.x
    mouse.cameraRelativeZ = mouse.y - camera.z
