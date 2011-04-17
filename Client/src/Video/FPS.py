#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline
import Video
import Video.PyGame
import Camera.Manage
import Player.MainPlayer

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
FRAMES_PER_SEC = None
CLOCK = None

#     ________________________
# ___/ Function Declarations  \_________________________________________________
def Init():
    global FRAMES_PER_SEC
    global CLOCK

    FRAMES_PER_SEC = 60
    CLOCK = pygame.time.Clock()

#Ticks FPS Timer -- FPS Regulation
def Tick():
    global FRAMES_PER_SEC
    global CLOCK
    
    #Tick PyGame Clock for FPS regulation
    dt = CLOCK.tick(FRAMES_PER_SEC)
    return dt