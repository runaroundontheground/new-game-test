export function consoleLog(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};
export function showLoadingProgress(message) {
    let loadingDiv = document.getElementById("loadingProgressDiv");
    loadingDiv.innerHTML += message + "<br />";
    loadingDiv.scrollTop = loadingDiv.scrollHeight;
}
showLoadingProgress("loading GlobalVariables.mjs");




export const canvasWidth = 1000;
export const canvasHeight = 500;
export const blockSize = 30; // pixels
export const chunkSize = [10, 30]; // width or length, then height (both in blocks)

export let canvas = document.getElementById("canvas");
canvas.width = canvasWidth;
canvas.height = canvasHeight;
export let ctx = canvas.getContext("2d");
ctx.font = "20px Arial";



export var images = {};


export const totalChunkSize = chunkSize[0] * blockSize;

export const gravity = 1;

export const itemEntitySize = blockSize / 2;

export let chunks = {};

export let keys = {};
export let keysPressed = {};

export let deltaTime = 1;

export function Rect(x, y, width, height) {
    let rect = {
        "x": x,
        "y": y,
        "width": width,
        "height": height
    }
    rect.collide = {};
    rect.collide.rect = function (otherRect) {
        let myRect = rect;

        let meetsX = false;
        let meetsY = false;

        if ((otherRect.x <= myRect.x + myRect.width) && (otherRect.x + otherRect.width >= myRect.x)) {
            meetsX = true;
        };
        if ((otherRect.y <= myRect.y + myRect.height) && (otherRect.y + otherRect.height >= myRect.y)) {
            meetsY = true;
        }

        if (meetsX && meetsY) {
            return true;
        };
        return false;
    };
    rect.collide.point = function (x, y) {
        let myRect = rect;

        let meetsX = false;
        let meetsY = false;


        if ((x >= myRect.x) && (x <= myRect.x + myRect.width)) {
            meetsX = true;
        };
        if ((y >= myRect.y) && (y <= myRect.y + myRect.height)) {
            meetsY = true;
        }

        if (meetsX && meetsY) {
            return true;
        };
        return false;
    }

    return rect
}

export const dictOfBlockBreakingStuff = {
    "grass": { "hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": true },
    "dirt": { "hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": true },
    "snowy dirt": { "hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": true },
    "clay": { "hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": true },
    "gravel": { "hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": true },
    "sand": { "hardness": 1, "effectiveTool": "shovel", "dropsWithNoTool": true },
    "stone": { "hardness": 2, "effectiveTool": "pickaxe", "dropsWithNoTool": false },
    "snowy stone": { "hardness": 2, "effectiveTool": "pickaxe", "dropsWithNoTool": false },
    "cobblestone": { "hardness": 2, "effectiveTool": "pickaxe", "dropsWithNoTool": false },
    "log": { "hardness": 2, "effectiveTool": "axe", "dropsWithNoTool": true },
    "planks": { "hardness": 2, "effectiveTool": "axe", "dropsWithNoTool": true },
    "leaves": { "hardness": 0, "effectiveTool": "axe", "dropsWithNoTool": false },
    "crafting table": { "hardness": 1, "effectiveTool": "axe", "dropsWithNoTool": true },
    "bedrock": { "hardness": "infinity", "effectiveTool": "none", "dropsWithNoTool": false },
    "air": { "hardness": "infinity", "effectiveTool": "none", "dropsWithNoTool": false },
    "water": { "hardness": "infinity", "effectiveTool": "none", "dropsWithNoTool": false }
};

export const canvasWidthInChunks = Math.floor(canvasWidth / totalChunkSize);
export const canvasHeightInChunks = Math.floor(canvasHeight / totalChunkSize);

export let entities = [];
export let projectiles = [];

export let items = {};
export let itemIcons = {};

export const fps = 60;
export let timeScale = 1

export const maxStackSize = 64;

export let recipes = {
    2: {
        "exact": {},
        "nearExact": {},
        "shapeless": {}
    },
    3: {
        "exact": {},
        "nearExact": {},
        "shapeless": {}
    }
};

export const listOfIntermediateItems = ["stick"];

export let listOfBlockNames = Object.keys(dictOfBlockBreakingStuff);

class Camera {
    constructor() {
        this.smoothness = 10;
        this.centerTheCamera = [canvasWidth / 2, canvasHeight / 2];
        this.x = -this.centerTheCamera[0];
        this.y = 0;
        this.z = -this.centerTheCamera[1];
        this.currentChunk = [0, 0];
    }
}

export let camera = new Camera();

class Random {
    constructor() {
        this.integer = this.integer.bind(this);
        this.float = this.float.bind(this);
    };

    integer(startInt, endInt) {
        return Math.floor(Math.random() * (endInt - startInt + 1) + startInt);
    }
    float(startNum, endNum) {
        return Math.random() * (endNum - startNum) + startNum;
    }
};

export let random = new Random();


class Trig {
    constructor() {

    }
}

export let trig = new Trig();

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
        this.heldSlot = {
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

export let mouse = new Mouse();




showLoadingProgress("global variables initialized");
