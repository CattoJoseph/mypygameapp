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

#a sprite will be an object which inherits from the built in sprite class
class Player(pg.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        #constructor
        pg.sprite.Sprite.__init__(self) #inheritance
        self.image = pg.Surface((50,50)) #surface gives you something to draw on
        self.image.fill(GREEN)
        #useful for moving, size, position and collision
        self.rect = self.image.get_rect() #looks at the image and gets its rect
        self.rect.center = (WIDTH/2, HEIGHT/2) #places image in the centre
    
    def update(self):
        #move the sprite
        self.rect.x +=5
        #to ensure it does not run off the screen
        if self.rect.left > WIDTH:
            self.rect.right = 0
#initialise common pygame objects
pg.init()
pg.mixer.init()

#create the window
screen = pg.display.set_mode((WIDTH,HEIGHT))
'''set mode takes one parameter therfore two brackets'''
pg.display.set_caption('My Game')
clock = pg.time.Clock()

#create a sprite group
all_sprites = pg.sprite.Group()
#instantiate the player object and add it to the sprite group
player = Player()
all_sprites.add(player)

#Game loop
#You need a while loop and a way to stop it - the variable "running" is used here
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