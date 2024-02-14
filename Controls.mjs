import { chunks, keys, keysPressed, showLoadingProgress, canvas, Rect } from "./GlobalVariables.mjs";
showLoadingProgress("loading Controls.mjs");
import { getBlockCoord, getChunkCoord, generateChunkTerrain } from "./Worldgen.mjs";


class Mouse {
    constructor() {
        this.x = 0
        this.y = 0
        this.pos = [0, 0]
        this.cameraRelativeX = 0
        this.cameraRelativeZ = 0
        this.cameraRelativePos = [0, 0]
        // block height for mining / placing
        this.selectedY = 0;
        this.selectedYChange = 0;
        // detection for blocks and stuff
        this.hoveredBlock = {}
        this.hoveredSlotId = 0
        

        this.inPlayerInventory = false
        this.inPlayerHotbar = false
        this.inASlot = false
        // needs to have these two in order to tranfer item data properly
        this.heldItem = {
            "contents": "empty",
            "count": 0
        }

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
        }
    };
}

export var mouse = new Mouse();

canvas.addEventListener("mousemove", function (event) {
    const canvasRect = canvas.getBoundingClientRect();
    const x = event.clientX - canvasRect.left;
    const y = event.clientY - canvasRect.top;
    mouse.pos = [x, y];
    mouse.x = x;
    mouse.y = y;
});
// add an event listener for clicking, keys down, keys up, and maybe some others?

export function updateMouseAndKeys () {

    let x = mouse.cameraRelativeX;
    let y = mouse.selectedY;
    let z = mouse.cameraRelativeZ;
    
    let chunkCoord = getChunkCoord(x, z);
    let blockCoord = getBlockCoord(x, y, z);

    if (chunks[chunkCoord].data[blockCoord] === undefined) {generateChunkTerrain(chunkCoord);};

    mouse.hoveredBlock["block"] = chunks[chunkCoord]["data"][blockCoord]
    mouse.hoveredBlock["chunkCoord"] = chunkCoord
    mouse.hoveredBlock["blockCoord"] = blockCoord


    mouse.buttons["pressed"]["left"] = false
    mouse.buttons["pressed"]["middle"] = false
    mouse.buttons["pressed"]["right"] = false


    mouseButtons = pygame.mouse.get_pressed()

    if not mouse.buttons["left"]:
        if mouseButtons[0]:
            mouse.buttons["pressed"]["left"] = true

    if not mouse.buttons["middle"]:
        if mouseButtons[1]:
            mouse.buttons["pressed"]["middle"] = true

    if not mouse.buttons["right"]:
        if mouseButtons[2]:
            mouse.buttons["pressed"]["right"] = true

    mouse.buttons["left"] = mouseButtons[0]
    mouse.buttons["middle"] = mouseButtons[1]
    mouse.buttons["right"] = mouseButtons[2]
}
    
showLoadingProgress("controls initialized");

