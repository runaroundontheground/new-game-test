
function consoleLog(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};

function showLoadingProgress(message) {
    let loadingDiv = document.getElementById("loadingProgressDiv");
    loadingDiv.innerHTML += message + "<br />";
    loadingDiv.scrollTop = loadingDiv.scrollHeight;
}

showLoadingProgress("started loading images");

import { images, canvasWidth, canvasHeight } from "./GlobalVariables.mjs";



let imageUrlsAndNames = {
    "stick": "./Images/stick.png",
    "stone axe": "./Images/tools/stone axe.png",
    "stone pickaxe": "./Images/tools/stone pickaxe.png",
    "wood axe": "./Images/tools/wood axe.png",
    "wood pickaxe": "./Images/tools/wood pickaxe.png",
    "inventory arrow": "./Images/arrow.png"
};



let allImagesLoaded = false;
let nonUIImagesLoaded = false;
let loadingUIImages = false;


var currentNumberOfLoadedImages = 0;
let UIElements = 6;
let totalNumberOfImages = Object.keys(imageUrlsAndNames).length + UIElements;

for (const key of Object.keys(imageUrlsAndNames)) {
    let image = new Image();
    image.src = imageUrlsAndNames[key];
    image.onload = function () {
        currentNumberOfLoadedImages += 1;
    }

    images[key] = image;

};

function makePlayerInventoryImages() {
    let widthOfInventoryInSlots = 9;
    let heightOfInventoryInSlots = 3;


    let inventoryCanvas = document.createElement("canvas");
    let inventoryCanvasContext = inventoryCanvas.getContext("2d");

    let hotbarCanvas = document.createElement("canvas");
    let hotbarCanvasContext = hotbarCanvas.getContext("2d");

    let inventoryWidthInPixels = canvasWidth / 3;

    let slotSizeInPixels = Math.round(inventoryWidthInPixels / widthOfInventoryInSlots);

    let gapBetweenSlots = Math.round(slotSizeInPixels / 5);

    inventoryWidthInPixels += gapBetweenSlots; // fix for a thing?


    let backgroundColor = "rgb(150, 150, 150)";
    let slotColor = "rgb(125, 125, 125)";
    let slotOutlineColor = "rgb(175, 175, 175)";
    let alphaForUI = 1;


    let emptySpaceBetweenItemAndSlotBorder = gapBetweenSlots / 2


    inventoryWidthInPixels += gapBetweenSlots * (widthOfInventoryInSlots + 1)

    let inventoryHeightInPixels = (slotSizeInPixels * heightOfInventoryInSlots)
    inventoryHeightInPixels += gapBetweenSlots * (heightOfInventoryInSlots + 1)

    // add some more height to the inventory for crafting grid and armor? if added
    let craftingAndArmorHeightInSlots = 4.25

    let craftingAndArmorWidthInPixels = inventoryWidthInPixels
    let craftingAndArmorHeightInPixels = (slotSizeInPixels * craftingAndArmorHeightInSlots)
    craftingAndArmorHeightInPixels += (gapBetweenSlots * craftingAndArmorHeightInSlots + 1)

    let craftingTableSizeInPixels = [Math.round(craftingAndArmorWidthInPixels), Math.round(craftingAndArmorHeightInPixels)]


    let craftingAndArmorSizeInPixels = [Math.round(craftingAndArmorWidthInPixels), Math.round(craftingAndArmorHeightInPixels)]
    // create the crafting and armor image, only the background first though


    let craftingAndArmorImage = new Image();
    let slotImage = new Image();
    let hotbarImage = new Image();
    let inventoryImage = new Image();
    let slotOutlineImage = new Image();
    let craftingTableImage = new Image();

    // make the crafting/armor image
    let craftingAndArmorCanvas = document.createElement("canvas");
    let craftingAndArmorCanvasContext = craftingAndArmorCanvas.getContext("2d");
    craftingAndArmorCanvas.width = craftingAndArmorWidthInPixels;
    craftingAndArmorCanvas.height = craftingAndArmorHeightInPixels;

    craftingAndArmorCanvasContext.fillStyle = backgroundColor;
    craftingAndArmorCanvasContext.globalAlpha = alphaForUI;

    craftingAndArmorCanvasContext.fillRect(0, 0, craftingAndArmorCanvas.width, craftingAndArmorCanvas.height);

    // make the crafting table image
    let craftingTableCanvas = document.createElement("canvas");
    let craftingTableCanvasContext = craftingTableCanvas.getContext("2d");
    craftingTableCanvas.width = craftingTableSizeInPixels[0];
    craftingTableCanvas.height = craftingTableSizeInPixels[1];

    craftingTableCanvasContext.fillRect(0, 0, craftingTableCanvas.width, craftingTableCanvas.height);

    // make the inventory image
    let inventorySizeInPixels = [Math.round(inventoryWidthInPixels), Math.round(inventoryHeightInPixels)]
    inventoryCanvas.width = inventorySizeInPixels[0];
    inventoryCanvas.height = inventorySizeInPixels[1];

    inventoryCanvasContext.fillStyle = backgroundColor;
    inventoryCanvasContext.fillRect(0, 0, inventoryCanvas.width, inventoryCanvas.height);



    // make the slot image
    let slotCanvas = document.createElement("canvas");
    let slotCanvasContext = slotCanvas.getContext("2d");
    slotCanvas.width = slotSizeInPixels;
    slotCanvas.height = slotSizeInPixels;
    slotCanvasContext.fillStyle = slotColor;
    slotCanvasContext.fillRect(0, 0, slotCanvas.width, slotCanvas.height);
    slotImage.src = slotCanvas.toDataURL();

    // make the slot outline image
    let slotOutlineCanvas = document.createElement("canvas");
    let slotOutlineCanvasContext = slotOutlineCanvas.getContext("2d");
    slotOutlineCanvas.width = slotSizeInPixels + gapBetweenSlots * 2;
    slotOutlineCanvas.height = slotSizeInPixels + gapBetweenSlots * 2;
    slotOutlineCanvasContext.strokeStyle = slotOutlineColor;
    slotOutlineCanvasContext.lineWidth = 5;
    slotOutlineCanvasContext.strokeRect(0, 0, slotOutlineCanvas.width, slotOutlineCanvas.height);
    slotOutlineImage.src = slotOutlineCanvas.toDataURL();

    // make hotbar image
    let hotbarSizeInPixels = [Math.round(inventorySizeInPixels[0]), Math.round(slotSizeInPixels + (gapBetweenSlots * 2))]
    hotbarCanvas.width = hotbarSizeInPixels[0];
    hotbarCanvas.height = hotbarSizeInPixels[1];
    hotbarCanvasContext.fillStyle = backgroundColor;
    hotbarCanvasContext.fillRect(0, 0, hotbarCanvas.width, hotbarCanvas.height);

    // result slot for 2x2 grid
    let slotX = ((widthOfInventoryInSlots) * slotSizeInPixels)
    let slotY = (slotSizeInPixels * 1.5)

    craftingAndArmorCanvasContext.fillStyle = slotColor;
    craftingAndArmorCanvasContext.fillRect(slotX, slotY, slotSizeInPixels, slotSizeInPixels);

    // result slot for 3x3 grid
    slotX = ((widthOfInventoryInSlots - 2) * slotSizeInPixels) + slotSizeInPixels * 1.7
    slotY = (slotSizeInPixels * 2.1)

    craftingTableCanvasContext.fillStyle = slotColor;
    craftingTableCanvasContext.fillRect(slotX, slotY, slotSizeInPixels, slotSizeInPixels);



    // draw things to the 2x2 crafting grid
    for (let y = 0; y < 2; y++) {
        for (let x = 0; x < 2; x++) {

            slotX = ((widthOfInventoryInSlots - 4) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
            slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))


            craftingAndArmorCanvasContext.fillStyle = slotColor;
            craftingAndArmorCanvasContext.fillRect(slotX, slotY, slotSizeInPixels, slotSizeInPixels);

        };
    };

    // draw the crafting table image things
    for (let y = 0; y < 3; y++) {
        for (let x = 0; x < 3; x++) {
            slotX = ((widthOfInventoryInSlots - 6) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
            slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))


            craftingTableCanvasContext.fillStyle = slotColor;
            craftingTableCanvasContext.fillRect(slotX, slotY, slotSizeInPixels, slotSizeInPixels);

        };
    };

    // arrow for 2x2 grid
    let arrowX = (widthOfInventoryInSlots - 0.6) * slotSizeInPixels;
    let arrowY = (slotSizeInPixels * 0.75) + slotSizeInPixels * 1.1;
    let arrowWidth = arrowX + (slotSizeInPixels / 3);
    let scale = images["inventory arrow"].naturalWidth / arrowWidth;
    let arrowHeight = images["inventory arrow"].naturalHeight / scale;


    craftingAndArmorCanvasContext.drawImage(images["inventory arrow"], arrowX, arrowY, arrowWidth, arrowHeight);

    craftingAndArmorImage.src = craftingAndArmorCanvas.toDataURL();


    // arrow for 3x3 grid
    arrowX = (widthOfInventoryInSlots - 0.60) * slotSizeInPixels - slotSizeInPixels * 0.8;
    arrowY = (slotSizeInPixels * 0.75) + slotSizeInPixels * 1.1 + slotSizeInPixels / 1.8

    craftingTableCanvasContext.drawImage(images["inventory arrow"], arrowX, arrowY, arrowWidth, arrowHeight);
    craftingTableImage.src = craftingTableCanvas.toDataURL();

    // draw slots to the inventory
    for (let y = 0; y < heightOfInventoryInSlots; y++) {
        for (let x = 0; x < widthOfInventoryInSlots; x++) {

            slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
            slotY = (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))

            inventoryCanvasContext.fillStyle = slotColor;
            inventoryCanvasContext.fillRect(slotX, slotY, slotSizeInPixels, slotSizeInPixels);

        };
    };
    inventoryImage.src = inventoryCanvas.toDataURL();

    // draw slots on the hotbar?

    for (let x = 0; x < widthOfInventoryInSlots; x++) {

        slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
        slotY = gapBetweenSlots;

        hotbarCanvasContext.fillStyle = slotColor;
        hotbarCanvasContext.fillRect(slotX, slotY, slotSizeInPixels, slotSizeInPixels);
    };
    hotbarImage.src = hotbarCanvas.toDataURL();

    images["UI/" + "inventory"] = inventoryImage;
    images["UI/" + "crafting table"] = craftingTableImage;
    images["UI/" + "hotbar"] = hotbarImage;
    images["UI/" + "slot"] = slotImage;
    images["UI/" + "slot outline"] = slotOutlineImage;
    images["UI/" + "crafting and armor"] = craftingAndArmorImage;

    inventoryImage.onload = function () { currentNumberOfLoadedImages += 1; };
    craftingTableImage.onload = function () { currentNumberOfLoadedImages += 1; };
    hotbarImage.onload = function () { currentNumberOfLoadedImages += 1; };
    slotImage.onload = function () { currentNumberOfLoadedImages += 1; };
    slotOutlineImage.onload = function () { currentNumberOfLoadedImages += 1; };
    craftingAndArmorImage.onload = function () { currentNumberOfLoadedImages += 1; };

};





// wait one second between each check
function checkForImagesLoading() {
    if (currentNumberOfLoadedImages >= totalNumberOfImages - UIElements) {
        nonUIImagesLoaded = true;
    }

    if (nonUIImagesLoaded && !loadingUIImages) {
        makePlayerInventoryImages();
        loadingUIImages = true;
    }

    if (currentNumberOfLoadedImages === totalNumberOfImages) {
        allImagesLoaded = true;
        showLoadingProgress("images have been loaded");
        clearInterval(interval);
        interval = null;
    }
    showLoadingProgress(currentNumberOfLoadedImages + "/" + totalNumberOfImages);
}


let interval = setInterval(checkForImagesLoading, 1000);


export { allImagesLoaded };