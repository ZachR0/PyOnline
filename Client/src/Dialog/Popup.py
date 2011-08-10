#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline
import Camera.Manage
import Video.PyGame
import Video.FPS
import Player.MainPlayer

#PyGame
import pygame
from pygame.locals import *

Dialog_Font = None

#Creates a Popup Dialog Box, returns the Surface
def Display(Text):
    #Setup Variables
    global Dialog_Font
    
    #Load Font
    Dialog_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 14)

    #Load Dialog Surface Background
    Dialog_Surface = pygame.image.load("data/images/Dialog_Background.png")

    #Generate Dialog Message
    Dialog_Text_Surface = []

    #Create a surface for each character
    for i in range(0, len(Text)):
        Dialog_Text_Surface.append(Dialog_Font.render(str(Text[i]), False, (255,255,255)))

    #Render Dialog Message To Dialog_Surface
    count = 0
    line_count = 0
    #Go through each character
    for i in range(0, len(Dialog_Text_Surface)):
        #Blit Surface Character
        Dialog_Surface.blit(Dialog_Text_Surface[i], (count*8,line_count*14))

        #60 char per line max
        if count >= 60:
            #Reset count
            count = -1

            #Increast line count
            line_count += 1

        #Increase count
        count += 1

    #Return Dialog Surface
    return Dialog_Surface