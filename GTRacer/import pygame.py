import pygame
from sys import exit




pygame.init()
screen = pygame.display.set_mode((1427,715))
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_d]:
        print("right")



    pygame.display.update()
    clock.tick(60)
        