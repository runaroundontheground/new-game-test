/*from GlobalVariables import deltaTime, items, entities, projectiles, fps, keysPressed
import Worldgen, Controls, Items, Rendering, Recipes # do this so command line works for everything probably from here
from Items import makeItemsExist
from Recipes import makeRecipesExist
from Controls import updateMouseAndKeys
from Rendering import render, generateSpawnArea, doCommandStuff, showInvalidCommand
from Player import player

import pygame, time

pygame.init()

clock = pygame.time.Clock()


def edit(targetClass, property, value, key = ""):
    # should allow me to modify stuff in classes, should also work with dicts
    # this is here to make the command line better for debugging and testing stuff
    if key != "":
        propertyOfClass = getattr(targetClass, property)
        propertyOfClass[key] = value
    else:
        setattr(targetClass, property, value)






running = True

def gameLoop():
    global deltaTime, running
    typingCommands = False
    commandString = ""
    # hopefully i did deltatime correctly

    generateSpawnArea()
    player.positionInSpawnArea()
    makeItemsExist()
    makeRecipesExist()
    


    
    while running:
        
        currentTime = time.time()

        updateMouseAndKeys()
        

        for event in pygame.event.get():
            if event.type == exit:
                pygame.quit()
            if event.type == pygame.TEXTINPUT:
                previousCommandString = commandString
                commandString += event.text

        if not typingCommands:

            if keysPressed[pygame.K_SLASH]:
                typingCommands = True
                commandString = ""
                time.sleep(.25)
                pygame.key.start_text_input()
                


            player.doStuff(deltaTime)

            def makeStuffInAListDoThings(list):
                i = -1
                while i >= -len(list):
                    list[i].doStuff(player)
                    if list[i].deleteSelf:
                        list.pop(i)
                    i -= 1
            makeStuffInAListDoThings(entities)
            makeStuffInAListDoThings(projectiles)
        

            render(deltaTime)

            clock.tick(fps)

            newCurrentTime = time.time()
            
            deltaTime = 1 + (newCurrentTime - currentTime)

        else: # currently typing commands
            submitCommand = False

            if keysPressed[pygame.K_BACKSPACE]:
                commandString = commandString[:-1]
                
            submitCommand = doCommandStuff(commandString, previousCommandString, submitCommand)

            

            if submitCommand:
                try:
                    eval(commandString)
                except:
                    print("invalid command")
                    showInvalidCommand()
                    time.sleep(1)
                    

                typingCommands = False
                commandString = ""

            clock.tick(fps)


gameLoop()

pygame.quit()


*/



// Assume you have equivalent implementations for deltaTime, items, entities, projectiles, fps, keysPressed
// Also, assume you have equivalent implementations for Worldgen, Controls, Items, Rendering, Recipes, and Player


// this should be all the imports, hopefully that's good now
import {
    deltaTime, items, entities, projectiles, fps, keysPressed,
    timeScale, consoleLog
} from "./GlobalVariables.mjs";
import { makeItemsExist } from "./Items.mjs";
import { makeRecipesExist } from "./Recipes.mjs";
import { updateMouseAndKeys } from "./Controls.mjs";
import { render, generateSpawnArea, doCommandStuff, } from "./Rendering.mjs";
import { player } from "./Player.mjs";

let running = true
function initializeGame() {
    generateSpawnArea();
    player.positionInSpawnArea();
    makeItemsExist();
    makeRecipesExist();

};
let previousTime = performance.now();
function gameLoop() {
    // do things, then call self using setTimeout at the bottom/end
    updateMouseAndKeys();



    let delayBetweenFramesInMilliseconds = (1000 / fps) * timeScale;
    if (running) {
        setTimeout(gameLoop, delayBetweenFramesInMilliseconds);
    };
};

//initializeGame();
//gameLoop();

consoleLog("main was able to load successfully")


// stuff that was kinda converted
/*
const pygame = require('pygame');
const time = require('time');  // Assuming you have an equivalent library for time functions

pygame.init();

const clock = new pygame.time.Clock();

function edit(targetClass, property, value, key = "") {
    if (key !== "") {
        targetClass[property][key] = value;
    } else {
        targetClass[property] = value;
    }
}

let running = true;

function gameLoop() {
    let deltaTime;
    let typingCommands = false;
    let commandString = "";

    generateSpawnArea();
    player.positionInSpawnArea();
    makeItemsExist();
    makeRecipesExist();

    while (running) {
        const currentTime = time.time();

        updateMouseAndKeys();

        pygame.event.pump();

        if (!typingCommands) {
            if (keysPressed[pygame.K_SLASH]) {
                typingCommands = true;
                commandString = "";
                time.sleep(.25);
                pygame.key.start_text_input();
            }

            player.doStuff(deltaTime);

            function makeStuffInAListDoThings(list) {
                for (let i = list.length - 1; i >= 0; i--) {
                    list[i].doStuff(player);
                    if (list[i].deleteSelf) {
                        list.splice(i, 1);
                    }
                }
            }

            makeStuffInAListDoThings(entities);
            makeStuffInAListDoThings(projectiles);

            render(deltaTime);

            clock.tick(fps);

            const newCurrentTime = time.time();
            deltaTime = 1 + (newCurrentTime - currentTime);
        } else { // currently typing commands
            let submitCommand = false;
            const previousCommandString = commandString;

            if (keysPressed[pygame.K_BACKSPACE]) {
                commandString = commandString.slice(0, -1);
            }

            submitCommand = doCommandStuff(commandString, previousCommandString, submitCommand);

            if (submitCommand) {
                try {
                    eval(commandString);
                } catch (error) {
                    console.log("Invalid command");
                    showInvalidCommand();
                    time.sleep(1);
                }

                typingCommands = false;
                commandString = "";
            }

            clock.tick(fps);
        }
    }

    pygame.quit();
}

gameLoop();
*/