import pygame
from pygame.locals import*
import random
import time

#Declaration
clock = pygame.time.Clock()
#pygame.mixer.pre_init(44100,16,2,4096)  #Frequency,size,channels,buffersizes
pygame.display.set_caption('Beta Snake-Tron')
pygame.font.init()
pygame.init()

#Game Configuration
fps = 40                 #Speed of worm
width = 1000
height = 800
score = 0
bgColor = (0,0,0)
snakeColor = (250,250,250)
snake2Color = (140,10,200)
wallColor = (0,250,0)
foodColor = (250,0,0)
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
#width = pygame.display.Info().current_w
#height = pygame.display.Info().current_h

#Some sprite configuration
foodInc = 50            #Increase snake's length for foodInc pixel long
foodx = foody = 10      #Food X-Size
snakex = snakey = 5     #Size of one part of Snake
iniLength = 10          #Initial Snake Length
vel = 5                 #Velocity must be equal to snake pixel size or will cause pixel-collision problem
snake1Pos = [width * 10/100,height * 90/100]
snake2Pos = [width * 90/100,height * 90/100]

#Font Configuration
BASICFONT = pygame.font.Font('freesansbold.ttf',18)
TITLEFONT = pygame.font.Font('freesansbold.ttf',18)
INSFONT = pygame.font.Font('freesansbold.ttf',12)


#Color Configuration
WHITE = (255,255,255)
GREY = (200, 200, 200)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,100)
LIGHTBLUE = (0,0,255)
PURPLE = (255,0,255)
ORANGE = (255,165,0)
PINK = (255,192,203)
YELLOW = (255,255,0)
BLACK = (0,0,0)

#Load Sound
song_loc = '/home/pi/mostec17/audio/'
sounds = ['wallCrash','self_crash','food_touch','snake_crash','di de','genghis_khan']
pygame.mixer.init()
#pygame.mixer.music.load(song_loc+sounds[]+'.mp3')
#pygame.mixer.music.play()
selfCrash = pygame.mixer.Sound('self_crash.wav')
selfCrash.play()
#foodTouch = pygame.mixer.Sound(song_loc+sounds[2]+'.wav')
#snakeCrash = pygame.mixer.Sound(song_loc+sounds[3]+'.wav')

#Class Declaration-----------------------------------------------------
class Food:
    def __init__(self,surface):
        self.surface = surface
        self.x = random.randint(20,width-20)
        self.y = random.randint(20,height-20)
        self.color = foodColor
        
    def draw(self):
        #Draw food --Can't be at obstacles or snake body parts or outside of boundary
        pygame.draw.rect(self.surface,self.color,(self.x,self.y,foodx,foody),0)

    def position(self):
        return self.x,self.y

    def check(self,x,y):
        if x < self.x or x > self.x + foodx:
            return False
        elif y < self.y or y > self.y + foody:
            return False
        else:
            return True

    def erase(self):
        pygame.draw.rect(self.surface,bgColor,(self.x,self.y,foodx,foody),0)


class Worm:
    # A worm
    
    def __init__(self,surface):
        self.surface = surface
        self.x = int(snake1Pos[0])
        self.y = int(snake1Pos[1])        
        self.length = iniLength
        self.vx = 0
        self.vy = -1           #Initial movement
        self.body = []
        self.crashed = False
        self.color = snakeColor

    def key_event(self,event):
        # handle control input
        if event.key == pygame.K_UP and not self.vy == vel:
            self.vy = -vel            #Because this is a reverse y-axis
            self.vx = 0
        if event.key == pygame.K_DOWN and not self.vy == -vel:
            self.vy = vel
            self.vx = 0
        if event.key == pygame.K_RIGHT and not self.vx == -vel:
            self.vx = vel
            self.vy = 0
        if event.key == pygame.K_LEFT and not self.vx == vel:
            self.vx = -vel
            self.vy = 0

    def move(self):
        # "Movement" = Sequence of making a pixel for snake's head and then removing the end pixel
        self.x += self.vx                #Increment based on direction of x and y
        self.y += self.vy

        r,g,b,a = self.surface.get_at((self.x,self.y))

        if (r,g,b) == snakeColor:
            self.crashed = True
        elif (r,g,b) == wallColor:
            self.crashed = True
        elif (r,g,b) == snake2Color:
            self.crashed = True
        #if (self.x,self.y) in self.body:   
         #   self.crashed = True
        
        self.body.insert(0,(self.x,self.y))  #Insert the new item into 1st place of list

        #if (self.grow_to > self.length):
            #self.length += 1
        
        if len(self.body) > self.length:     #Remove the last item if body is longer than default length
            self.body.pop()


    def draw(self,ate):
        if ate == False:
            x,y = self.body[0]                     #Draw the head
            #self.surface.set_at((x,y),self.color)
            pygame.draw.rect(self.surface,self.color,(x,y,snakex,snakey),0)
            x,y = self.body[-1]                    #Remove the tail
            pygame.draw.rect(self.surface,bgColor,(x,y,snakex,snakey),0)
        if ate == True:
            for x,y in self.body:
                pygame.draw.rect(self.surface,self.color,(x,y,snakex,snakey),0)
        #self.surface.set_at((x,y),bgColor)

    def eat(self):            #Growing worm length 
        self.length += foodInc

    def position(self):
        return self.x, self.y
#----------------------------------------------------------------------------
class Worm2:
    # A second worm
    
    def __init__(self,surface):
        self.surface = surface
        self.x = int(snake2Pos[0])
        self.y = int(snake2Pos[1])
        self.length = iniLength
        self.vx = 0
        self.vy = -1           #Initial movement
        self.body = []
        self.crashed = False
        self.color = snake2Color

    def key_event(self,event):
        # handle control input
        if event.key == pygame.K_w and not self.vy == vel:
            self.vy = -vel            #Because this is a reverse y-axis
            self.vx = 0
        if event.key == pygame.K_s and not self.vy == -vel:
            self.vy = vel
            self.vx = 0
        if event.key == pygame.K_d and not self.vx == -vel:
            self.vx = vel
            self.vy = 0
        if event.key == pygame.K_a and not self.vx == vel:
            self.vx = -vel
            self.vy = 0

    def move(self):
        global wallCrash
        # "Movement" = Sequence of making a pixel for snake's head and then removing the end pixel
        self.x += self.vx                #Increment based on direction of x and y
        self.y += self.vy

        r,g,b,a = self.surface.get_at((self.x,self.y))

        if (r,g,b) == snake2Color:
            self.crashed = True
        elif (r,g,b) == wallColor:
            self.crashed = True
        elif (r,g,b) == snakeColor:
            self.crashed = True
        #if (self.x,self.y) in self.body:   
         #   self.crashed = True
        
        self.body.insert(0,(self.x,self.y))  #Insert the new item into 1st place of list

        
        if len(self.body) > self.length:     #Remove the last item if body is longer than default length
            self.body.pop()


    def draw(self,ate):
        if ate == False:
            x,y = self.body[0]                     #Draw the head
            pygame.draw.rect(self.surface,self.color,(x,y,snakex,snakey),0)
            x,y = self.body[-1]                    #Remove the tail
            pygame.draw.rect(self.surface,bgColor,(x,y,snakex,snakey),0)
        if ate == True:
            for x,y in self.body:
                pygame.draw.rect(self.surface,self.color,(x,y,snakex,snakey),0)

    def eat(self):            
        self.length += foodInc

    def position(self):
        return self.x, self.y
#----------------------------------------------------------------------------


def main():
    result = gameRun()
    if result == 1:
        pass
    if result == 2:
        pass
    if result == 3:
        pass
    
        
#Initialize 
def gameRun():
    global screen
    global score
    w = Worm(screen)
    w2 = Worm2(screen)
    f = Food(screen)
    screen.fill(bgColor)
    pygame.draw.rect(screen,wallColor,(0,0,width,10),0)
    pygame.draw.rect(screen,wallColor,(0,0,10,height),0)
    pygame.draw.rect(screen,wallColor,(width-10,0,10,height),0)
    pygame.draw.rect(screen,wallColor,(0,height-10,width,10),0)
    running = True

    while running:
        w.move()
        w.draw(False)    #Draw before move because we need that box to be colored first before collision can be detected
        w2.move()
        w2.draw(False)
        f.draw()

        #Collision Detection for Snake 1
        if w.crashed:
            running = False
            print("Snake 1 Collides")
        elif f.check(w.x,w.y):       #Send snake's head position
            score += 1
            w.eat()
            print("Score: %d" %score)
            f.erase()
            w.draw(True)
            f = Food(screen)          # make new food
    
        #Collision Detection for Snake 2
        if w2.crashed:
            running = False
            print("Snake 2 Collides")
        elif f.check(w2.x,w2.y):       #Send snake's head position
            score += 1
            w2.eat()
            print("Score(2): %d" %score)
            f.erase()
            w2.draw(True)
            f = Food(screen)          # make new food
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                w.key_event(event)
                w2.key_event(event)
                    
        pygame.display.flip()
        clock.tick(fps)

def terminate():
    pygame.display.quit()
    pygame.quit()

main()
