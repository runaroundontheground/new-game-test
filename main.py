from widelyUsedVariables import deltaTime
from controls import updateKeys, updateMouse
from rendering import render
from player import player
import pygame, time

pygame.init()

clock = pygame.time.Clock()
FPS = 60


"""
ok currently:
fix rendering
    specifically, block render size scaling
player block step-up
    add a small velocity decrease, since you're "stepping" up stuff

ok new idea:
    when generating stuff that will definitely result with an overhang (player can go under)
    then have a different thingy that sees if player is within a certain range of it
    (player x < thing and player x > thing) if that's true
    then make the above block somewhat transparent so the player can see under it
    use some kind of system within where scaling happens to also make things do that
    or maybe not, instead i could only apply that to blocks that don't have any blocks
    under them, that's detected in chunk generation, but i'd need to check it while adding
    structures too
    actually, if structures are done before the chunk has its blocks rendered,
    i won't need to worry about any special things for structures, i'll just have to
    change what the block rendering/updates do


later plans:
trees
add breaking/placing blocks
    idea for that
    have a selector go on the mouse, or use arrow keys to select the block to break
    use scroll wheel to change y level, maybe < or > for y level using keyboard


wayyy later:
potentially naturally generated caves
crafting
lighting
enemies
day/night cycle



"""



running = True

def gameLoop():
    global deltaTime
    # hopefully i did deltatime correctly

    render(deltaTime)
    # call render in order to generate spawn area
    # yeah, maybe it shouldn't be in there but it is anyway

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
    hooray! the rendering and scaling work fine
    but now i need perlin noise generation to happen
    
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
    use something similar to minecraft's lighting, light emmitting stuff has a light level,
    light decays over distance, more so through walls, daytime has a high light level
    use pygame coloring stuff to change block's lighting

crafting system:
    copy minecraft?
"""