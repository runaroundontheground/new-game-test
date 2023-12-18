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
keys = pygame.key.get_pressed()
deltaTime = 1

# extra info for what is required to break blocks
dictOfBlockBreakingStuff = {
    # sediment/shovel effective type blocks
    "grass": {"hardness": 1, "effectiveTool": "shovel"},
    "dirt": {"hardness": 1, "effectiveTool": "shovel"},
    "snowy dirt": {"hardness": 1, "effectiveTool": "shovel"},
    "clay": {"hardness": 1, "effectiveTool": "shovel"},
    "gravel": {"hardness": 1, "effectiveTool": "shovel"},
    "sand": {"hardness": 1, "effectiveTool": "shovel"},
    
    # stone/pickaxe effective type blocks
    "stone": {"hardness": 3, "effectiveTool": "pickaxe"},
    "snowy stone": {"hardness": 3, "effectiveTool": "pickaxe"},
    
    # wood/axe effective type blocks
    "log": {"hardness": 2, "effectiveTool": "axe"},
    "leaves": {"hardness": 0, "effectiveTool": "axe"},

    # any new tools types to add here? this is where they go


    # unbreakable blocks/wouldn't make sense to be able to break them
    "bedrock": {"hardness": "infinity", "effectiveTool": "none"},
    "air": {"hardness": "infinity", "effectiveTool": "none"},
    "water": {"hardness": "infinity", "effectiveTool": "none"}
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
