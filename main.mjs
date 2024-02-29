
import {
    deltaTime, items, entities, projectiles, fps, keysPressed,
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

function initializeGame() {
    consoleLog("test")

    generateSpawnArea();
    player.positionInSpawnArea();
    makeItemsExist();
    makeRecipesExist();

};

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
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

    deltaTime = performance.now() - lastFrameTime;

    let delayBetweenFramesInMilliseconds = (1000 / fps) * timeScale;
    if (running) {
        setTimeout(gameLoop, delayBetweenFramesInMilliseconds);
    };
};



let waitUntilImagesLoaded = setInterval(function () {
    if (allImagesLoaded) {
        initializeGame();
        showLoadingProgress("main was able to load successfully");
        gameLoop();
        clearInterval(waitUntilImagesLoaded);
    };
}, 1 * 1000);




