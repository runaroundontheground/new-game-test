
import {
    deltaTime, items, entities, projectiles, fps, keysPressed,
    timeScale, consoleLog, allImagesLoaded, showLoadingProgress
} from "./GlobalVariables.mjs";
import { makeItemsExist } from "./Items.mjs";
import { makeRecipesExist } from "./Recipes.mjs";
import { updateMouseAndKeys } from "./Controls.mjs";
import { render, generateSpawnArea, doCommandStuff } from "./Rendering.mjs";
import { player } from "./Player.mjs";

showLoadingProgress("loading main.mjs")
let lastFrameTime = 0
let running = true
function initializeGame() {
    generateSpawnArea();
    player.positionInSpawnArea();
    makeItemsExist();
    makeRecipesExist();


};

function gameLoop() {
    lastFrameTime = performance.now();
    // do things, then call self using setTimeout at the bottom/end

    for (let i = entities.length - 1; i >= 0; i--) {

        entities[i].doStuff();
        if (entities[i].deleteMe) { entities.splice(i, 1); };

    }

    for (let i = projectiles.length - 1; i >= 0; i--) {

        projectiles[i].doStuff();
        if (projectiles[i].deleteMe) { projectiles.splice(i, 1); };

    }

    render();
    updateMouseAndKeys();

    currentTime = performance.now();
    deltaTime = currentTime - lastFrameTime;

    let delayBetweenFramesInMilliseconds = (1000 / fps) * timeScale;
    if (running) {
        setTimeout(gameLoop, delayBetweenFramesInMilliseconds);
    };
};



window.addEventListener("load", function () {
    if (allImagesLoaded) {
        initializeGame();
        showLoadingProgress("main was able to load successfully");
        //gameLoop();
    };
});



