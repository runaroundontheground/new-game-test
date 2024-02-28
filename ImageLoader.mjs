
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
export let images = {};

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

// wait one second between each check
const checkForLoadedImages = setInterval( function () {

    if (currentNumberOfLoadedImages === totalNumberOfImages) {
        allImagesLoaded = true;
        showLoadingProgress("images have been loaded");
    };

    if (allImagesLoaded) {clearInterval(checkForLoadedImages);};
}, 1000);