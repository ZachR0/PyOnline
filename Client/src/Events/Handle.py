import time
import Networking.Client
import Console.Manage
#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import sys

#PyOnline
import Maps.Tiled
import Video.PyGame
import Player.MainPlayer

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Function Declarations  \_________________________________________________
#Goes through each event in queue, and handles accordingly

def EventLoop():
    #Update KeyState
    Keystate = pygame.key.get_pressed()

    #Used to keep track of how many times a directional key is held down (for player movement)
    Direction_Count = 0

    #Direction_Count Management
    if Keystate[pygame.K_w] == True or Keystate[pygame.K_s] == True or \
       Keystate[pygame.K_a] == True or Keystate[pygame.K_d] == True:
        Direction_Count += 1
    else:
        Direction_Count = 0

    #Go through each event
    for event in pygame.event.get():
        #Important Events
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                #Disconnect from game server
                Networking.Client.DisConnect()
                
                #Stop PyGame
                pygame.quit()

                #Exit Completly
                sys.exit(0)
            if event.key == K_BACKSLASH:
                #Toggle Fullscreen
                if Video.PyGame.Screen_Fullscreen == False:
                    Video.PyGame.SetVideo(800, 640, True)
                else:
                    Video.PyGame.SetVideo(800, 640, False)
                    
            if event.key == K_BACKQUOTE:
                #Focus/Unfocus console
                if Console.Manage.Console_Focused != True:
                    #Focus
                    Console.Manage.Console_Focused = True;
                    
                    #Display a screen message
                    Console.Manage.ScreenWrite("Console Activated!")
                
                    #Change key input speed(good speed for typing)
                    pygame.key.set_repeat(200,200)
                else:
                    #UnFocus
                    Console.Manage.Console_Focused = False;
                    
                    #Display a screen message
                    Console.Manage.ScreenWrite("Console NOT Activated!")
                
                    #Change key input speed(good speed for normal input)
                    pygame.key.set_repeat(1,1)
                
                #Stop event loop
                break;

        #Check if console is focused; If so, allow it to handle events
        if Console.Manage.Console_Focused == True:
            Console.Manage.EventHandle(event)
        else:
            #Keydown Events
            if event.type == KEYDOWN:

                #Player Movement Down
                if event.key == pygame.K_s and Player.MainPlayer.Can_Move_Down == True:
                    Player.MainPlayer.Moving_Up = False
                    Player.MainPlayer.Moving_Down = True
                    Player.MainPlayer.Moving_Right = False
                    Player.MainPlayer.Moving_Left = False
                    if Direction_Count == 0:
                        Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Down
                    Player.MainPlayer.YPOS += Player.MainPlayer.Move_Speed

                    #Networking.Client.SendData(str("mov_plr:" + str(Player.MainPlayer.XPOS)+ ":" + str(Player.MainPlayer.YPOS) + ":") + str(Player.MainPlayer.Current_Frame) + ":")

                    #While checking object area collision, ignore any issues (Incase obj has been removed in another thread)
                    try:
                        #DeTrigger ALL Level Objects on player movement
                        for i in range(0, len(Maps.Tiled.Level_Objects)):
                            Maps.Tiled.Level_Objects[i].DeTrigger()
                    except:
                        #Do nothing
                        pass

                #Player Movement Up
                if event.key == pygame.K_w and Player.MainPlayer.Can_Move_Up == True:
                    Player.MainPlayer.Moving_Up = True
                    Player.MainPlayer.Moving_Down = False
                    Player.MainPlayer.Moving_Right = False
                    Player.MainPlayer.Moving_Left = False
                    if Direction_Count == 0:
                        Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Up
                    Player.MainPlayer.YPOS -= Player.MainPlayer.Move_Speed

                    #Networking.Client.SendData(str("mov_plr:" + str(Player.MainPlayer.XPOS)+ ":" + str(Player.MainPlayer.YPOS) + ":") + str(Player.MainPlayer.Current_Frame) + ":")

                    #While checking object area collision, ignore any issues (Incase obj has been removed in another thread)
                    try:
                        #DeTrigger ALL Level Objects on player movement
                        for i in range(0, len(Maps.Tiled.Level_Objects)):
                            Maps.Tiled.Level_Objects[i].DeTrigger()
                    except:
                        #Do nothing
                        pass

                #Player Movement Left
                if event.key == pygame.K_a and Player.MainPlayer.Can_Move_Left == True:
                    Player.MainPlayer.Moving_Up = False
                    Player.MainPlayer.Moving_Down = False
                    Player.MainPlayer.Moving_Right = False
                    Player.MainPlayer.Moving_Left = True
                    if Direction_Count == 0:
                        Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Left
                    Player.MainPlayer.XPOS -= Player.MainPlayer.Move_Speed

                    #Networking.Client.SendData(str("mov_plr:" + str(Player.MainPlayer.XPOS)+ ":" + str(Player.MainPlayer.YPOS) + ":") + str(Player.MainPlayer.Current_Frame) + ":")

                    #While checking object area collision, ignore any issues (Incase obj has been removed in another thread)
                    try:
                        #DeTrigger ALL Level Objects on player movement
                        for i in range(0, len(Maps.Tiled.Level_Objects)):
                            Maps.Tiled.Level_Objects[i].DeTrigger()
                    except:
                        #Do nothing
                        pass

                #Player Movement Right
                if event.key == pygame.K_d and Player.MainPlayer.Can_Move_Right == True:
                    Player.MainPlayer.Moving_Up = False
                    Player.MainPlayer.Moving_Down = False
                    Player.MainPlayer.Moving_Right = True
                    Player.MainPlayer.Moving_Left = False
                    if Direction_Count == 0:
                        Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Right
                    Player.MainPlayer.XPOS += Player.MainPlayer.Move_Speed

                    #Networking.Client.SendData(str("mov_plr:" + str(Player.MainPlayer.XPOS)+ ":" + str(Player.MainPlayer.YPOS) + ":") + str(Player.MainPlayer.Current_Frame) + ":")

                    #While checking object area collision, ignore any issues (Incase obj has been removed in another thread)
                    try:
                        #DeTrigger ALL Level Objects on player movement
                        for i in range(0, len(Maps.Tiled.Level_Objects)):
                            Maps.Tiled.Level_Objects[i].DeTrigger()
                    except:
                        #Do nothing
                        pass

            if event.type == KEYUP:
                if event.key == pygame.K_s:
                    Player.MainPlayer.Moving_Down = False

                    Player.MainPlayer.Can_Move_Up = True
                    Player.MainPlayer.Can_Move_Down = True
                    Player.MainPlayer.Can_Move_Left = True
                    Player.MainPlayer.Can_Move_Right = True

                if event.key == pygame.K_w:
                    Player.MainPlayer.Moving_Up = False

                    Player.MainPlayer.Can_Move_Up = True
                    Player.MainPlayer.Can_Move_Down = True
                    Player.MainPlayer.Can_Move_Left = True
                    Player.MainPlayer.Can_Move_Right = True


                if event.key == pygame.K_a:
                    Player.MainPlayer.Moving_Left = False

                    Player.MainPlayer.Can_Move_Up = True
                    Player.MainPlayer.Can_Move_Down = True
                    Player.MainPlayer.Can_Move_Left = True
                    Player.MainPlayer.Can_Move_Right = True

                    
                if event.key == pygame.K_d:
                    Player.MainPlayer.Moving_Right = False
                    Player.MainPlayer.Can_Move_Up = True
                    Player.MainPlayer.Can_Move_Down = True
                    Player.MainPlayer.Can_Move_Left = True
                    Player.MainPlayer.Can_Move_Right = True