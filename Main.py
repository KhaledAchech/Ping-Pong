import pygame, sys, random	
from tkinter import *
from tkinter import messagebox

def player_animation():
	#linking the speed value to the player y position
	player.y += player_speed

	#avoid getting out of screen ==> basically teleporting the player to the very top or to the very bottom
	#if he s going to surpass the limits
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_hight:
		player.bottom = screen_hight

def opponent_ai():
 	#Opponenet ai
	if opponent.top < ball.y:
		opponent.top += opponent_speed
	if opponent.bottom > ball.y:
		opponent.bottom -= opponent_speed
 		
 	#preventing the opponent from going out of the screen
	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_hight:
		opponent.bottom = screen_hight


def ball_animation():
#ball animation
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_hight:
		pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1

	if ball.left <= 0:
		pygame.mixer.Sound.play(score_sound)
		player_score += 1
		score_time = pygame.time.get_ticks()

	if ball.right >= screen_width:
		pygame.mixer.Sound.play(score_sound)
		opponent_score += 1
		score_time = pygame.time.get_ticks()

	#Colisions
	if ball.colliderect(player) and ball_speed_x > 0:
		pygame.mixer.Sound.play(pong_sound)
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0:
		pygame.mixer.Sound.play(pong_sound)
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

def ball_restart():
	global ball_speed_x, ball_speed_y, score_time

	current_time = pygame.time.get_ticks()
	#teleporting the ball to the center of the screen
	ball.center = (screen_width/2, screen_hight/2)

	#the countdown
	if current_time - score_time < 700:
		number_three = game_font.render('3',False,light_bleu)
		screen.blit(number_three,(screen_width/2 - 10, screen_hight/2 + 20))

	if 700 < current_time - score_time < 1400:
		number_two = game_font.render('2',False,light_bleu)
		screen.blit(number_two,(screen_width/2 - 10, screen_hight/2 + 20))

	if 1400 < current_time - score_time < 2100:
		number_one = game_font.render('1',False,light_bleu)
		screen.blit(number_one,(screen_width/2 - 10, screen_hight/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_x, ball_speed_y = 0, 0
	else:
		#restarting the ball in a random direction
		ball_speed_x = 7 * random.choice((1, -1))
		ball_speed_y = 7 * random.choice((1, -1))
		score_time = None
	


#General settings
pygame.mixer.pre_init(44100,-16,2,512)# ==> initializing the sound buffer to 512 to avoid sound effects delay
pygame.init() # ==>Initializing pygame can help avoid some errors, to be hones i don't know exactly what kind of errors 
			  #	but it's advisable to use.
clock = pygame.time.Clock() # ==>This 'clock' will help set the frames needed afterwards so that the computer doesn't run the game at full speed. 

#Setting up the main window
screen_width = 1280
screen_hight = 960
screen = pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption('Ping Pong')

#game rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_hight/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_hight/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_hight/2 - 70, 10, 140)

#Color Scheme
bg_color = pygame.Color('grey12')
light_bleu = (104,176,171)

#ball speed
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

#player speed
player_speed = 0

#opponent speed
opponent_speed = 7


#text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

#score timer
score_time = True

#sound effects
pong_sound = pygame.mixer.Sound("Sound_effects/pong.ogg")
score_sound = pygame.mixer.Sound("Sound_effects/score.ogg")

#The main loop
while True:
	#handling input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:# ==> you can find all pygame events and locals on : https://www.pygame.org/docs/ref/event.html
			pygame.quit()
			sys.exit()

		#player movement 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed += 7
			if event.key == pygame.K_UP:
				player_speed -= 7

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -= 7
			if event.key == pygame.K_UP:
				player_speed += 7

		
	#calling ball_animation function
	ball_animation()

	#preventing the player from going out of the screen
	player_animation()

	#opponent opponent_ai
	opponent_ai()

	#Drawing The game elements
	screen.fill(bg_color)
	pygame.draw.rect(screen,light_bleu,player)
	pygame.draw.rect(screen,light_bleu,opponent)
	pygame.draw.ellipse(screen,light_bleu,ball)
	pygame.draw.aaline(screen,light_bleu,(screen_width/2,0),(screen_width/2,screen_hight))

	if score_time:
		ball_restart()

	player_text = game_font.render(f"{player_score}",False,light_bleu)
	screen.blit(player_text,(660,470))# ==> putting the text surface on the screen surface
	opponent_text = game_font.render(f"{opponent_score}",False,light_bleu)
	screen.blit(opponent_text,(600,470))

	#Updating the frame
	pygame.display.flip()# ==> Take everything that came before the loop and draw a pic of that
	clock.tick(60)# ==> Setting the number of frames to 60 frame per second.