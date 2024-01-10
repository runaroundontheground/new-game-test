from GlobalVariables import deltaTime, items, entities, projectiles, FPS, keysPressed
import Worldgen, Controls, Items, Rendering # do this so command line works for everything? from here
from Items import makeItemsExist
from Controls import updateMouseAndKeys
from Rendering import render, generateSpawnArea, doCommandStuff, showInvalidCommand
from Player import player

import pygame, time

pygame.init()

clock = pygame.time.Clock()



"""
to do list/ideas for things:


    make sure inventory management is fully functioning and doesn't break

    idea for adding actual textures to the block textures
    use a perlin noise map when generating the block to put some random darker/lighter bits on the texture

    blocks needed to make simple structures (like a small hut, or something)
        planks, probably make cobblestone 


    

    add some crappy images for the tools (aka drawing a line on a surf, then another line)
    to make the icons

    add 3? surfaces to represent breaking blocks
    probably at the mouse's position, with math.floor and blocksize to put it
    on top of the block
    based on % of break progress, put that kind of breaking progress surf there
    
    recipes: complicated wow

    extend the player inventory, and then also figure out how to make crafting work
    and make sure recipes aren't awful to add
    recipes:
        based on grid size:
        2x2:
            dict with 4 items, ex: {0: empty, 1: planks,
                                    2: empty, 3: planks}
                                    = sticks
    recipe detection ideas:
        go through the crafting slots, and then count how many of each item there is in it
        ex: sticks recipe, req's two planks, and nothing else
        and then after than, if it's a shapeless recipe, that's all that needs to be done
        if it's shaped, like sticks, but can be crafted in multiple spots, then
        define some functions to check whether the recipe has items in the right spots, so for sticks
        it would look through the list until it finds a plank, and then looks if theres a plank above 
        or under it

        the way to begin searching for recipes:
        if something is put into the crafting grid, count the number of items and stuff
        using all the keys from what is in the crafting grid
        use dict.get and check that against all recipes, if it returns false while checking a recipe then
        just stop checking that one



    adding recipes:
        3 recipe types?
        shapeless, exact, and nearExact
        for all recipes, input a dict that has the count of whatever items need to be in the crafting grid
        for shapeless recipes, all it needs is the count of items
        exact recipes:
        input a dict with items in specific slots/slot ids, and dont include empty slots
        nearExact recipes:
        hopefully there can't be too many of these, they probably need specific code to work
        maybe have it so that a specific layout is inputed, 



    
oh. welp, uhh dropped items and other entites need to be scaled based on
height from the player and stuff
that could be annoying
attempted this^, and didn't get it just now


    

problem that can happen with current implementation of structure gen
if a structure is too big, then it'll break out of the fix i made to fix that
(like a village or something)
solution?
    probably to generate the terrain of any chunks that the structure overlaps with
    if that chunk doesn't exist already
    hooray, more try else things

    that doesn't matter until i have bigger structures though...





later:
animations
    DON'T BE COMPLICATED
    why do i always overcomplicate these...
potentially naturally generated caves
crafting
    probably copy mc, wonder how i'll make adding recipes annoying to do
    shapeless, shaped
lighting
    idea for general lighting based on time of day
    render a really big rectangle black rectangle that covers the screen and has
    varying alpha levels
enemies
    probably a simple ai, similar to terraria's run towards player and jump over things
    new ai idea: draw a line to the player that only goes on x/z axis and then check
    if any blocks are in the way there (maybe also floor blocks?)
    go there, and do checks and stuff
day/night cycle



"""



running = True

def gameLoop():
    global deltaTime
    typingCommands = False
    commandString = ""
    # hopefully i did deltatime correctly

    generateSpawnArea()
    player.positionInSpawnArea()
    makeItemsExist()
    # hooray for adding a function to do this!
    player.giveItem(items["log"], 3)
    player.giveItem(items["grass"], 64)
    player.giveItem(items["stone pickaxe"], 1)
    player.giveItem(items["stone"], 8)
    
    
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

            clock.tick(FPS)

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

            clock.tick(FPS)


gameLoop()

pygame.quit()

"""
the plan
first:
   
    infinite world or finite, pre-generated? maybe add option for both
    save player/world files into txt or something
    block types:
        air, grass, dirt, stone, snow, sand, water, ice, logs, planks, glass

animation ideas:
    make an animation system that works for holding things easily
    DONT MAKE THE ANIMATIONS SUPER COMPLEX - simple works good

    anchor the player's arms to shoulders, and rotate them around that
    maybe use IK or something similar i could come up with
        get distance to where hands should be, compare that to the arm's lengths,
        figure rest out later
    or i could make a few generalized animations, swing two handed, swing one handed
    held one handed, held two handed
    later edit: why would i want to use inverse kinematics here??

    customizable sections of player (color, armor, etc)
        color of skin, armor, clothes
        save different colorable things as separate surfaces so they can be recolored]1

lighting system ideas:
    use something similar to minecraft's lighting, light emitting stuff has a light level,
    light decays over distance, more so through walls, daytime has a high light level
    use pygame coloring stuff to change block's lighting
    read the text block that's before the game loop for diff info

crafting system:
    copy minecraft?
"""