from GlobalVariables import deltaTime, items, entities, projectiles, FPS, keysPressed
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


"""
to do list/ideas for things:

    make sure inventory management is fully functioning and doesn't break


    need to add some wood tools, in order to get the stone tools
    pickaxe, axe, shovel, no weapons exist yet

    
    lets goooooo
    crafting sticks works now

    now all i need to do is add in a shovel, and make a crafting table, and make
    a crafting table UI that uses all of the player's crafting slots, and that removes
    the items from the crafting slots if the player closes the ui aka inventory



    set up some kind of function to call when messing with the inventory in a way that would require
    changing the interaction points of inventory slots
    normalInventoryPosition = (x, y)?
    reset it to that when things happen to get to the normal inventory state or something


    blocks needed to make simple structures (like a small hut, or something)
        glass?
        same rule as water (or similar at least), uses alpha by default

    
    problem with smallScaleBlockUpdates
        when you place a block that is next to water, it's not rendered for some reason
        wait nvm, it has alpha, still no idea why
        that needs to be fixed
        also one of them has super high alpha, but it's only with logs for some reason
    
    

    add a crappy image for a shovel

    add 3? surfaces to represent breaking blocks
    probably at the mouse's position, with math.floor and blocksize to put it
    on top of the block
    based on % of break progress, put that kind of breaking progress surf there
    
    hooray, recipes have been somewhat figured out
        



    
oh. welp, uhh dropped items and other entites need to be scaled based on
height from the player and stuff
that could be annoying
attempted this^, and didn't get it to work quickly so it'll be done later


    

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

enemies
    probably a simple ai, similar to terraria's run towards player and jump over things
    new ai idea: draw a line to the player that only goes on x/z axis and then check
    if any blocks are in the way there (maybe also floor blocks?)
    go there, and do checks and stuff

day/night cycle and lighting
    don't use a screen sized surface with some alpha for lighting
    use rgb add or subtract or whatever, that will also be used for the lighitng system in general
    but everything on screen can have that as a temporarly solution for testing overall lighting

    new lighting idea:
        every air block has a light value, and it dimishes over distance, but in direct light it will be max
        i guess i'll copy mc, so 15 is the max light level
        after doing block updates from the inital generation, then do lighting updates, and it will go from
        height limit down, to see if there is air, and then if there is air, it'll have a value of like,
        receivesDaylight: True or something

        in small scale block updates, it will run from the affected block up, until 

    that's conveinent
    255/15 = 17, so there'd be jumps of 17 rgb between each light level or something like that
    
        
        new properties that all blocks will need (including air)
            receivesDaylight and light

    light dimishes 100% through any non transparent blocks

    the way blocks will be lit with the only light source being daylight:
        initially determined in block updates, and then based on the current time of the day cycle
        receivesDaylight will stay the same, but light will change, figure out how to determine the jumps



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