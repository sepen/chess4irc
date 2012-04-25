import pygame, time

personaje = pygame.image.load("image.png")
screen = pygame.display.set_mode((480,480))
screen.blit(personaje,(10,10))
pygame.display.update()
time.sleep(2)
