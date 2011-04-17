#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import sys
import os
import os.path
import shutil
import gc
import time
import thread
import zipfile

#Simple PyGame GUI
import SPG.gui
import SPG.defaultStyle

#PyOnline
import Video.PyGame
import Video.FPS
import Networking.Client

#PyGame
import pygame
from pygame.locals import *

from xml.dom import minidom
import urllib2

Clients_Node = None

current_Line = 0 #Used by Write() function

def Check():
    global Clients_Node
    
    Updates_Found = False

    #Make sure old update.xml does not exist locally
    if os.path.exists("update.xml"):
        #Remove old copy
        os.remove("update.xml")

    #Download update.xml
    u = urllib2.urlopen('http://pyonline.zachr.co/update.xml')
    localFile = open('update.xml', 'w')
    localFile.write(u.read())
    localFile.close()

    #Parse XML
    xmldoc = minidom.parse('update.xml')

    #Get Clients from XML
    Clients_Node = xmldoc.getElementsByTagName("clients")[0].childNodes

    #Get Current Version from XML (server ver)
    Remote_Ver = xmldoc.getElementsByTagName("clients")[0].getAttribute("ver")
    print "Current Client Ver (Server Side):", Remote_Ver

    #Check if an update is needed
    if str(Remote_Ver) != str(Networking.Client.CLIENT_VER):
        Updates_Found = True
    else:
        Updates_Found = False

    if Updates_Found == True:
        #Init Video
        Video.PyGame.InitVideo()

        #Setup Video
        Video.PyGame.SetVideo(800, 640, False)

        #Update Window Caption To Current Ver
        pygame.display.set_caption(str("PyOnline - " + str(Networking.Client.CLIENT_VER)))

        #Init FPS System
        Video.FPS.Init()

        #Inform user that an update is needed...
        Write("Updates needed! -- Starting update manager, please wait...")
        Write(str(str(Networking.Client.CLIENT_VER) + " ===> " + str(Remote_Ver)))

        #Update Display
        pygame.display.flip()

        #Wait a moment before continuing...
        time.sleep(3)

        #Figure out what OS we are using
        Platform_Data = os.uname()[0]

        #Startup Update Manager accordingly...
        if Platform_Data == "Darwin":
            #Startup Update Manager for OSX
            os.system("open ../../../Update_Manager.app/")
            time.sleep(0.2)
            sys.exit(0)

        elif Platform_Data == "Windows": #TODO: What is os.uname[0] value under win32?
            pass
        elif Platform_Data == "Linux": #TODO: What is os.uname[0] value under *nix systems
            pass


#Used to write text to the screen during updating
def Write(text, x=0, update_line=True, black=False):
    global current_Line

    #Font for update stuff
    Info_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 10)

    #Display Loding Information
    if black != True:
        InfoSurf = Info_Font.render(str(text), True, (255,255,255))
    else:
        InfoSurf = Info_Font.render(str(text), True, (0,0,0))

    Video.PyGame.Screen.blit(InfoSurf, (int(x),int(current_Line))) #Render Text

    if update_line == True:
        current_Line += 15