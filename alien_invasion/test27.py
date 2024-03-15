import pygame, sys

pygame.init()
size = width, height = 600, 400
BLACK = 0, 255, 0
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
icon = pygame.image.load("images/PYG03-flower.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pygame壁球")
ball = pygame.image.load("images/PYG02-ball.gif")
ballRect = ball.get_rect()
fps = 100
fclock = pygame.time.Clock()
bgColor = pygame.Color("green")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)
    pygame.display.update()
    fclock.tick(fps)
