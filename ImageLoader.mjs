
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

export var allImagesLoaded = false;
export var images = {};

let imageUrlsAndNames = {
    "stick": "./Images/stick.png",
    "stone axe": "./Images/tools/stone axe.png",
    "stone pickaxe": "./Images/tools/stone pickaxe.png",
    "wood axe": "./Images/tools/wood axe.png",
    "wood pickaxe": "./Images/tools/wood pickaxe.png",
    "inventory arrow": "./Images/arrow.png"
};






let currentNumberOfLoadedImages = 0;
let totalNumberOfImages = Object.keys(imageUrlsAndNames).length;

for (const key of Object.keys(imageUrlsAndNames)) {
    let image = new Image();
    image.src = imageUrlsAndNames[key];
    image.onload = function () {
        currentNumberOfLoadedImages += 1;

        consoleLog(currentNumberOfLoadedImages);
    }

    images[key] = image;

};


function makePlayerInventoryImages() {
    let widthOfInventoryInSlots = 9;
    let heightOfInventoryInSlots = 3;

    let newCanvas = document.createElement("canvas");
    let context = newCanvas.getContext("2d");

    let canvasWidth = document.getElementById("canvas").width;
    let canvasHeight = document.getElementById("canvas").height;

    let inventoryWidthInPixels = canvasWidth / 3;
    let slotSizeInPixels = Math.round(inventoryWidthInPixels / widthOfInventoryInSlots);

    let gapBetweenSlots = Math.round(slotSizeInPixels / 5);


    let backgroundColor = "rgb(150, 150, 150)";
    let slotColor = "rgb(125, 125, 125)";
    let slotOutlineColor = "rgb(175, 175, 175)";
    let alphaForUI = 255;

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
    newCanvas.width = craftingAndArmorSizeInPixels[0];
    newCanvas.height = craftingAndArmorSizeInPixels[1];


    let craftingAndArmorImage = new Image();
    let slotImage = new Image();
    let hotbarImage = new Image();
    let inventoryImage = new Image();
    let slotOutlineImage = new Image();
    let craftingTableImage = new Image();

    // make the crafting/armor image
    context.fillStyle = backgroundColor
    context.globalAlpha = alphaForUI;
    context.fillRect(0, 0, newCanvas.width, newCanvas.height);
    craftingAndArmorImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);

    // make the crafting table image
    newCanvas.width = craftingTableSizeInPixels[0];
    newCanvas.height = craftingTableSizeInPixels[1];

    context.fillRect(0, 0, newCanvas.width, newCanvas.height);
    craftingTableImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);

    // make the inventory image
    let inventorySizeInPixels = (Math.round(inventoryWidthInPixels), Math.round(inventoryHeightInPixels))
    newCanvas.width = inventorySizeInPixels[0];
    newCanvas.height = inventorySizeInPixels[1];

    context.fillRect(0, 0, newCanvas.width, newCanvas.height);
    inventoryImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);

    // make the slot image
    newCanvas.width = slotSizeInPixels;
    newCanvas.height = slotSizeInPixels;
    context.fillStyle = slotColor
    context.fillRect(0, 0, newCanvas.width, newCanvas.height);
    slotImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);

    // make the slot outline image
    newCanvas.width = slotSizeInPixels + gapBetweenSlots * 2;
    newCanvas.height = slotSizeInPixels + gapBetweenSlots * 2;
    context.strokeStyle = slotOutlineColor;
    context.strokeRect(0, 0, newCanvas.width, newCanvas.height);
    slotOutlineImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);

    // make hotbar image
    let hotbarSizeInPixels = (Math.round(inventorySizeInPixels[0]), Math.round(slotSizeInPixels + (gapBetweenSlots * 2)))
    newCanvas.width = hotbarSizeInPixels[0];
    newCanvas.height = hotbarSizeInPixels[1];
    context.fillStyle = backgroundColor;
    context.fillRect(0, 0, newCanvas.width, newCanvas.height);
    hotbarImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);

    // result slot for 2x2 grid
    let slotX = ((widthOfInventoryInSlots) * slotSizeInPixels)
    let slotY = (slotSizeInPixels * 1.5)

    newCanvas.width = craftingAndArmorWidthInPixels;
    newCanvas.height = craftingAndArmorHeightInPixels;
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);
    context.drawImage(craftingAndArmorImage, 0, 0);
    context.drawImage(slotImage, slotX, slotY);
    craftingAndArmorImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);

    // result slot for 3x3 grid
    slotX = ((widthOfInventoryInSlots - 2) * slotSizeInPixels) + slotSizeInPixels * 1.7
    slotY = (slotSizeInPixels * 2.1)

    newCanvas.width = craftingTableSizeInPixels[0];
    newCanvas.height = craftingTableSizeInPixels[1];
    context.drawImage(craftingTableImage, 0, 0);
    context.drawImage(slotImage, slotX, slotY);
    craftingTableImage.src = newCanvas.toDataURL();
    context.clearRect(0, 0, newCanvas.width, newCanvas.height);




    // draw things to the 2x2 crafting grid
    for (let y = 0; y < 2; y++) {
        for (let x = 0; x < 2; x++) {

            slotX = ((widthOfInventoryInSlots - 4) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
            slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))


            newCanvas.width = craftingAndArmorWidthInPixels;
            newCanvas.height = craftingAndArmorHeightInPixels;
            context.clearRect(0, 0, newCanvas.width, newCanvas.height);
            context.drawImage(craftingAndArmorImage, 0, 0);
            context.drawImage(slotImage, slotX, slotY);
            craftingAndArmorImage.src = newCanvas.toDataURL();

        };
    };

    // draw the crafting table image things
    for (let y = 0; y < 3; y++) {
        for (let x = 0; x < 3; x++) {
            slotX = ((widthOfInventoryInSlots - 6) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
            slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))


            newCanvas.width = craftingTableSizeInPixels[0];
            newCanvas.height = craftingTableSizeInPixels[1];
            context.clearRect(0, 0, newCanvas.width, newCanvas.height);
            context.drawImage(craftingTableImage, 0, 0);
            context.drawImage(slotImage, slotX, slotY);
            craftingTableImage.src = newCanvas.toDataURL();

        };
    };

    // arrow for 2x2 grid
    let arrowX = (widthOfInventoryInSlots - 0.6) * slotSizeInPixels;
    let arrowY = (slotSizeInPixels * 0.75) + slotSizeInPixels * 1.1;
    let arrowWidth = arrowX + (slotSizeInPixels / 3);
    let scale = images["inventory arrow"].naturalWidth / arrowWidth;
    let arrowHeight = images["inventory arrow"].naturalHeight / scale;


    context.clearRect(0, 0, newCanvas.width, newCanvas.height);
    newCanvas.width = craftingAndArmorWidthInPixels;
    newCanvas.height = craftingAndArmorHeightInPixels;
    context.drawImage(craftingAndArmorImage, 0, 0)
    context.drawImage(images["inventory arrow"], arrowX, arrowY, arrowWidth, arrowHeight);

    craftingAndArmorImage.src = newCanvas.toDataURL();


    // arrow for 3x3 grid
    arrowX = (widthOfInventoryInSlots - 0.60) * slotSizeInPixels - slotSizeInPixels * 0.8;
    arrowY = (slotSizeInPixels * 0.75) + slotSizeInPixels * 1.1 + slotSizeInPixels / 1.8

    context.clearRect(0, 0, newCanvas.width, newCanvas.height);
    newCanvas.width = craftingTableSizeInPixels[0];
    newCanvas.height = craftingTableSizeInPixels[1];
    context.drawImage(craftingTableImage, 0, 0);
    context.drawImage(images["inventory arrow"], arrowX, arrowY, arrowWidth, arrowHeight);
    craftingTableImage.src = newCanvas.toDataURL();


    for (let y = 0; y < heightOfInventoryInSlots; y++) {
        for (let x = 0; x < widthOfInventoryInSlots; x++) {

            slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
            slotY = (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))

            context.clearRect(0, 0, newCanvas.width, newCanvas.height);
            newCanvas.width = inventoryWidthInPixels;
            newCanvas.height = inventoryHeightInPixels;
            context.drawImage(inventoryImage, 0, 0);
            context.drawImage(slotImage, slotX, slotY);
            inventoryImage.src = newCanvas.toDataURL();
        };
    };

    images["UI/" + "inventory"] = inventoryImage;
    images["UI/" + "crafting table"] = craftingTableImage;
    images["UI/" + "hotbar"] = hotbarImage;
    images["UI/" + "slot"] = slotImage;
    images["UI/" + "slot outline"] = slotOutlineImage;
    images["UI/" + "crafting and armor"] = craftingAndArmorImage;

};

makePlayerInventoryImages();




// wait one second between each check
const checkForLoadedImages = setInterval(function () {

    if (currentNumberOfLoadedImages === totalNumberOfImages) {
        allImagesLoaded = true;
        showLoadingProgress("images have been loaded");
    };

    if (allImagesLoaded) {
        clearInterval(checkForLoadedImages);
    };
}, 1000);