from controls import updateKeys, updateMouse
from rendering import render
from player import player
import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

running = True

"""
very important idea
put a border around the edge of blocks, that is a color that makes sense for the block
stone: slightly darker
grass: use the dirt color for the sides
dirt: use a slightly darker version of the dirt color

once i've fixed the find block function and anything related, add a performance
fix that is caused by not rendering any blocks that have another block directly above them
that'll probably break caves and being able to do stuff with blocks

"""


def gameLoop():
    while running:
        
        updateKeys()
        updateMouse()
        
        for event in pygame.event.get():
            if event.type == exit:
                pygame.quit()

        player.doStuff()
        

        render()
        
        clock.tick(FPS)


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