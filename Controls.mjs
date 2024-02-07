/*from Worldgen import getBlockCoord, getChunkCoord, generateChunkTerrain
from GlobalVariables import chunks, keys, keysPressed



class Mouse {
    constructor():
        this.x = 0
        this.y = 0
        this.pos = (0, 0)
        this.cameraRelativeX = 0
        this.cameraRelativeZ = 0
        this.cameraRelativePos = (0, 0)
        # block height for mining / placing
        this.selectedY = 0
        this.selectedYChange = 0
        # detection for blocks and stuff
        this.hoveredBlock = {}
        this.hoveredSlotId = 0
        

        this.inPlayerInventory = False
        this.inPlayerHotbar = False
        this.inASlot = False
        # needs to have these two in order to tranfer item data properly
        this.heldItem = {
            "contents": "empty",
            "count": 0
        }

        this.buttons = {
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
}

mouse = Mouse()


def updateMouseAndKeys():
        
    keysPressed = pygame.key.get_just_pressed()

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

    if blockCoord not in chunks[chunkCoord]["data"]:
        generateChunkTerrain(chunkCoord)
    mouse.hoveredBlock["block"] = chunks[chunkCoord]["data"][blockCoord]
    mouse.hoveredBlock["chunkCoord"] = chunkCoord
    mouse.hoveredBlock["blockCoord"] = blockCoord
    
    






    

print("controls initialized")

*/



import { getBlockCoord, getChunkCoord, generateChunkTerrain } from "./Worldgen.mjs";
import { chunks, keys, keysPressed, consoleLog } from "./GlobalVariables.mjs";

class Mouse {
    constructor() {
        this.x = 0;
        this.y = 0;
        this.pos = [0, 0];
        this.cameraRelativeX = 0;
        this.cameraRelativeZ = 0;
        this.cameraRelativePos = [0, 0];
        this.selectedY = 0;
        this.selectedYChange = 0;
        this.hoveredBlock = {};
        this.hoveredSlotId = 0;

        this.inPlayerInventory = false;
        this.inPlayerHotbar = false;
        this.inASlot = false;

        this.heldItem = {
            "contents": "empty",
            "count": 0
        };

        this.buttons = {
            "left": false,
            "middle": false,
            "right": false,
            "pressed": {
                "left": false,
                "middle": false,
                "right": false
            },
            "held": {
                "left": false,
                "middle": false,
                "right": false
            }
        };
    }
}

const mouse = new Mouse();

document.addEventListener("keydown", function (event) {
    if (keysPressed)
    keys[event.key] = true;
    
});

document.addEventListener("keyup", function (event) {
    keys[event.key] = false;
});

function updateMouseAndKeys() {
    const keysPressed = pygame.key.get_just_pressed(); // Assuming pygame functions are appropriately replaced

    mouse.pos = pygame.mouse.get_pos();
    [mouse.x, mouse.y] = mouse.pos;

    mouse.buttons["pressed"]["left"] = false;
    mouse.buttons["pressed"]["middle"] = false;
    mouse.buttons["pressed"]["right"] = false;

    const mouseButtons = pygame.mouse.get_pressed();

    if (!mouse.buttons["left"]) {
        if (mouseButtons[0]) {
            mouse.buttons["pressed"]["left"] = true;
        }
    }

    if (!mouse.buttons["middle"]) {
        if (mouseButtons[1]) {
            mouse.buttons["pressed"]["middle"] = true;
        }
    }

    if (!mouse.buttons["right"]) {
        if (mouseButtons[2]) {
            mouse.buttons["pressed"]["right"] = true;
        }
    }

    mouse.buttons["left"] = mouseButtons[0];
    mouse.buttons["middle"] = mouseButtons[1];
    mouse.buttons["right"] = mouseButtons[2];

    const x = mouse.cameraRelativeX;
    const y = mouse.selectedY;
    const z = mouse.cameraRelativeZ;

    const chunkCoord = getChunkCoord(x, z);
    const blockCoord = getBlockCoord(x, y, z);

    if (!(blockCoord in chunks[chunkCoord]["data"])) {
        generateChunkTerrain(chunkCoord);
    }

    mouse.hoveredBlock["block"] = chunks[chunkCoord]["data"][blockCoord];
    mouse.hoveredBlock["chunkCoord"] = chunkCoord;
    mouse.hoveredBlock["blockCoord"] = blockCoord;
}

console.log("controls initialized");