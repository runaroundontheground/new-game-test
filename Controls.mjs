import { chunks, keys, keysPressed, showLoadingProgress, canvas, Rect, consoleLog, mouse } from "./GlobalVariables.mjs";
showLoadingProgress("loading Controls.mjs");
import { getBlockCoord, getChunkCoord, generateChunkTerrain } from "./Worldgen.mjs";

let inFocus = false;

canvas.addEventListener("mouseenter", function (event) {
    inFocus = true;
})
canvas.addEventListener("mouseleave", function (event) {
    inFocus = false;
})

canvas.addEventListener("mousemove", function (event) {
    const canvasRect = canvas.getBoundingClientRect();
    const x = event.clientX - canvasRect.left;
    const y = event.clientY - canvasRect.top;
    mouse.pos = [x, y];
    mouse.x = x;
    mouse.y = y;
});


addEventListener("contextmenu", function (event) {
    if (inFocus) { // disable the context menu while playing game
    event.preventDefault();
    };
})

window.addEventListener("mousedown", function (event) {

    if (inFocus) {

        event.preventDefault();

        switch (event.button) {
            case 0:
                mouse.buttons.left = true;
                mouse.buttons.pressed.left = true;
                break;
            case 2:
                mouse.buttons.right = true;
                mouse.buttons.pressed.right = true;
                break;
        };
    };
});

window.addEventListener("mouseup", function (event) {

    if (inFocus) {
        switch (event.button) {
            case 0:
                mouse.buttons.left = false; break;
            case 2:
                mouse.buttons.right = false; break;
        }
    };

});

window.addEventListener("keydown", function (event) {

    if (inFocus) {
        event.preventDefault();

        if (!keys[event.key]) { keysPressed[event.key] = true; };
        keys[event.key] = true;
        keys.ctrl = event.ctrlKey;
        keys.shift = event.shiftKey;

    };

})

window.addEventListener("keyup", function (event) {

    if (inFocus) { keys[event.key] = false; };

})
// add an event listener for clicking, keys down, keys up, and maybe some others?

export function updateMouseAndKeys() {

    let x = mouse.cameraRelativeX;
    let y = mouse.selectedY;
    let z = mouse.cameraRelativeZ;

    let chunkCoord = getChunkCoord(x, z);
    let blockCoord = getBlockCoord(x, y, z);

    if (chunks[chunkCoord].data[blockCoord] === undefined) { generateChunkTerrain(chunkCoord); };

    mouse.hoveredBlock = chunks[chunkCoord].data[blockCoord];
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

