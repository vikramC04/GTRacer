import pygame
from sys import exit
from random import choice

class Racecar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        racecar = pygame.image.load('graphics/racecar/racecar_stationary.png').convert_alpha()
        racecar_small = pygame.transform.rotozoom(racecar, 0, 0.5)

        racecar_move = pygame.image.load('graphics/racecar/racecar_moving.png').convert_alpha()
        racecar_move_small = pygame.transform.rotozoom(racecar_move, 0, 0.5)

        self.racecar_animation = [racecar_small, racecar_move_small]
        self.cycle = 0
        self.image = self.racecar_animation[self.cycle]

        self.leftrect = self.image.get_rect(midbottom = (250, 700))
        self.middlerect = self.image.get_rect(midbottom = (700, 700))
        self.rightrect = self.image.get_rect(midbottom = (1175, 700))

        self.racecar_position = [self.leftrect,self.middlerect,self.rightrect]
        self.racecar_index = 0
        self.last_index = len(self.racecar_position) - 1
        self.rect = self.racecar_position[self.racecar_index]
        
        self.last_clicked = 0
    def animation(self):
        self.cycle += 0.1
        if self.cycle >= 2: self.cycle = 0
        self.image = self.racecar_animation[int(self.cycle)]
    def position(self):
        pressed = pygame.key.get_pressed()
        delay_interval = int(pygame.time.get_ticks()) - self.last_clicked
        if delay_interval > 200:
            if pressed[pygame.K_d] and self.racecar_index != self.last_index:
                self.racecar_index += 1
                self.last_clicked = int(pygame.time.get_ticks())    
            elif pressed[pygame.K_a] and self.racecar_index != 0:
                self.racecar_index -= 1
                self.last_clicked = int(pygame.time.get_ticks())
        
        self.rect = self.racecar_position[self.racecar_index]
    def update(self):
        self.animation()
        self.position()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "trash":
            trash_image = pygame.image.load('graphics/obstacles/trash_can.png').convert_alpha()     
            self.image = pygame.transform.smoothscale_by(trash_image, 1.5)
        elif type == "rock":
            self.image = pygame.image.load('graphics/obstacles/rock.png').convert_alpha()   
         
        self.rect = self.image.get_rect(center = (choice([250,700,1175]), -200))
    def movement(self):
        self.rect.y += 5
    def end_task(self):
        if self.rect.y >= 800: self.kill()
    def update(self):
        self.movement()
        self.end_task()

def sprite_collision():
    if pygame.sprite.spritecollide(racer.sprite, obstacle, False):
        obstacle.empty()
        return False
    return True

def score():
    current_score = int(pygame.time.get_ticks()/1000) - start_time
    score_text = score_font.render(f'Score:{current_score}', False, (0,0,0))
    score_text_rect = score_text.get_rect(center = (1340, 30))
    screen.blit(score_text, score_text_rect)
    return current_score

pygame.init()
screen = pygame.display.set_mode((1427,715))
pygame.display.set_caption('GTRacer')
clock = pygame.time.Clock()

game_font = pygame.font.Font('font/racesport.ttf', 50)
title_text = game_font.render("GTRacer", False, (255,255,255))
title_text_rect = title_text.get_rect(center = (713, 110))

start_text = game_font.render("Press Any Key To Start", False, (255,255,255))
start_text_rect = start_text.get_rect(center = (713, 650))

score_font = pygame.font.Font('font/emulogic.ttf', 20)

helmet = pygame.image.load('graphics/helmet.png').convert_alpha()
title_helmet = pygame.transform.rotozoom(helmet, 0, 0.7)
title_helmet_rect = title_helmet.get_rect(center = (713, 355))

racetrack_surf = pygame.image.load('graphics/racetrack.png').convert_alpha() 
racer = pygame.sprite.GroupSingle()
racer.add(Racecar())

obstacle = pygame.sprite.Group()

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

game_start = False
start_time = 0
current_score = 0

background_music = pygame.mixer.Sound('audio/race.wav')
background_music.play(loops = -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_start:
            if event.type == obstacle_timer:
                obstacle.add(Obstacle(choice(["rock", "trash"])))
        else:
            if event.type == pygame.KEYDOWN:
                game_start = True
                start_time = int(pygame.time.get_ticks()/1000)
                
           
    if game_start:
        screen.blit(racetrack_surf, (0,0))
        racer.draw(screen)
        racer.update()
        obstacle.draw(screen)
        obstacle.update()
        current_score = score()
        game_start = sprite_collision()
    else:
        screen.fill("#EE4E34")
        screen.blit(title_text,title_text_rect)
        screen.blit(start_text,start_text_rect)
        screen.blit(title_helmet, title_helmet_rect)

        if current_score != 0:
            score_text = game_font.render(f'Your Score:{current_score}', False, (255,255,255))
            score_text_rect = score_text.get_rect(center = (713, 580))
            screen.blit(score_text,score_text_rect)
    

    pygame.display.update()
    clock.tick(60)


