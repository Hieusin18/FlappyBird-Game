import pygame
from random import randint
pygame.mixer.init()
sound_wing = pygame.mixer.Sound("wing.wav")
sound_point = pygame.mixer.Sound("point.wav")
sound_hit = pygame.mixer.Sound("hit.wav")
sound_die = pygame.mixer.Sound("die.wav")

WIDTH,HEIGHT=400,600

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
running = True


GREEN = (0,200,0)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW =(255,255,0)
SKY_BLUE = (135, 206, 235)

TUBE_WIDTH = 60
TUBE_VELOCITY = 3  
TUBE_GAP = 150

tube1_x = 600
tube2_x = 800
tube3_x = 1000
tube1_height = randint(100,300)
tube2_height = randint(100,300)
tube3_height = randint(100,300)

BIRD_X = 50
bird_y = 400
BIRD_WIDTH =35
BIRD_HEIGHT =35
bird_drop_velocity = 0
GRAVITY = 0.3

score =0 
best_score = 0
font_score = pygame.font.SysFont('impact',40)
font_endgame = pygame.font.SysFont('impact', 30)

tube1_pass =False
tube2_pass =False
tube3_pass =False

pausing = False
game_started = False

background_image=pygame.image.load("background-night.png")
background_image=pygame.transform.scale(background_image,(WIDTH,HEIGHT))

bird_image=pygame.image.load("bluebird-downflap.png")
bird_image=pygame.transform.scale(bird_image,(BIRD_WIDTH,BIRD_HEIGHT))

sand_image=pygame.image.load("ground.png")
sand_image=pygame.transform.scale(sand_image,(WIDTH,50))
sand_x1 = 0
sand_x2 = 400
GROUND_SPEED = 3

tube_image=pygame.image.load("tube.png")
tube_image = pygame.transform.scale(tube_image, (TUBE_WIDTH, 400))  
tube_image_flip = pygame.transform.flip(tube_image, False, True)

gameover_image = pygame.image.load("gameover.png")
gameover_image = pygame.transform.scale(gameover_image, (192, 42))

   

icon = pygame.image.load("favicon.ico")  
pygame.display.set_icon(icon)
while running:
    clock.tick(60)
    screen.fill(GREEN) 
    screen.blit(background_image,(0,0))
    
  
    tube1_rect=screen.blit(tube_image_flip,(tube1_x,tube1_height-400))
    tube2_rect=screen.blit(tube_image_flip,(tube2_x,tube2_height-400))
    tube3_rect=screen.blit(tube_image_flip,(tube3_x,tube3_height-400))
    
    tube1_rect_inv=screen.blit(tube_image,(tube1_x,tube1_height+TUBE_GAP))
    tube2_rect_inv=screen.blit(tube_image,(tube2_x,tube2_height+TUBE_GAP))
    tube3_rect_inv=screen.blit(tube_image,(tube3_x,tube3_height+TUBE_GAP))
   
    sand_rect = pygame.Rect(0, 540, WIDTH, 60)
    screen.blit(sand_image, (sand_x1, 550))
    screen.blit(sand_image, (sand_x2, 550))
    if not pausing:
        sand_x1 -= GROUND_SPEED
        sand_x2 -= GROUND_SPEED
    if sand_x1 <= -WIDTH:
        sand_x1 = sand_x2 + WIDTH
    if sand_x2 <= -WIDTH:
        sand_x2 = sand_x1 + WIDTH
    sky_rect=pygame.Rect(0,0,WIDTH,5)
    
    bird_rect=screen.blit(bird_image,(BIRD_X,bird_y))

    if game_started:
        tube1_x =  tube1_x - TUBE_VELOCITY
        tube2_x =  tube2_x - TUBE_VELOCITY 
        tube3_x =  tube3_x - TUBE_VELOCITY 
        bird_y += bird_drop_velocity
        bird_drop_velocity += GRAVITY
    
    if tube1_x <-TUBE_WIDTH: 
        tube1_x = 550
        tube1_height = randint(100,300)
        tube1_pass =False
    if tube2_x <-TUBE_WIDTH:
        tube2_x = 550
        tube2_height = randint(100,300)
        tube2_pass =False
    if tube3_x <-TUBE_WIDTH:
        tube3_x = 550
        tube3_height = randint(100,300)
        tube3_pass =False
        
    score_txt = font_score.render(str(score),True,WHITE)
    screen.blit(score_txt,(WIDTH//2,5))
    
    if tube1_x+TUBE_WIDTH<=BIRD_X and tube1_pass == False : 
        score+=1
        tube1_pass = True
        sound_point.play()
    if tube2_x+TUBE_WIDTH<=BIRD_X and tube2_pass == False :
        score+=1
        tube2_pass = True 
        sound_point.play()
    if tube3_x+TUBE_WIDTH<=BIRD_X and tube3_pass == False :
        score+=1
        tube3_pass = True  
        sound_point.play() 
        
    if not pausing:     
        for tube in [tube1_rect,tube2_rect,tube3_rect,tube1_rect_inv,tube2_rect_inv,tube3_rect_inv,sand_rect,sky_rect]:
            if bird_rect.colliderect(tube): 
                sound_hit.play()
                sound_die.play()
                pausing =True
                TUBE_VELOCITY=0
                if score > best_score:
                    best_score = score
                    break
          
              
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_SPACE:
                if pausing:
                    bird_y =400
                    TUBE_VELOCITY = 3 
                    tube1_x=600
                    tube2_x=800 
                    tube3_x=1000
                    
                    score=0
                    pausing=False
                    game_started = False
                elif not game_started:
                    game_started = True
                    bird_drop_velocity = -10
                else:
                    bird_drop_velocity=0
                    bird_drop_velocity -=7
                    GRAVITY = 0.4
                    sound_wing.play()
    if bird_y + BIRD_HEIGHT >= 550:  
        bird_y = 550 - BIRD_HEIGHT
        bird_drop_velocity = 0 
    if not game_started and not pausing:
        start_txt = font_endgame.render("Press SPACE to start", True, YELLOW)
        screen.blit(start_txt, (WIDTH//2 - start_txt.get_width()//2, HEIGHT//2))
    if pausing:
        
        score_txt_big = font_endgame.render("Your Score: " + str(score), True, BLACK)
        best_txt = font_endgame.render("Best Score: " + str(best_score), True, BLUE)
        restart_txt = font_endgame.render("Press SPACE to restart", True, YELLOW)
        
        screen.blit(gameover_image, (WIDTH//2 - 192//2, HEIGHT//2 - 100))
        screen.blit(score_txt_big, (WIDTH//2 - score_txt_big.get_width()//2, HEIGHT//2 - 40))
        screen.blit(best_txt, (WIDTH//2 - best_txt.get_width()//2, HEIGHT//2))
        screen.blit(restart_txt, (WIDTH//2 - restart_txt.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()
 
pygame.quit()
    
    

    

