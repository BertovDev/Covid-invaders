import random
import math

import pygame
from pygame import mixer

# inicializamos
pygame.init()

# Creamos la pantalla
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("./images/wallpaper.png")

# Background sounds
mixer.music.load("./sounds/background.mp3")
mixer.music.set_volume(0.25)
mixer.music.play(-1) # Eso genera el loop

# Titulo e Icono del juego
pygame.display.set_caption("Covid invader")
icon = pygame.image.load("./images/alien.png")
pygame.display.set_icon(icon)

# Jugador
playerImg = pygame.image.load("./images/spaceship.png")

# Posicion del Jugador
playerX = 370 # Valores en relacion a la pantalla
playerY = 480
playerX_change = 0

# Enemigo
ENEMY_SPEED = 0.2
enemyImg = [] # Lista vacia de enemigos
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
nums_of_enemies = 6

for i in range(nums_of_enemies):
    enemyImg.append(pygame.image.load("./images/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(ENEMY_SPEED)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("./images/bullet.png")
bulletX = playerX
bulletY = playerY
BULLET_SPEED = 0.8
bulletY_change = BULLET_SPEED
bullet_state = False

# Puntaje
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("freesansbold.ttf",64)

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200,250))

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

# Creamos una funcion para player
def player(x,y):
    screen.blit(playerImg,(x,y)) # metodo que dibuja en la pantalla

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
# Creamos bucle de juego
running = True

while running:
    
    # Fondo de pantalla
    screen.fill((0,0,0))
    # Agrego background
    screen.blit(background,(0,0))
    
    
    for event in pygame.event.get(): # Con esto accedemos a todos los eventos
        if event.type == pygame.QUIT:
            running = False
        
        # Si alguna tecla es presionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                   playerX_change = -0.3
                
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
                
            if event.key == pygame.K_SPACE:
                if bullet_state == False:
                    bulletX = playerX
                    bulletY = playerY
                    bullet_sound = mixer.Sound("./sounds/laser1.wav")
                    bullet_sound.play()
                    bullet_sound.set_volume(0.2)
                    bullet_state = True
                
        # Si la tecla deja de ser presionada
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            
            
    # Movimiento Jugador
    playerX += playerX_change
    
    # Chequeo si llega al borde de la pantalla
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    player(playerX,playerY)
    
    # Movimiento del enemigo
    
    for i in range(nums_of_enemies):
        
        # Game over
        if enemyY[i] > 440:
            for j in range(nums_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -ENEMY_SPEED
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = ENEMY_SPEED
            enemyY[i] += enemyY_change[i]
        
        
        # Collitions
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Reseteo la bullet
            bulletY = playerY
            bullet_state = False
            score_value += 1
            collision_sound = mixer.Sound("./sounds/collision.wav")
            collision_sound.play()
            collision_sound.set_volume(0.5)
            # Creo un nuevo enemigo en posicion random
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i],enemyY[i],i)

    
    # Movimiento Bullet
    # Si la bullet llega al tope de pantalla se borra
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = False
    
    # Seteo para poder disparar otra bullet
    if bullet_state == True:
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)
        
    # Aumento dificultad
    if score_value >= 10:
        ENEMY_SPEED = 0.3
    if score_value >= 20:
        ENEMY_SPEED = 0.5
    if score_value >= 50:
        ENEMY_SPEED = 0.7
    
    # actualizar puntaje
    show_score(textX,textY)
    
    
    pygame.display.update() # actualiza la pantalla