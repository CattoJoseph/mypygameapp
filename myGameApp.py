#imports
import pygame as pg
import random
import sqlite3

from os import path
from supportModules import *
img_dir = path.join(path.dirname(__file__),'img') #img is the folder where the graphics are
snd_dir = path.join(path.dirname(__file__),'snd') #snd is the folder where the sounds are
#load all game graphics
#convert() methods will draw the image in memory before it is displayed which is
# much faster than drawing it in real time i.e. pixel by pixel  
# time = 0
#parameters
WIDTH,HEIGHT,FPS = (1000,600,60)
#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#a sprite will be an object which inherits from the built in sprite class
class Player(pg.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        #constructor
        pg.sprite.Sprite.__init__(self) #inheritance
        self.image = pg.transform.scale(player_img,(64,53)) #surface gives you something to draw on
        self.image.set_colorkey(BLACK)
        #useful for moving, size, position and collision
        self.rect = self.image.get_rect() #looks at the image and gets its rect
        self.radius = int(self.rect.width /2)  # assumption made since width of sprite is 64 - radius is 32
        #we will draw a circle so we see how big it is so we can adjust the radius
        #we will draw it in red at the center of the rectangle and using the radius above
        #pg.draw.circle(self.image,RED,self.rect.center,self.radius)
        
        self.rect.centerx = (WIDTH/2) #places image in the centre
        self.rect.bottom = HEIGHT-10
        #it needs to move side to side so we need speed
        self.speedx = 0
        
    def update(self):
        #we will keep the default speed of the object to zero and only alter it with a key press
        #this way we avoid coding for what happens when the key is released
        self.speedx = 0
        keystate = pg.key.get_pressed() #returned a list of keys that are down
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        #move the sprite
        self.rect.x += self.speedx # move at speed to be set by controls
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        #to ensure it does not run off the screen
        if self.rect.left > WIDTH:
            self.rect.right = 0
    def shoot(self):
        #spawns new bullet at centerx of player
        #y will spawn at the top - i.e.bottom of the bullet at the top of the player
        bullet = Bullet(self.rect.centerx,self.rect.top)
        #add bullet to all sprites group so that its updated
        all_sprites.add(bullet)
        #add bullet to the bullets sprite group
        bullets.add(bullet)
        #play a sound
        shoot_sound.play()
class Mob(pg.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(mob_img,(60,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width /2)
        #pg.draw.circle(self.image,RED,self.rect.center,self.radius)

        #make the enemy spawn off top of the screen to appear off the screen and then start dropping down
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
        self.rect.y = random.randrange(-100,-40) # this is off the screen
        self.speedy = random.randrange(4,10)
    
    def update(self):
        #move downwards
        self.rect.y += self.speedy
        #deal with enemy when they get to the bottom of the screen
        if self.rect.top > HEIGHT +10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
            self.rect.y = random.randrange(-100,-40) #this is off the screen
            self.speedy = random.randrange(1, 8)

class Boss(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(boss_img,(150,150))
        self.image.set_colorkey(BLACK)
        #set sprite image to a copy
        self.rect = self.image.get_rect()
        health = 3
        self.radius = int(self.rect.width * 0.9/2)
        self.rect.centerx = WIDTH/2
        self.rect.y = random.randrange(-100,-40)
        self.speedy = 8

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.centerx = WIDTH /2
            self.rect.y = random.randrange(-100,-40)
            self.speedy = 8

#create a sprite group
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group() #creating another group would aid during collision detection
boss = pg.sprite.Group()

#initialise common pygame objects
pg.init()
pg.mixer.init()

#create the window
screen = pg.display.set_mode((WIDTH,HEIGHT))
'''set mode takes one parameter therefore two brackets'''
pg.display.set_caption("My Game")
clock = pg.time.Clock()#handles the speed

background = pg.image.load(path.join(img_dir,"RMBackground.jpg")).convert()
#to place the image somewhere, make a rect for it
background_rect = background.get_rect()
mob_img = pg.image.load(path.join(img_dir, "MrNimbusEnemy.png")).convert()
player_img = pg.image.load(path.join(img_dir, "Rick2 player.jpg")).convert()
bullet_img = pg.image.load(path.join(img_dir, "Morty bullet.png")).convert()
boss_img = pg.image.load(path.join(img_dir, 'evilMorty.jpg')).convert()
  
 #L   o ad sound files
shoot_sound = pg.mixer.Sound(path.join(snd_dir,'mortyHello.mp3'))
#Load sxplosion sounds
expl_sounds = []
for snd in ['Nimbus.mp3', 'Nimbus.mp3']:
    expl_sounds.append(pg.mixer.Sound(path.join(snd_dir,snd)))

#Load background sound
pg.mixer.music.load(path.join(snd_dir,'RMbgaudio.mp3'))
pg.mixer.music.set_volume(0.75)

#conn = sqlite3.connect("RickAndMortyGame")
conn = sqlite3.connect("RickAndMortyGame.db" )

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        # x and y are respawn positions based on the player's position
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(bullet_img,(30,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #set re-spawn position to right infront of the player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        #rect moves upwards at the speed
        self.rect.y += self.speedy
        #kill it if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()  
#Load other image

#create a sprite group
all_sprites = pg.sprite.Group()
# create an enemy sprite group
mobs = pg.sprite.Group()
bullets = pg.sprite.Group() # bullets sprite group
#instantiate the player object and add it to the sprite group
player = Player()
#spawn some mobs
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
all_sprites.add(player)
score = 0
all_sprites.add(boss)
#play background audio
#parameters could include - play list, looping
#loops=-1 - tells pygame to look each time audio gets to the end
pg.mixer.music.play(loops=-1)

#Game loop
#You need a while loop and a way to stop it - the variable "running" is used here
running = True
while running:
    #keep the game running at the right speed
    clock.tick(FPS)
    #process input(events)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        #check event for keydown to shoot
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
    num1= random.randint(1,20)
    num2 = random.randint(1,20)
    if score % 30 == 0 and score >0:
        all_sprites.remove(mobs)
        answer = int(input(f"What is {num1} times {num2}?"))
        draw_text(screen,str(answer),40,WIDTH/2,HEIGHT/2)
        pg.display.flip()
        if num1 * num2 == answer:
            correct_message = ("Correct! Play on!")
            draw_text(screen,str(correct_message),42,WIDTH/2,HEIGHT/2)
            pg.display.flip()
            all_sprites.add(mobs)
            score += 1
        else:
            quit

    #update
    all_sprites.update()
    
    #check if a bullet hits a mob
        #you have to consider a group of bullets and a group of mobs
        #using a pygame.sprite.groupcollide() mehtod helps to collide two groups together
        #Setting the last two parameters will delete the bullet and the mob which collide with each other
        #notice that this will kill the mobs so there needs to be a way of respawning them if they get killed
    hits = pg.sprite.groupcollide(mobs,bullets,True,True)
    bosshits = pg.sprite.groupcollide(boss,bullets,True,True)
    for hit in hits:
        score +=1 # 1 point for every hit you make
        if score == 50:
            b = Boss()
            all_sprites.remove(mobs)
            all_sprites.add(b)
            boss.add(b)
            for bosshit in bosshits:
                health = health - 1
                if health == 0:
                    all_sprites.remove(boss)                      
        random.choice(expl_sounds).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    #Check to see if a mob hit the player
    hits = pg.sprite.spritecollide(player,mobs,False, pg.sprite.collide_circle) # parameters are object to check against and group against
                                    #FALSE indicates whether hit item in group should be deleted or not
    bosshits = pg.sprite.spritecollide(player,boss,False, pg.sprite.collide_circle)


    if hits:
        running = False
    #draw/render
    screen.fill(BLACK) #keep this just in case the background image does not fit the entire screen
    #draw background on the screen
    #blit means copy the pixels of one thing on to another
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    #draw the score here
    draw_text(screen,str(score),40,WIDTH/2,20, RED)
#    while running:
#        draw_time(screen,str(time),40,WIDTH/2-400,20,timer)
    #always do this after drawing everything
    pg.display.flip()
print(conn)
'''
Username = input("Enter username: ")
if checkExists() == 1:
    conn.commit()
else:
    print("This person is not in the database")
'''

#terminate the game window and close everything
pg.quit
name=input('Enter your name: ')
id = int(input('Enter your ID: '))
writeNewRecord(name, id, score)