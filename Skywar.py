import pygame
import random
import math

pygame.init()

#color
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
blue=(40,240,180)
green=(40,240,120)


#creating a window 
screen_width=800
scree_hight=600
gamewindow=pygame.display.set_mode((screen_width,scree_hight))
pygame.display.update()
background=pygame.image.load('space.jpg')
background=pygame.transform.scale(background,(screen_width,scree_hight)).convert_alpha()

#set title and icone
pygame.display.set_caption("Fight for Galaxy")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
pygame.display.update()

#games pecific variable
exit_game=False
game_over=False

#player
playerimg=pygame.image.load('spaceship.png')
playerX=370
playerY=480
velocity_x=0
velocity_y=0

#Enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_velocity=[]
enemyY_velocity=[]
num_of_enemies=8
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))
    enemyX_velocity.append(0.5)
    enemyY_velocity.append(20)


#Bullet
#ready=we can't see the bullet on screen
#fire=bullet is currently in screen
bulletimg=pygame.image.load('bullet.png')
bulletX=playerX
bulletY=playerY
bullet_velocity_X=0
bullet_velocity_Y=3
bullet_state="ready"
score=0

def player(x,y):
    gamewindow.blit(playerimg,(x,y))

def enemy(x,y,i):
    gamewindow.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    gamewindow.blit(bulletimg,(x+16,y+10))   

#Creating text on the screen
font=pygame.font.SysFont(None,25)
def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    gamewindow.blit(screen_text,(x,y))

def collision(x1,y1,x2,y2):  
    distance=math.sqrt((math.pow(x1-x2,2))+(math.pow(y1-y2,2))) 
    return distance

while not exit_game:
   # gamewindow.fill(black)
    gamewindow.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit_game=True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                velocity_x=-1.5
                bulletX=playerX
            if event.key==pygame.K_RIGHT:
                velocity_x=1.5
                bulletX=playerX
            if event.key==pygame.K_UP:
                velocity_y=-1.5
            
            if event.key==pygame.K_DOWN:
                velocity_y=+1.5

            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX=playerX
                    bulletY=playerY
                    fire_bullet(bulletX,bulletY)        

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                velocity_x=0
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                velocity_y=0
            
    playerX+=velocity_x
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736    
  
    playerY+=velocity_y
    if playerY<=0:
        playerY=0
    elif playerY>=536:
        playerY=536

   #Bullet Movement
    if bulletY<=0:
        bulletY=playerY
        bullet_state="ready" 

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bullet_velocity_Y     
    
 #Enemy Movement
    for i in range(num_of_enemies):        
        enemyX[i]+=enemyX_velocity[i]

        if enemyX[i]<=0:
            enemyX_velocity[i]=1
            enemyY[i]+=enemyY_velocity[i]
        elif enemyX[i]>=736:
            enemyX_velocity[i]=-1
            enemyY[i]+=enemyY_velocity[i]   

        if collision(enemyX[i],enemyY[i],bulletX,bulletY)<10:
            score+=5  
            bullet_state="ready"
            enemyX[i]=random.randint(0,400)
            enemyY[i]=random.randint(0,20)  
        text_screen("Score:"+str(score),white,700,3)
        enemy(enemyX[i],enemyY[i],i)    

        distance=collision(enemyX[i],enemyY[i],playerX,playerY)
        if distance<25:
            game_over=True
            break
                        
        if enemyY[i]>550:
            game_over=True
            break
            pygame.quit()

              
    player(playerX,playerY)
    pygame.display.update()
    

quit()