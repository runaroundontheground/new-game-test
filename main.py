from widelyUsedVariables import deltaTime
from controls import updateKeys, updateMouse
from rendering import render, generateSpawnArea
from player import player
import pygame, time

pygame.init()

clock = pygame.time.Clock()
FPS = 60


"""
ok currently:
fix rendering
    specifically, block render size scaling

trees, make generation actually work
    pre-generate terrain in a decent radius around player?
    then within another radius, generate structures, and then do block updates

transparency on blocks with nothing below them
    actually almost working all the way, but it needs to check if the block
    below it doesn't have a block below it, in order to make that block
    have alpha so the player can see while under blocks
    most obviously broken with trees
    trees are also the only way to show this, as there's no caves currently
    or block modification


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

        updateKeys()
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