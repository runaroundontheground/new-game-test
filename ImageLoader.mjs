
function consoleLog(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};

let imageDiv = document.getElementById("imageHolder");


let imagesHaveBeenAdded = false;
var allImagesLoaded = false;
export { allImagesLoaded };

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


window.addEventListener("load", function () {
    if (imagesHaveBeenAdded === true) {
        allImagesLoaded = true;
    };
    consoleLog("allImagesLoaded: " + allImagesLoaded);
    consoleLog("imagesHaveBeenAdded: " + imagesHaveBeenAdded);
});

