import pygame, math
pygame.display.init()
pygame.font.init()

screenWidth, screenHeight = 1000, 500

font = pygame.font.Font(size = 24)

blockSize = 30 # pixels
chunkSize = (10, 30) # width or length, then height (both in blocks)

totalChunkSize = chunkSize[0] * blockSize

gravity = 1

itemEntitySize = blockSize/2

chunks = {}

keys = []
keys.append(pygame.key.get_pressed())
keysPressed = []
for index, num in enumerate(keys[0]):
    keysPressed.append(False)

deltaTime = 1


# extra info for what is required to break blocks
dictOfBlockBreakingStuff = {
    # sediment/shovel effective type blocks
    "grass": {"hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": True},
    "dirt": {"hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": True},
    "snowy dirt": {"hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": True},
    "clay": {"hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": True},
    "gravel": {"hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": True},
    "sand": {"hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": True},
    
    # stone/pickaxe effective type blocks
    "stone": {"hardness": 3, "effectiveTool": "pickaxe", "dropsWithNoTool": False},
    "snowy stone": {"hardness": 3, "effectiveTool": "pickaxe", "dropsWithNoTool": False},
    
    # wood/axe effective type blocks
    "log": {"hardness": 2, "effectiveTool": "axe", "dropsWithNoTool": True},
    "leaves": {"hardness": 0, "effectiveTool": "axe", "dropsWithNoTool": True},

    # any new tools types to add here? this is where they go


    # unbreakable blocks/wouldn't make sense to be able to break them
    "bedrock": {"hardness": "infinity", "effectiveTool": "none", "dropsWithNoTool": False},
    "air": {"hardness": "infinity", "effectiveTool": "none", "dropsWithNoTool": False},
    "water": {"hardness": "infinity", "effectiveTool": "none", "dropsWithNoTool": False}
}



screenWidthInChunks = math.floor( screenWidth / totalChunkSize )
screenHeightInChunks = math.floor( screenHeight / totalChunkSize )

# every entity will be here, besides player
# hopefully doing the stuff for these entities isn't super laggy
# need to add a for loop that does a standard function for each entity,
# like entity.runSelf(deltaTime) or something
entities = []
projectiles = []

# dict with all items in it
items = {}
itemIcons = {}

FPS = 60

maxStackSize = 64

listOfBlockNames = [
    "air", "grass", "dirt", "snowy dirt", "stone", "snowy stone", "sand",
    "clay", "gravel", "water", "bedrock", "log", "leaves"
]


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



def rotatePoint(surface, angle, pivot, offset = pygame.math.Vector2(0, 0)):
    """Rotate the surface around the pivot point.
    thank you other people, for figuring this out for me so i can copy it
    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center = pivot + rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.
