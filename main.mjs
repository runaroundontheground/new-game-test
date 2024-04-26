
import {
    items, entities, projectiles, fps, keysPressed,
    timeScale, showLoadingProgress,
    canvas, ctx, // importing things to be accessed from eval() command line thingy
    chunks
} from "./GlobalVariables.mjs";
import { makeItemsExist } from "./Items.mjs";
import { makeRecipesExist } from "./Recipes.mjs";
import { updateMouseAndKeys } from "./Controls.mjs";
import { render, generateSpawnArea } from "./Rendering.mjs";
import { player } from "./Player.mjs";
import { allImagesLoaded } from "./ImageLoader.mjs";



showLoadingProgress("loading main.mjs")

let lastFrameTime = 0;
let running = true;
let deltaTime = 1;




let commandInput = document.getElementById("command input");

commandInput.onkeydown = function (event) {
    if (event.key == "Enter") {
        let value = commandInput.value;
        commandInput.value = "";
        eval(String(value));
        commandInput.blur()
    }
}

document.getElementById("game stopper").onclick = () => {
    running = false;
    canvas.width = 5;
    canvas.height = 5;
}


function initializeGame() {

    clearInterval(tryToStartGame);
    tryToStartGame = null;

    generateSpawnArea();
    player.positionInSpawnArea();
    makeItemsExist();
    makeRecipesExist();

};

function gameLoop() {

    lastFrameTime = performance.now();

    player.doStuff(deltaTime);


    for (let i = entities.length - 1; i >= 0; i--) {

        entities[i].doStuff(player);
        if (entities[i].deleteMe) { entities.splice(i, 1); };

    }

    for (let i = projectiles.length - 1; i >= 0; i--) {

        projectiles[i].doStuff(player);
        if (projectiles[i].deleteMe) { projectiles.splice(i, 1); };

    }

    render();

    updateMouseAndKeys();

    deltaTime = 1//(performance.now() - lastFrameTime) / 1000; // it's probably in milliseconds right

    if (deltaTime > 2) {
        deltaTime = 2;
    }

    let delayBetweenFramesInMilliseconds = 1000 / fps//(1000 / fps) * timeScale;


    if (running) {
        requestAnimationFrame(function () { setTimeout(gameLoop, delayBetweenFramesInMilliseconds); });
    };
};


function checkForImageLoaded() {
    if (allImagesLoaded) {

        initializeGame();
        showLoadingProgress("main loaded, probably");
        gameLoop();
        //let game = setInterval(gameLoop, 1000/fps);
        clearInterval(tryToStartGame);
        tryToStartGame = null;
        document.getElementById('loadingProgressDiv').style.display = 'none'
    };
}

let tryToStartGame = setInterval(checkForImageLoaded, 1000);




