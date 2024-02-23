import { blockSize, gravity, maxStackSize, itemEntitySize, Rect, consoleLog, showLoadingProgress, camera } from "./GlobalVariables.mjs";
import { findBlock } from "./Worldgen.mjs";

showLoadingProgress("loading Entities.mjs");

// base entity with no ai
class Entity {
    constructor(x, y, z, xv, yv, zv) {
        this.x = x || 0; this.xv = xv || 0;
        this.y = y || 0; this.yv = yv || 0;
        this.z = z || 0; this.zv = zv || 0;

        this.deleteMe = false;

        this.width = blockSize;
        this.height = this.width;

        this.rect = Rect(0, 0, this.width, this.height);


    };
};

export class ItemEntity extends Entity {
    constructor(x, y, z, xv, yv, zv, count, itemData) {


        super(x, y, z, xv, yv, zv);

        this.itemData = itemData
        this.count = count

        this.width = itemEntitySize;
        this.height = itemEntitySize;
        this.rect = Rect(0, 0, this.width, this.height);

        this.renderData = {
            "drawType": "image",
            "position": [0, 0],
            "width": this.width,
            "height": this.height
        }

        this.terminalVelocity = -10;

        this.timers = {
            "pickupDelay": 20
        }




        this.positionUpdates = function (player) {

            let a = findBlock(this.x, this.y - this.height, this.z, ignoreWater = true)
            let b = findBlock(this.x, this.y - this.height, this.z + this.width, ignoreWater = true)
            let c = findBlock(this.x + this.width, this.y - this.height, this.z, ignoreWater = true)
            let d = findBlock(this.x + this.width, this.y - this.height, this.z + this.width, ignoreWater = true)
            let blockBelow = false;

            if (a || b || c || d) { blockBelow = true; };

            if (blockBelow) {
                this.yv = 0;

                // snap this onto the block it should be on
                this.y = Math.floor(this.y / blockSize) * blockSize + this.height;

                // do friction
                this.xv -= this.xv / 15;
                this.zv -= this.zv / 15;

                if (Math.abs(this.xv) < 0.1) { this.xv = 0; };
                if (Math.abs(this.zv) < 0.1) { this.zv = 0; };

            } else {
                if (this.yv > this.terminalVelocity) { this.yv -= gravity; };
            };


            if (this.xv != 0) {

                let sideValue = this.x;
                let blockToSide = false;

                if (this.xv > 0) { sideValue += this.width; };

                let collision = {
                    "corner 1": findBlock(sideValue, this.y, this.z),
                    "corner 2": findBlock(sideValue, this.y, this.z + this.width),
                    "corner 3": findBlock(sideValue, this.y - this.height, this.z),
                    "corner 4": findBlock(sideValue, this.y - this.height, this.z + this.width),
                };

                for (const cornerPassedCollision of Object.values(collision)) {
                    if (cornerPassedCollision) { blockToSide = true; break; }
                };


                if (blockToSide) { this.x -= this.xv; this.xv = 0; };
            };


            if (this.zv != 0) {

                let sideValue = this.z;
                let blockToSide = false;

                if (this.zv > 0) { sideValue += this.width; };

                let collision = {
                    "corner 1": findBlock(this.x, this.y, sideValue),
                    "corner 2": findBlock(this.x + this.width, this.y, sideValue),
                    "corner 3": findBlock(this.x, this.y - this.height, sideValue),
                    "corner 4": findBlock(this.x + this.width, this.y - this.height, sideValue),
                };

                for (const cornerPassedCollision of Object.values(collision)) {
                    if (cornerPassedCollision) { blockToSide = true; break; }
                }


                if (blockToSide) { this.z -= this.zv; this.zv = 0; };
            };
        };

        let insideABlock = findBlock(this.x + this.width / 2, this.y - this.height / 2, this.z + this.width / 2, ignoreWater = true)
        if (insideABlock) { this.y += blockSize / 2; };


        // update image things
        
        let y = 0;
        y = Math.floor(this.y / blockSize);
        if (y >= chunkSize[1]) {y = chunkSize[1] - 1};
        if (y < 0) {y = 0};

        this.renderData.x = this.x - camera.x;
        this.renderData.y = this.z - camera.z;
        this.renderData.yLayer = y;

        
        this.x += this.xv;
        this.y += this.yv;
        this.z += this.zv;

        this.rect.x = this.x;
        this.rect.y = this.z;


        this.runTimers = function () {
            for (const key of Object.keys(this.timers)) {
                let value = this.timers[key];

                if (value > 0) { value -= 1; };
                if (value < 0) { value += 1; };

                this.timers[key] = value;
            };
        };

        this.playerInteraction = function (player) {
            if (this.timers.pickupDelay == 0) {

                if (this.rect.collide.rect(player.rect)) {

                    let itemPickedUp = player.giveItem(this.itemData, this.count);
                    if (itemPickedUp) { this.deleteMe = true; }
                };
            };
        };

        this.doStuff = function (player) {

            if (!this.deleteMe) {
                this.positionUpdates(player);
                this.runTimers();
                this.playerInteraction(player);
            };
        };
    };
};









showLoadingProgress("Entities.mjs initialized");
