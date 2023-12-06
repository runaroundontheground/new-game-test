from widelyUsedVariables import deltaTime, items
from itemsAndEntities import makeItemsExist
from controls import updateMouseAndKeys
from rendering import render, generateSpawnArea
from player import player

import pygame, time

pygame.init()

clock = pygame.time.Clock()
FPS = 60


"""
ok currently:

to do list but in order:
    
    
    display an item count in the bottom right corner of inv slots that have items
    make sure placing blocks actually removes 1 from the count
    add/make sure item entities actually work and give player their 
    make sure picking up the items can stack properly, and other stuff
    once that's done ish
    do the inventory looping when closing the inventory with something in 
    mouse.helditem, because if the inv is full, can't place the item, so it has to
    be dropped


inventory:
    need to make it so that while looping through the player's inventory, it also
    sets the item in the slot to have the slotId of that slot, so that the item
    can modify the player's inventory from the item code, instead of manual things
    in the player's code
    in order to keep things from breaking, player can't jump while the inv is open
    if the player tries to close their inventory while there's an item in the cursor,
    copy minecraft's implementation:
        loop through hotbar, if any of the slots are empty, put it there, then break
        loop through inventory, if any slots are empty, put there, break
    

add breaking/placing blocks
    placing blocks has been implemented, but you can't break them, and it doesn't
    track item count

oh. welp, uhh dropped items and other entites need to be scaled based on
height from the player and stuff
that could be annoying

    

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
day/night cycle



"""



running = True

def gameLoop():
    global deltaTime
    # hopefully i did deltatime correctly

    generateSpawnArea()
    player.positionInSpawnArea()
    makeItemsExist()
    player.inventory[4]["contents"] = items["log"]
    player.inventory[9]["contents"] = items["grass"]

    while running:
        currentTime = time.time()

        updateMouseAndKeys()
        
        
        for event in pygame.event.get():
            if event.type == exit:
                pygame.quit()

        player.doStuff(deltaTime)
        

        render(deltaTime)
        
        clock.tick(FPS)

        newCurrentTime = time.time()
        
        deltaTime = 1 + (newCurrentTime - currentTime)


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