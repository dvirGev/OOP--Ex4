import pygame
import os
print()
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(r'../shaked.wav')
pygame.mixer.music.play(-1)