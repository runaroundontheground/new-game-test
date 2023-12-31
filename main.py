from globalVariables import deltaTime, items, entities, projectiles, FPS, keysPressed, typingCommands, commandString
from items import makeItemsExist
from controls import updateMouseAndKeys
from rendering import render, generateSpawnArea, doCommandStuff, showInvalidCommand
from player import player

import pygame, time

pygame.init()

clock = pygame.time.Clock()



"""
ok currently:

to do list:

    
    make sure inventory management is fully functioning and doesn't break (often at least)

    add in an actual command line thing within the game to run commands, instead
    of just using eval() on an input (probably pretty insecure lol but eh whatever)



    
    


    when placing blocks, apparently picking up a block does weird things sometimes
    the blocks aren't placing correctly, it's not actually putting it down
    
                        figure out why alpha on the trees don't work sometimes
                            ok, nevermind for now, idk why it won't work
    
                        figure out why the heck destroying a part of one tree breaks it on every single
                        other tree, the heck is happening???
                        still have no idea why it's broken
    

    add some crappy images for the tools (aka drawing a line on a surf, then another line)
    to make the icons

    add 3? surfaces to represent breaking blocks
    probably at the mouse's position, with math.floor and blocksize to put it
    on top of the block
    based on % of break progress, put that kind of breaking progress surf there
    

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
typingCommands = False
commandString = ""


running = True

def gameLoop():
    global deltaTime, typingCommands, commandString
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
        
        if keysPressed[pygame.K_SLASH]:
            typingCommands = True
            commandString = ""
            clock.tick(15)
            print("started doing commands stuff")
            

        for event in pygame.event.get():
            if event.type == exit:
                pygame.quit()

        if not typingCommands:

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
        

            render(deltaTime, typingCommands)

            clock.tick(FPS)

            newCurrentTime = time.time()
            
            deltaTime = 1 + (newCurrentTime - currentTime)

        else: # currently typing commands
            # add in a special feature in render that only does stuff when 
            # typingCommands is true
            submitCommand = False
            commandString, submitCommand = doCommandStuff(commandString, submitCommand)


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