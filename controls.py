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
        self.cameraRelativeX = 0
        self.cameraRelativeZ = 0
        self.cameraRelativePos = (0, 0)

        self.buttons = {
            "left": False,
            "middle": False,
            "right": False,
            "pressed": {
                "left": False,
                "middle": False,
                "right": False
            }
        }

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

    mouse.buttons["pressed"]["left"] = False
    mouse.buttons["pressed"]["middle"] = False
    mouse.buttons["pressed"]["right"] = False

    mouseButtons = pygame.mouse.get_pressed()

    if not mouse.buttons["left"]:
        if not mouseButtons[0]:
            mouse.buttons["pressed"]["left"] = True
    if not mouse.buttons["middle"]:
        if not mouseButtons[1]:
            mouse.buttons["pressed"]["middle"] = True
    if not mouse.buttons["right"]:
        if not mouseButtons[2]:
            mouse.buttons["pressed"]["right"] = True

    mouse.buttons["left"] = mouseButtons[0]
    mouse.buttons["middle"] = mouseButtons[1]
    mouse.buttons["right"] = mouseButtons[2]





    


