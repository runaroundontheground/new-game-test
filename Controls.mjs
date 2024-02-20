import { chunks, keys, keysPressed, showLoadingProgress, canvas, Rect, consoleLog } from "./GlobalVariables.mjs";
showLoadingProgress("loading Controls.mjs");
import { getBlockCoord, getChunkCoord, generateChunkTerrain } from "./Worldgen.mjs";


class Mouse {
    constructor() {
        this.x = 0;
        this.y = 0;
        this.pos = [0, 0];
        this.cameraRelativeX = 0;
        this.cameraRelativeZ = 0;
        this.cameraRelativePos = [0, 0];
        // block height for mining / placing
        this.selectedY = 0;
        this.selectedYChange = 0;
        // detection for blocks and stuff
        this.hoveredBlock = {};
        this.hoveredSlotId = 0;
        

        this.inPlayerInventory = false;
        this.inPlayerHotbar = false;
        this.inASlot = false;
        // needs to have these two in order to tranfer item data properly
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
            }
        };
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

canvas.addEventListener("mousedown", function (event) {

    switch (event.button) {
        case 0:
            mouse.buttons.left = true;
            mouse.buttons.pressed.left = true;
            break;
        case 2:
            mouse.buttons.right = true;
            mouse.buttons.pressed.right = true;
            break;
        break;
    }

    

});

canvas.addEventListener("mouseup", function (event) {

    switch (event.button) {
        case 0:
            mouse.buttons.left = false; break;
        case 2:
            mouse.buttons.right = false; break;
        break;
    }

});

canvas.addEventListener("keydown", function (event) {

    if (!keys[event.key]) {keysPressed[event.key] = true;};
    keys[event.key] = true;
    keys.ctrl = event.ctrlKey;
    keys.shift = event.shiftKey;

    event.preventDefault();

})

canvas.addEventListener("keyup", function (event) {

    keys[event.key] = false;

})
// add an event listener for clicking, keys down, keys up, and maybe some others?

export function updateMouseAndKeys () {

    let x = mouse.cameraRelativeX;
    let y = mouse.selectedY;
    let z = mouse.cameraRelativeZ;
    
    let chunkCoord = getChunkCoord(x, z);
    let blockCoord = getBlockCoord(x, y, z);

    if (chunks[chunkCoord].data[blockCoord] === undefined) {generateChunkTerrain(chunkCoord);};

    mouse.hoveredBlock.block = chunks[chunkCoord].data[blockCoord];
    mouse.hoveredBlock.chunkCoord = chunkCoord;
    mouse.hoveredBlock.blockCoord = blockCoord;


    mouse.buttons.pressed.left = false;
    mouse.buttons.pressed.middle = false;
    mouse.buttons.pressed.right = false;
    for (const key of Object.keys(keysPressed)) {
        keysPressed[key] = false;
    }

}
    
showLoadingProgress("controls initialized");

