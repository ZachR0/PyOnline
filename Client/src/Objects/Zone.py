import Console.Manage
#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import time

#PyOnline
import Player.MainPlayer
import Video.PyGame
import Dialog.Popup
import Dialog.Global
import Camera.Manage
import Maps.Tiled

#PyGame
import pygame
from pygame.locals import *

#     _______________________
# ___/ Varaible Declaration  \__________________________________________________
Font = None
Last_Triggered_Zone_Name = None
Zone_Name_Surface = None

#     _______________________
# ___/ Function Declaration  \__________________________________________________
def Trigger(ID, Zone_Name):
    global Last_Triggered_Zone_Name
    global Font
    global Zone_Name_Surface
    
    if Last_Triggered_Zone_Name != Zone_Name:
        #Set Last Triggered Zone Name as the current
        Last_Triggered_Zone_Name = Zone_Name

        #Load our font
        Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 18)

        #Render Zone_Name
        Zone_Name_Surface = Font.render(str(Zone_Name), False, (255,0,0))

        #Write Zone Change Info to Console
        Console.Manage.Write(str("Entering " + str(Zone_Name)), (255,250,205))

        #Allow the Zone_Name_Surface to be displayed for one second
        time.sleep(1)

        #Reset Zone_Name_Surface Data
        Zone_Name_Surface = None


def DeTrigger():
    #Do nothing
    pass
