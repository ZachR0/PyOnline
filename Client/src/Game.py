#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import sys
import os.path
import gc
import thread

#Simple PyGame GUI
import SPG.gui
import SPG.defaultStyle

#PyOnline
import Video
import Video.PyGame
import Video.FPS
import Video.Rendering
import Events.Handle
import Maps.Tiled
import Collision.Manage
import Camera.Manage
import Player.MainPlayer
import Dialog.Popup
import Dialog.Global
import Objects.Zone
import Console.Manage
import Networking.Client
import Maps.Tiled
import NPC.Manage

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
SERVER_MODE = False
LEVEL_TO_LOAD = "data/maps/World/World.tmx"

#     ___________
# ___/ Game Code \______________________________________________________________
def Run():
    #Font for debug loading stuff
    Debug_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 10)

    #Was the user fullscreen during login?
    FS = Video.PyGame.Screen_Fullscreen

    #Init Video
    Video.PyGame.InitVideo()

    #Setup Video
    Video.PyGame.SetVideo(800, 640, FS)

    #Display Loading Information
    InfoSurf = Debug_Font.render("Starting to load game content...", False, (255,255,255))
    Video.PyGame.Screen.blit(InfoSurf, (0,0)) #Render Text
    pygame.display.flip() #Update Display

    #Init FPS System
    Video.FPS.Init()

    #Update Window Caption To Current Ver
    pygame.display.set_caption(str("PyOnline - " + str(Networking.Client.CLIENT_VER)))

    #Only continue if a connection to the game server has been made
    if Networking.Client.isConnected:
        #Display Loading Information
        InfoSurf = Debug_Font.render("Loading World Map (This may take some time)...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,15*1)) #Render Text
        pygame.display.flip() #Update Display

        #Load Map Data
        if os.path.exists(str(LEVEL_TO_LOAD)):
            Maps.Tiled.LoadLevel(str(LEVEL_TO_LOAD))
        else:
            print "Requested level file \"", str(LEVEL_TO_LOAD), "\" cannot be found!"
            pygame.quit()
            sys.exit(0)

        #Display Loading Information
        InfoSurf = Debug_Font.render("Setting up game console...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,15*2)) #Render Text
        pygame.display.flip() #Update Display

        #Init Input Console / Chat Window
        Console.Manage.Init()

        #Display Loading Information
        InfoSurf = Debug_Font.render("Setting up local player...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,15*3)) #Render Text
        pygame.display.flip() #Update Display

        #Init Player
        Player.MainPlayer.Init()
        
        #Display Loading Information
        InfoSurf = Debug_Font.render("Loading NPC Data...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,15*4)) #Render Text
        pygame.display.flip() #Update Display

        #Load NPC Data
        NPC.Manage.LoadNPCData()

        #Start Player Movement Monitor Thread
        thread.start_new_thread(Player.MainPlayer.Movement_Monitor_Thread, ())

        #Display Loading Information
        InfoSurf = Debug_Font.render("Starting server communication loop...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,15*5)) #Render Text
        pygame.display.flip() #Update Display

        #Start Connection Loop Thread
        thread.start_new_thread(Networking.Client.Connection_Loop, ())

        #Display Loading Information
        InfoSurf = Debug_Font.render("Enabling collision manager...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,1565)) #Render Text
        pygame.display.flip() #Update Display

        #Startup the Collision Manager
        Collision.Manage.Setup()

        #Display Loading Information
        InfoSurf = Debug_Font.render("Writing server messages to game console...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,15*7)) #Render Text
        pygame.display.flip() #Update Display

        #Display Server Messages
        color = 0
        for i in range(0, int(len(Networking.Client.SERVER_MESSAGES))):
            #Do not write a \n to the first and last messages
            if i > 0 and i < int(len(Networking.Client.SERVER_MESSAGES)):
                Console.Manage.Write(str(" "), (0,0,0))

            #Alternate message color per line
            if color == 0:
                Console.Manage.Write(str(Networking.Client.SERVER_MESSAGES[i]), (255,134,0))
                color = 1
            elif color == 1:
                Console.Manage.Write(str(Networking.Client.SERVER_MESSAGES[i]), (151,214,216))
                color = 0

        #Test NPC
        #Test = NPC.Manage.NPC_Obj("NPC Name", "100", "4430", "4389", "4700,4389;4630;4389;",\
        #   "4", "test_npc.lua", "test_npc/TestNPC.png", "test_npc/SpriteMap.sm")
        #Test.Moving_Right = True

        #Display Loading Information
        InfoSurf = Debug_Font.render("Entering Game Loop...", False, (255,255,255))
        Video.PyGame.Screen.blit(InfoSurf, (0,15*7)) #Render Text
        pygame.display.flip() #Update Display

        #Game Loop
        while True:
            #Event Handling
            Events.Handle.EventLoop()

            #Update Camera (Keep centered around player)
            Camera.Manage.CamX = Player.MainPlayer.XPOS - (Video.PyGame.Screen_Width / 2)
            Camera.Manage.CamY = Player.MainPlayer.YPOS - (Video.PyGame.Screen_Height / 2)

            #Update Player Animation Data
            Player.MainPlayer.Animate()

            #Test NPC Animation
            #Test.Animate()
            
            #Animate NPCs
            NPC.Manage.AnimateNPC()

            #Test NPC Movement
           # if Test.Moving_Right:
           #     if Test.Current_X < 4730:
           #         Test.Current_X += Test.Move_Speed
           #         Test.Can_Move_Right = True
           #         Test.Moving_Right = True
           #         Test.Can_Move_Down = False
           #         Test.Moving_Down = False
           #         Test.Can_Move_Left = False
           #         Test.Moving_Left = False
           #         Test.Can_Move_Up = False
           #         Test.Moving_Up = False
           #     else:
           #         Test.Can_Move_Right = False
           #         Test.Moving_Right = False
           #         Test.Can_Move_Down = True
           #         Test.Moving_Down = True
           #         Test.Can_Move_Left = False
           #         Test.Moving_Left = False
           #         Test.Can_Move_Up = False
           #         Test.Moving_Up = False

           # elif Test.Moving_Down:
           #     if Test.Current_Y < 4589:
           #         Test.Current_Y += Test.Move_Speed
           #         Test.Can_Move_Right = False
           #         Test.Moving_Right = False
           #         Test.Can_Move_Down = True
           #         Test.Moving_Down = True
           #         Test.Can_Move_Left = False
           #         Test.Moving_Left = False
           #         Test.Can_Move_Up = False
           #         Test.Moving_Up = False
           #     else:
           #         Test.Can_Move_Right = False
           #         Test.Moving_Right = False
           #         Test.Can_Move_Down = False
           #         Test.Moving_Down = False
           #         Test.Can_Move_Left = True
           #         Test.Moving_Left = True
           #         Test.Can_Move_Up = False
           #         Test.Moving_Up = False

           # elif Test.Moving_Left:
           #     if Test.Current_X > 4430:
           #         Test.Current_X -= Test.Move_Speed
           #         Test.Can_Move_Right = False
           #         Test.Moving_Right = False
           #         Test.Can_Move_Down = False
           #         Test.Moving_Down = False
           #         Test.Can_Move_Left = True
           #         Test.Moving_Left = True
           #         Test.Can_Move_Up = False
           #         Test.Moving_Up = False
           #     else:
           #         Test.Can_Move_Right = False
           #         Test.Moving_Right = False
           #         Test.Can_Move_Down = False
           #         Test.Moving_Down = False
           #         Test.Can_Move_Left = False
           #         Test.Moving_Left = False
           #         Test.Can_Move_Up = True
           #         Test.Moving_Up = True

           # elif Test.Moving_Up:
           #     if Test.Current_Y > 4389:
           #         Test.Current_Y -= Test.Move_Speed
           #         Test.Can_Move_Right = False
           #         Test.Moving_Right = False
           #         Test.Can_Move_Down = False
           #         Test.Moving_Down = False
           #         Test.Can_Move_Left = False
           #         Test.Moving_Left = False
           #         Test.Can_Move_Up = True
           #         Test.Moving_Up = True
           #     else:
           #         Test.Can_Move_Right = True
           #         Test.Moving_Right = True
           #         Test.Can_Move_Down = False
           #         Test.Moving_Down = False
           #         Test.Can_Move_Left = False
           #         Test.Moving_Left = False
           #         Test.Can_Move_Up = False
           #         Test.Moving_Up = False


            #Update Map/Level Camera (To Match Camera.Manage system)
            Maps.Tiled.Renderer.set_camera_position(Camera.Manage.CamX , Camera.Manage.CamY , Video.PyGame.Screen_Width, Video.PyGame.Screen_Height)

            #Update Console Data
            Console.Manage.Update()

            #Clear screen before rendering
            Video.PyGame.Screen.fill((0,0,0))

            #Render Map/Level Layer for layer
            for id in Maps.Tiled.Layer_Range:
                Maps.Tiled.Renderer.render_layer(Video.PyGame.Screen, id, Video.PyGame.Screen.blit)

                #Make sure to render the player above the ground layer
                if id == Maps.Tiled.Ground_ID:
                    #Render Player
                    Player.MainPlayer.Render()

                    #Render any players
                    for player in Networking.Client.OTHER_PLAYERS:
                        Networking.Client.OTHER_PLAYERS[str(player)].Render()

                    #Test NPC Render
                    #Test.Render()
                    
                    #Render NPCs
                    NPC.Manage.RenderNPC()

            #Render Current Dialog (If There is one)
            if Dialog.Global.CURRENT_DIALOG_SURFACE != None:
                Video.PyGame.Screen.blit(Dialog.Global.CURRENT_DIALOG_SURFACE, ((Player.MainPlayer.XPOS - Camera.Manage.CamX)/2, (Player.MainPlayer.YPOS - Camera.Manage.CamY) + 50))

            #Render Zone Name (If needed)
            if Objects.Zone.Zone_Name_Surface != None:
                Video.PyGame.Screen.blit(Objects.Zone.Zone_Name_Surface, (Video.PyGame.Screen_Width / 2, Video.PyGame.Screen_Height / 3))
                
            #Render Screen Message (If needed)
            if Console.Manage.Screen_Message != None:
                Video.PyGame.Screen.blit(Console.Manage.Screen_Message, (Video.PyGame.Screen_Width / 2, Video.PyGame.Screen_Height / 3))

            #Render Game Console
            Console.Manage.Render()

            #Update Display
            pygame.display.flip()

            #FPS Regulation
            Video.FPS.Tick()

            #Python Garbage Collection
            gc.collect()