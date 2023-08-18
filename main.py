import random as rand
import pygame as pg


pg.init()

display = pg.display.set_mode((100, 100))
rect = pg.Rect(0, 0, 20, 20)

display.fill((255, 255, 255))
pg.display.flip()
input()

pg.quit()
