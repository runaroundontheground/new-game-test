import pygame
pygame.init()

keys = pygame.key.get_pressed()
keysPressed = []
for num in range(len(keys)):
    keysPressed.append(False)

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = (0, 0)

mouse = Mouse()

def updateKeys():
    global keys
    tempKeys = pygame.key.get_pressed()
        
    for keyID in range(len(tempKeys)):
        keysPressed[keyID] = False
        if not keys[keyID] and tempKeys[keyID]:
            keysPressed[keyID] = True
    keys = tempKeys

def updateMouse():
    mouse.pos = pygame.mouse.get_pos()
    mouse.x, mouse.y = mouse.pos[0], mouse.pos[1]