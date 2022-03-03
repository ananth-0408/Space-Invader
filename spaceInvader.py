import pygame
import moviepy
from moviepy.editor import *
import random
import time
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((900, 600))
background = pygame.image.load('./Images/space-back.jpg')
background = pygame.transform.scale(background, (900, 600))
gameOverVideo = moviepy.editor.VideoFileClip("./End Credits/end credits.mp4")
mixer.music.load('./Songs/bg_music.mp3')
mixer.music.set_volume(0.12)
mixer.music.play(-1)

#score
score = 0
font = pygame.font.Font('freesansbold.ttf', 28)
#coords
textX = 10
textY = 10

pygame.display.set_caption("Space Invader")
image = pygame.image.load('./Images/spaceship.png')
pygame.display.set_icon(image)

playerImg = pygame.image.load('./Images/char.png')
playerX = 400
playerY = 490
playerX_change = 0

enemyX = []
enemyY = []
enemyImg = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies) :
	img = pygame.image.load('./Images/space-invaders.png')
	img = pygame.transform.flip(img, False, True)
	enemyImg.append(pygame.transform.scale(img, (65, 65)))
	enemyX.append(random.randint(0, 800))
	enemyY.append(random.randint(50, 250))
	enemyX_change.append(0.5)
	enemyY_change.append(40)


#gameovertxt
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)
yourScoreFont = pygame.font.Font('freesansbold.ttf', 20)

bulletImg = pygame.image.load('./Images/bullet.png')
bulletX = 0
bulletY = 490
bulletX_change = 0.5
bulletY_change = 1
bullet_state = "ready"

playerImg = pygame.transform.scale(playerImg, (100, 100))
bulletImg = pygame.transform.scale(bulletImg, (45, 45))

bulletSound = mixer.Sound('./Songs/laser.mp3')
explosion = mixer.Sound('./Songs/explosion.mp3')
explosion.set_volume(1.7)
bulletSound.set_volume(1.0)

def showScore(x, y) :
	scoreText = font.render('Score : ' + str(score), True, (255, 255, 255))
	screen.blit(scoreText, (x, y))

def gameOverTxt() :
	mixer.music.stop()
	# gameOverVideo.subclip(0, 5)
	gameFinalVideo = gameOverVideo.fx(vfx.resize, width=900)
	gameFinalVideo.volumex(0.01)
	gameFinalVideo.preview()
	




def player(x, y) :
	screen.blit(playerImg, (x, y))

def enemy(x, y, i) :
	screen.blit(enemyImg[i], (x, y))

def fireBullet(x, y) :
	global bullet_state
	bullet_state = "fire"

	

def collisionCheck(enemyX, enemyY, bulletX, bulletY) :
	distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
	if bullet_state == "ready": 
		return False
	if distance < 27 :
		return True
	else :
		return False

running = True
while running :
	screen.fill((0, 0, 0))
	screen.blit(background, (0, 0))


	# keyboard events
	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			running = False
		if event.type == pygame.KEYDOWN :
			if event.key == pygame.K_LEFT :
				playerX_change = -0.6
			if event.key == pygame.K_RIGHT :
				playerX_change = 0.6
			if event.key == pygame.K_SPACE :
				bulletX = playerX
				bulletSound.play()
				fireBullet(bulletX, bulletY)

		if event.type == pygame.KEYUP :
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
				playerX_change = 0
				playerX += 3
			
	playerX += playerX_change
	# end of keyboard events

	# out of bounds check
	if playerX >= 800 :
		playerX = 800
	elif playerX <= 0 :
		playerX = 0

	# enemy movement
	for i in range(num_of_enemies) :

		#game ovah
		if enemyY[i] > 440 :
			for j in range(num_of_enemies) :
				enemyY[j] = 2000
			gameOverTxt()

			break


		if enemyX[i] >= 850 :
			enemyX_change[i] = -0.5
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] <= 0 :
			enemyX_change[i] = 0.5
			enemyY[i] += enemyY_change[i]

		#collision
		collision = collisionCheck(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision :
			explosion.play()
			bulletY = 490
			bullet_state = "ready"
			score += 1
			enemyX[i] = random.randint(0, 800)
			enemyY[i] = random.randint(50, 250)

		enemy(enemyX[i], enemyY[i], i)
		enemyX[i] += enemyX_change[i]

	if bulletY <= 0:
		bulletY = 490
		bullet_state = "ready"
	if bullet_state == "fire":
		fireBullet(bulletX, bulletY)
		screen.blit(bulletImg, (bulletX + 25, bulletY))
		bulletY -= bulletY_change
	
	player(playerX, playerY)
	showScore(textX, textY)
	pygame.display.update()
