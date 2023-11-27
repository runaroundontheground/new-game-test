from widelyUsedVariables import deltaTime
from controls import updateMouseAndKeys, updateMouse
from rendering import render, generateSpawnArea
from player import player
import pygame, time

pygame.init()

clock = pygame.time.Clock()
FPS = 60


"""
ok currently:


problem that can happen with current implementation of structure gen
if a structure is too big, then it'll break out of the fix i made to fix that
(like a village or something)
solution?
    probably to generate the terrain of any chunks that the structure overlaps with
    if that chunk doesn't exist already
    hooray, more try else things

    that doesn't matter until i have bigger structures though...


in order to make placing/breaking blocks work, i'll probably need some form of
inventory, so i guess that's up next

which also means items need to exist
item system ideas:
    a base class for items: Item
    has some parameters, like name, and what kind of item it is
    subclasses for different item types?
    need to research how to use subclasses, since i forgor


inventory ideas:
    make something similar to mc inventory
    render a rectangle that's big, and then render small squares which are
    the inventory slots, and then inside of those, render whatever item is supposed
    to be there
    rendering an item that's in the player's inventory:
        the item probably has an image called itemIcon.png or something
        that's whats rendered in the box, will probably automatically resize those
        to be whatever the inventory slot size should be
    the inventory is a class, with built in functions like adding an item
    removing an item, anything else that i might add
    slot sorting things:
        same inv size as mc, top left slot is slot id 0, right 1 is slot id 1, so on
        once it reaches 9, it'll go to the middle left slot, and so on

add breaking/placing blocks
    idea for that
    have a selector go on the mouse, or use arrow keys to select the block to break
    use scroll wheel to change y level, maybe < or > for y level using keyboard
    have a selector that 'frames' the blocks, maybe green if valid for break/place
    red if not valid for those
    should block swap exist: no
    


wayyy later:
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

    while running:
        currentTime = time.time()

        updateMouseAndKeys()
        updateMouse()
        
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