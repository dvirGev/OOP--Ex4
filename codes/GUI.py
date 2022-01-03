from os import system
import pygame
from pygame import *
# init pygame
WIDTH, HEIGHT = 1080, 720
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
background_image = image.load('background.png')
file = 'song.wav'
mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.
mixer.music.play()
font.init()
# display.flip()
while True:
    background_image = transform.scale(background_image, (screen.get_width(), screen.get_height()))
    screen.blit(background_image, [0,0])
    # display.flip()
    display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    