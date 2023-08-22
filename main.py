import random
import pygame

pygame.init()

keys = pygame.key.get_pressed()
keysPressed = []
for num in range(len(keys)):
    keysPressed.append(False)

screenWidth = 600
screenHeight = 400
screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()
FPS = 60

running = True
while running:




    clock.tick(FPS)

pygame.quit()
