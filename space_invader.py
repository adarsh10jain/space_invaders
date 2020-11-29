import pygame
import random
import math
from pygame import mixer

pygame.init()

#creating the screen

screen=pygame.display.set_mode((800,600))

#tile and icon

pygame.display.set_caption("#SPACE INVADERS#")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player image
player_img=pygame.image.load('space_ship.png')
playerX=370
playerY=480
playerX_chg=0

#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',34)

#game_over_font
game_over=pygame.font.Font('freesansbold.ttf',64)

#background image
#background_img=pygame.image.load('space_background.png')


#background sound
mixer.music.load("background_music.mp3")
mixer.music.play(-1)




#enemy image
enemy_img=[]
enemyX=[]
enemyY=[]
enemyX_chg=[]
enemyY_chg=[]
number_of_enemy=6
for i in range(number_of_enemy):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_chg.append(0.3)
    enemyY_chg.append(40)

#ready-you can't see the bullent in the screen 
#fire-the bullet is currntly moving

#bullet image
bullet_img=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_chg=0
bulletY_chg=4
bullet_state='ready'


def player(x,y):
    screen.blit(player_img,(x,y))


def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet_img,(x+16,y+10))

def iscollision(bulletX,bulletY,enemyX,enemyY):
    distance=math.sqrt((math.pow(bulletX-enemyX,2))+(math.pow(bulletY-enemyY,2)))
    if distance <=20:
        return True
    else :
        return False

def game_over_text():
    over_text=game_over.render("GAME OVER",True,(0,0,0))
    screen.blit(over_text,(200,250))

def score():
    score=font.render("SCORE: "+ str(score_value),True,(0,0,0))
    screen.blit(score,(10,10))


#Game loop which runs infinitely and listen the events
running=True
while running:

#for background of the game window
    screen.fill((255,255,255))

    #background image
    #screen.blit(background_img,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_chg+=0.7
                #print("right key is pressed")
            if event.key == pygame.K_LEFT:
                playerX_chg-=0.7
                #print("right key is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_chg=0

    playerX+=playerX_chg

#creating the boundary for player
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
#creating the boundary for enemy
    for i in range(number_of_enemy):
        enemyX[i]+=enemyX_chg[i]

        #game over
        if enemyY[i]>=440:
            for j in range(number_of_enemy):
                enemyY[j]=4000
            game_over_text()
            break


        if enemyX[i]<=0:
            enemyX_chg[i]=0.3
            enemyY[i]+=enemyY_chg[i]
        elif enemyX[i]>=736:
            enemyX_chg[i]=-0.3
            enemyY[i]+=enemyY_chg[i]
        
#check for collision
        collision=iscollision(bulletX,bulletY,enemyX[i],enemyY[i])
        if collision:
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)
        


#bullet movement
    if bulletY == 0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_chg

#calling player functyion to draw player with blit function with new cordinates
    player(playerX,playerY)
    score()
    pygame.display.update()
