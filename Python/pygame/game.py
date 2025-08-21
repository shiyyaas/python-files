import pygame

pygame.init()

#SCREEN SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

img = pygame.image.load("images/bird.png")
clock = pygame

run = True
x = 0

while run:
    screen.fill((0, 0, 0))

    screen.blit(img, (x, 30))
    x += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()