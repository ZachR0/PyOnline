#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import thread

#PyOnline
import Camera.Manage
import Video.PyGame
import Video.FPS
import Maps.Tiled
import Player.MainPlayer

#PyGame
import pygame
from pygame.locals import *


#     ________________________
# ___/ Variable Declarations  \_________________________________________________
TILES_PER_THREAD_MAX = None
OBJECTS_PER_THREAD_MAX = None

#     ________________________
# ___/ Function Declarations  \_________________________________________________
#Seperates Collision Handling Into Different Threads
def Setup():
    global TILES_PER_THREAD_MAX
    global OBJECTS_PER_THREAD_MAX

    #Set Max number of tiles to check per thread
    if len(Maps.Tiled.Collision_Layer.Tiles) >= 100:
        TILES_PER_THREAD_MAX = len(Maps.Tiled.Collision_Layer.Tiles)/2
    else:
        TILES_PER_THREAD_MAX = len(Maps.Tiled.Collision_Layer.Tiles)

    #Set the Max number of objects to be checked per thread
    if len(Maps.Tiled.Level_Objects) >= 10:
        OBJECTS_PER_THREAD_MAX = len(Maps.Tiled.Level_Objects)/2
    else:
        OBJECTS_PER_THREAD_MAX = len(Maps.Tiled.Level_Objects)

    count = 0 #tmpLoop counter
    overallCount = 0 #Loop counter
    startElement = 0 #First tile in range
    endElement = 0 #Last tile in range
    no_increase = False #Prevents over increasing of "count"

    #Debug output
    #print "[Collision Manager]:{Tiles}:-Overall length: ", len(Maps.Tiled.Collision_Layer.Tiles)

    #Seperate Collision Tiles into detection threads
    for i in range(0, len(Maps.Tiled.Collision_Layer.Tiles)):
        if count >= TILES_PER_THREAD_MAX:
            #Set the elements
            startElement = i - count
            endElement = startElement + count

            #Debug output
            #print "[Collision Manager]:{Tiles}:-Starting new thread: start=", startElement, " end=", endElement

            #Start a new collision detection block thread
            thread.start_new_thread(Collision_Detection_Thread, (startElement, endElement))

            #Reset variables
            startElement = 0
            endElement = 0
            count = 0
            no_increase = True

        #Increase count?
        if no_increase == False:
            count += 1
        else:
            no_increase = False

        #Keep track of i, so we can add the remaining tiles to a thread
        overallCount = i

    #Start a new collision detection block thread for the remaining tiles
    startElement = (overallCount - count) + 1
    endElement = startElement + count
    #print "[Collision Manager]:{Tiles}:-Starting new thread: start=", startElement, " end=", endElement
    thread.start_new_thread(Collision_Detection_Thread, (startElement, endElement))
    
    #Reset all variables
    count = 0 #tmpLoop counter
    overallCount = 0 #Loop counter
    startElement = 0 #First object in range
    endElement = 0 #Last object in range
    no_increase = False #Prevents over increasing of "count"

    #Debug output
    #print "\n[Collision Manager]:{Objects}:-Overall length: ", len(Maps.Tiled.Level_Objects)

    #Seperate Object into trigger detection threads
    for i in range(0, len(Maps.Tiled.Level_Objects)):
        if count >= OBJECTS_PER_THREAD_MAX:
            #Set the elements
            startElement = i - count
            endElement = startElement + count

            #Debug output
            #print "[Collision Manager]:{Objects}:-Starting new thread: start=", startElement, " end=", endElement

            #Start a new collision detection block thread
            thread.start_new_thread(Object_Trigger_Detection_Thread, (startElement, endElement))

            #Reset variables
            startElement = 0
            endElement = 0
            count = 0
            no_increase = True

        #Increase count?
        if no_increase == False:
            count += 1
        else:
            no_increase = False

        #Keep track of i, so we can add the remaining tiles to a thread
        overallCount = i

    #Start a new object trigger detection block thread for the remaining tiles
    startElement = (overallCount - count) + 1
    endElement = startElement + count
    #print "[Collision Manager]:{Objects}:-Starting new thread: start=", startElement, " end=", endElement
    thread.start_new_thread(Object_Trigger_Detection_Thread, (startElement, endElement))

#Collision Detection - Collision Layer and Main Player
def Collision_Detection_Thread(start, end):
    while True:
        #Check Collision Against Level Collision Layer and Main Player
        for i in range(int(start), int(end)):
            if(Maps.Tiled.Collision_Layer.Tiles[i].Tile_Surface.get_rect(center=(Maps.Tiled.Collision_Layer.Tiles[i].Tile_X, Maps.Tiled.Collision_Layer.Tiles[i].Tile_Y), \
            size=(Maps.Tiled.Collision_Layer.Tiles[i].Tile_Surface.get_width() + 10, Maps.Tiled.Collision_Layer.Tiles[i].Tile_Surface.get_height() + 10)).colliderect\
                (Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_rect(size=(Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_width(), \
                Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_height()), center=(Player.MainPlayer.XPOS, Player.MainPlayer.YPOS)))) == True:
                    
                    #if Player.MainPlayer.Moving_Right == True:
                    #    Player.MainPlayer.XPOS -= Player.MainPlayer.Move_Speed+5
                    #elif Player.MainPlayer.Moving_Left == True:
                    #    Player.MainPlayer.XPOS += Player.MainPlayer.Move_Speed+5
                    #elif Player.MainPlayer.Moving_Up == True:
                    #    Player.MainPlayer.YPOS += Player.MainPlayer.Move_Speed+5
                    #elif Player.MainPlayer.Moving_Down == True:
                    #    Player.MainPlayer.YPOS -= Player.MainPlayer.Move_Speed+5

                    if Player.MainPlayer.Moving_Up == True:
                        Player.MainPlayer.YPOS += Player.MainPlayer.Move_Speed
                        Player.MainPlayer.Can_Move_Up = False
                        Player.MainPlayer.Can_Move_Down = True
                        Player.MainPlayer.Can_Move_Left = True
                        Player.MainPlayer.Can_Move_Right = True
                        
                    elif Player.MainPlayer.Moving_Down == True:
                        Player.MainPlayer.YPOS -= Player.MainPlayer.Move_Speed
                        Player.MainPlayer.Can_Move_Up = True
                        Player.MainPlayer.Can_Move_Down = False
                        Player.MainPlayer.Can_Move_Left = True
                        Player.MainPlayer.Can_Move_Right = True

                    elif Player.MainPlayer.Moving_Left == True:
                        Player.MainPlayer.XPOS += Player.MainPlayer.Move_Speed
                        Player.MainPlayer.Can_Move_Up = True
                        Player.MainPlayer.Can_Move_Down = True
                        Player.MainPlayer.Can_Move_Left = False
                        Player.MainPlayer.Can_Move_Right = True

                    elif Player.MainPlayer.Moving_Right == True:
                        Player.MainPlayer.XPOS -= Player.MainPlayer.Move_Speed
                        Player.MainPlayer.Can_Move_Up = True
                        Player.MainPlayer.Can_Move_Down = True
                        Player.MainPlayer.Can_Move_Left = True
                        Player.MainPlayer.Can_Move_Right = False



                    break #Try to limit over "de-collisioning"
                    
        Video.FPS.Tick()



#Object Trigger Detection - Main Player and Object Layer
def Object_Trigger_Detection_Thread(start, end):
    while True:
        #While checking object area collision, ignore any issues (Incase obj has been removed in another thread)
        try:
            #Check Collision Against Level Object Area
            for i in range(int(start), int(end)):
                if (Maps.Tiled.Level_Objects[i].Collision_Rect.colliderect(\
                Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_rect(\
                size=(Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_width(), Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_height()), \
                center=(Player.MainPlayer.XPOS, Player.MainPlayer.YPOS)))) == True:
                    
                    #Trigger Object
                    Maps.Tiled.Level_Objects[i].Trigger()

                    #Break from loop - faster checking
                    break
        except:
            #Ignore any issues, don't allow crash
            pass

        Video.FPS.Tick()