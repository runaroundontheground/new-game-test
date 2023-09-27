from controls import updateKeys, updateMouse
from rendering import render
from player import player
import pygame

pygame.init()

 




from rendering import render

clock = pygame.time.Clock()
FPS = 60

running = True

def gameLoop():
    while running:
        
        updateKeys()
        updateMouse()
        
        for event in pygame.event.get():
            if event.type == exit:
                pygame.quit()
        

        render()
        
        clock.tick(FPS)


gameLoop()

pygame.quit()

"""
the plan
first:
    somewhat setup player controlling and camera
    test some things for the zoomed rendering
worlgen and height things:
    top down game, randomly generated using perlin noise to create a map of heights
    implement 3 axis somehow: x, y, z

    change the zoom of everything around the player, default zoom for stuff that's the same height,
    lower zoom for stuff that's lower down, and higher zoom for higher stuff
    make tiles transparent if the player is under them
    
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
        save different colorable things as separate surfaces so they can be recolored]

lighting system ideas:
    use something similar to minecraft's lighting, light emmitting stuff has a light level,
    light decays over distance, more so through walls, daytime has a high light level
    use pygame coloring stuff to change block's lighting

crafting system:
    copy minecraft?
"""