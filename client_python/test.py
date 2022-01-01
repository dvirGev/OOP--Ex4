import pygame


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(r'pokemonSong.mp3')
pygame.mixer.play(-1, 0.0)
