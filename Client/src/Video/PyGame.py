import Networking.Client
import pygame.cursors
#     _________________
# ___/ Module Imports  \________________________________________________________
#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
Screen = None
Screen_Width = None
Screen_Height = None
Screen_Fullscreen = None

#     ________________________
# ___/ Function Declarations  \_________________________________________________

#Init PyGame and other subsets for video
def InitVideo():
    #Init Pygame
    pygame.init()

    #Hide Mouse
    #pygame.mouse.set_visible(0)

    #Set Mousr Cursor
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    #Enable Keyinput repeat
    pygame.key.set_repeat(1,1)

#Get PyGame video mode, screen attributes, etc
def SetVideo(Width, Height, Fullscreen):
    #Setup Variables
    global Screen
    global Screen_Width
    global Screen_Height
    global Screen_Fullscreen
    Screen_Width = Width
    Screen_Height = Height

    #Set screen size
    if Fullscreen == False:
        Screen = pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE, 32)
        Screen_Fullscreen = False
    else:
        Screen = pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE, 32)
        Screen_Fullscreen = True

    #Set Window caption
    pygame.display.set_caption(str("PyOnline - " + str(Networking.Client.CLIENT_VER)))

    #Fill screen with background color
    Screen.fill((0,0,0))

    #Update screen display
    pygame.display.flip()