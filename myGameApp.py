#imports
import pygame as pg
import random

#parameters
WIDTH,HEIGHT,FPS = (800, 600,30)
#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#initialise common pygame objects
pg.init()
pg.mixer.init()

#create the window
screen = pg.display.set_mode((WIDTH,HEIGHT))
'''set mode takes one parameter therfore two brackets'''
pg.display.set_caption('My Game')
clock = pg.time.Clock()

#Game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    #update
            
    #draw/render
    screen.fill(BLACK)
    pg.display.flip()
pg.quit