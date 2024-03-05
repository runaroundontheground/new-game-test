
import {
    items, entities, projectiles, fps, keysPressed,
    timeScale, consoleLog, showLoadingProgress,
    canvas, ctx
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
    
    /*
    for (let i = entities.length - 1; i >= 0; i--) {

        entities[i].doStuff();
        if (entities[i].deleteMe) { entities.splice(i, 1); };

    }

    for (let i = projectiles.length - 1; i >= 0; i--) {

        projectiles[i].doStuff();
        if (projectiles[i].deleteMe) { projectiles.splice(i, 1); };

    }*/

    render();

    updateMouseAndKeys();

    deltaTime = performance.now() - lastFrameTime;

    let delayBetweenFramesInMilliseconds = (1000 / fps) * timeScale;
    if (running) {
        setTimeout(gameLoop, delayBetweenFramesInMilliseconds);
    };
};


function checkForImageLoaded () {
    if (allImagesLoaded) {

    initializeGame();
    showLoadingProgress("main loaded, probably");
    gameLoop();
    clearInterval(tryToStartGame);
    tryToStartGame = null;
    };
}

let tryToStartGame = setInterval(checkForImageLoaded, 1000);




