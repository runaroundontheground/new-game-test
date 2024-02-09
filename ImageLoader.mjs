import { consoleLog, allImagesLoaded } from "./GlobalVariables.mjs";

let imageDiv = document.getElementById("imageHolder");
/*
based on a list that i make manually, load all of those images, put them into imageHolder
with display: none; and then once document.all images are loaded or whatever the actual thing is
set allImagesLoaded to true (in main i guess?)
*/
let imagesHaveBeenAdded = false;

window.addEventListener("load", function () {
    if (imagesHaveBeenAdded) {
        allImagesLoaded = true
    };
    consoleLog("allImagesLoaded: " + allImagesLoaded);
    consoleLog("imagesHaveBeenAdded: " + imagesHaveBeenAdded);
});

let imageUrls = [
    "./Images/stick.png",
    "./Images/tools/stone axe.png",
    "./Images/tools/stone pickaxe.png",
    "./Images/tools/wood axe.png",
    "./Images/tools/wood pickaxe.png"
];



imageUrls.forEach(function (url) {
    let image = document.createElement("img");
    image.style.display = "none";
    image.src = url;
    imageDiv.appendChild(image);
});

imagesHaveBeenAdded = true;
