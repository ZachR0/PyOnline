import thread
import os.path
import os
#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import socket

#PyOnline
import Camera.Manage
import Video.PyGame
import Video.FPS
import Maps.Tiled
import Console.Manage
import Networking.Client
import NPC.Manage

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
NPC_Objects = []


#     ________________________
# ___/  Class Declarations    \_________________________________________________
class NPC_Waypoint:
    #The npc will walk to that X,Y cord, automatically detecting directional
    #movement depending on current x,y pos
    X = None
    Y = None
    
class NPC_Obj:
    Name = None #From SQL
    Health = None #From SQL
    Current_X = None #From SQL
    Current_Y = None #From SQL
    Waypoints_X = [] #From SQL (x0,y0;x1,y1;x2,y2;)
    Waypoints_Y = [] #From SQL (x0,y0;x1,y1;x2,y2;)
    Script_File = None #From SQL
    SpriteSheet_File = None #From SQL
    SpriteMap_File = None #Based on SpiteSheet_File, will default to SpriteMap.sm in that directory
    Sprites = []
    Move_Speed = None #From SQL
    Current_Frame = None
    Max_Frame_Up = None
    Min_Frame_Up = None
    Max_Frame_Down = None
    Min_Frame_Down = None
    Max_Frame_Left = None
    Min_Frame_Left = None
    Max_Frame_Right = None
    Min_Frame_Right = None
    Moving_Right = None
    Moving_Left = None
    Moving_Up = None
    Moving_Down = None
    Can_Move_Up = None
    Can_Move_Down = None
    Can_Move_Left = None
    Can_Move_Right = None

    IS_VALID = None

    def __init__(self, NPCName, NPCHealth, NPCCurrentX, NPCCurrentY, NPCWaypointData,\
        NPCMoveSpeed, NPCScriptFile, NPCSpriteSheetFile, NPCSpriteMapFile):
            #Set Values accordingly
            self.Name = NPCName
            self.Health = int(NPCHealth)
            self.Current_X = int(NPCCurrentX)
            self.Current_Y = int(NPCCurrentY)
            self.Move_Speed = int(NPCMoveSpeed)
            self.Script_File = str("data/scripts/npc/" + str(NPCScriptFile))
            self.SpriteSheet_File = str("data/sprites/npc/" + str(NPCSpriteSheetFile))
            self.SpriteMap_File = str("data/sprites/npc/" + str(NPCSpriteMapFile))
            self.IS_VALID = False


            #Pull waypoint data and place it into Waypoint array accordingly
            ##Format: x0,y0;x1,y1;x2,y2;   NOTE- ; must ALWAYS be at the end!!
            Waypoint_Data = str(NPCWaypointData)
            XData = []
            YData = []
            while len(Waypoint_Data) > 1:
                Sep_Loc = Waypoint_Data.find(";")

                TmpData = Waypoint_Data[0:Sep_Loc]
                Comma_Loc = TmpData.find(",")
                XData.append(TmpData[0:Comma_Loc])
                YData.append(TmpData[Comma_Loc+1:len(TmpData)])

                Waypoint_Data = Waypoint_Data[Sep_Loc+1:len(Waypoint_Data)]
            self.Waypoints_X = XData
            self.Waypoints_Y = YData

            #Make sure Script file exists
            if os.path.exists(str(self.Script_File)) == False:
                print "Error during NPC Init! - Script file location invalid(",\
                    "Name:", self.Name, "ScriptFile:", str(self.Script_File), ")"
            else:
                #So now that the script file exists, lets check the sprite file
                if os.path.exists(str(self.SpriteSheet_File)) == False:
                    print "Error during NPC Init! - SpriteSheet file location invalid(",\
                        "Name:", self.Name, "SpriteFile:", str(self.SpriteSheet_File), ")"
                else:
                    #So now that the script, and sprite files are good, check the sprite map file:
                    if os.path.exists(str(self.SpriteMap_File)) == False:
                        print "Error during NPC Init! - SpriteMap file location invalid(",\
                            "Name:", self.Name, "SpriteMap:", str(self.SpriteMap_File), ")"
                    else:
                        #All local client files for this NPC SHOULD be okay!
                        self.IS_VALID = True

            #Only continue if we are valid!
            if self.IS_VALID == True:
                self.Sprites = []
                self.Max_Frame_Up = 0
                self.Min_Frame_Up = -1
                self.Max_Frame_Down = 0
                self.Min_Frame_Down = -1
                self.Max_Frame_Left = 0
                self.Min_Frame_Left = -1
                self.Max_Frame_Right = 0
                self.Min_Frame_Right = -1
                self.Current_Frame = 0
                self.Moving_Right = False
                self.Moving_Left = False
                self.Moving_Up = False
                self.Moving_Down = False
                self.Can_Move_Up = True
                self.Can_Move_Down = True
                self.Can_Move_Left = True
                self.Can_Move_Right = True

                #Load Sprite
                tmpSprite = pygame.image.load(str(self.SpriteSheet_File))

                #Open sprite map and load data
                FILE = open(str(self.SpriteMap_File), 'r')
                DATA = FILE.readlines()
                FILE.close()

                #Go through each line and pull important data
                count = 0 #Count ignores comments
                for line in DATA:
                    Data_Line = str(line).strip()

                    #Ignore comments
                    if Data_Line[0:1] != "#":
                        #Direction
                        Sep_Loc = Data_Line.find(";")
                        Direction = Data_Line[0:Sep_Loc]
                        Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                        #OffSet X
                        Sep_Loc = Data_Line.find(";")
                        OffX = Data_Line[0:Sep_Loc]
                        Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                        #OffSet Y
                        Sep_Loc = Data_Line.find(";")
                        OffY = Data_Line[0:Sep_Loc]
                        Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                        #Width
                        Sep_Loc = Data_Line.find(";")
                        Width = Data_Line[0:Sep_Loc]
                        Data_Line = Data_Line[Sep_Loc+1:len(Data_Line)]

                        #Height
                        Height = Data_Line[0:Sep_Loc]

                        #Update animation frame information
                        if Direction == "DOWN":
                            #Do we need to set Min_Frame?
                            if self.Min_Frame_Down == -1:
                                self.Min_Frame_Down = count
                            #Update Max_Frame
                            self.Max_Frame_Down += 1
                        if Direction == "UP":
                            #Do we need to set Min_Frame?
                            if self.Min_Frame_Up == -1:
                                self.Min_Frame_Up = count
                            #Update Max_Frame
                            self.Max_Frame_Up += 1

                        if Direction == "LEFT":
                            #Do we need to set Min_Frame?
                            if self.Min_Frame_Left == -1:
                                self.Min_Frame_Left = count
                            #Update Max_Frame
                            self.Max_Frame_Left += 1

                        if Direction == "RIGHT":
                            #Do we need to set Min_Frame?
                            if self.Min_Frame_Right == -1:
                                self.Min_Frame_Right = count
                            #Update Max_Frame
                            self.Max_Frame_Right += 1

                        #Append sprite from sprite sheet
                        self.Sprites.append(tmpSprite.subsurface((int(OffX), int(OffY), int(Width), int(Height))))

                        #Increase loop count
                        count += 1

                #Fix Max_Fame Value
                self.Max_Frame_Down += self.Min_Frame_Down
                self.Max_Frame_Up += self.Min_Frame_Up
                self.Max_Frame_Left += self.Min_Frame_Left
                self.Max_Frame_Right += self.Min_Frame_Right

                #Take Max_Frame down one to respect the "starting from zero" system
                self.Max_Frame_Down -= 1
                self.Max_Frame_Up -= 1
                self.Max_Frame_Left -= 1
                self.Max_Frame_Right -= 1


    #Renders NPC
    def Render(self):
        Video.PyGame.Screen.blit(self.Sprites[int(self.Current_Frame)], (int(self.Current_X)-int(Camera.Manage.CamX), int(self.Current_Y)-int(Camera.Manage.CamY)))


    #Handles NPC Sprite Animation
    def Animate(self):
        #Moving Right
        if self.Moving_Right == True:
            #Keep within Frames Min_Frame-Max_Frame
            if self.Current_Frame >= self.Min_Frame_Right and self.Current_Frame < self.Max_Frame_Right:
                self.Current_Frame += 1
            elif self.Current_Frame > self.Max_Frame_Right:
                self.Current_Frame -= 1
            else:
                self.Current_Frame = self.Min_Frame_Right

        #Moving Left
        if self.Moving_Left == True:
            #Keep within Frames Min_Frame-Max_Frame
            if self.Current_Frame >= self.Min_Frame_Left and self.Current_Frame < self.Max_Frame_Left:
                self.Current_Frame += 1
            elif self.Current_Frame > self.Max_Frame_Left:
                self.Current_Frame -= 1
            else:
                self.Current_Frame = self.Min_Frame_Left

        #Moving Down
        if self.Moving_Down == True:
            #Keep within Frames Min_Frame-Max_Frame
            if self.Current_Frame >= self.Min_Frame_Down and self.Current_Frame < self.Max_Frame_Down:
                self.Current_Frame += 1
            elif self.Current_Frame > self.Max_Frame_Down:
                self.Current_Frame -= 1
            else:
                self.Current_Frame = self.Min_Frame_Down

        #Moving Up
        if self.Moving_Up == True:
            #Keep within Frames Min_Frame-Max_Frame
            if self.Current_Frame >= self.Min_Frame_Up and self.Current_Frame < self.Max_Frame_Up:
                self.Current_Frame += 1
            elif self.Current_Frame > self.Max_Frame_Up:
                self.Current_Frame -= 1
            else:
                self.Current_Frame = self.Min_Frame_Up
        
    #Handles NPC Movement Waypoints
    def Move(self):
        while True:
            #Go through each way point set
            count = 0
            for wayX in self.Waypoints_X:
                #Get corrasponding waypoint Y
                wayY = self.Waypoints_Y[count]
                
                #Move NPC until XCord matches wayX
                if self.Current_X < int(wayX): #Move right?
                    #Move right however long is needed
                    while self.Current_X <= int(wayX):
                        #Update Animation Direction
                        self.Moving_Right = True
                        self.Moving_Left = False
                        self.Moving_Move_Up = False
                        self.Moving_Down = False
                        
                        #Move
                        self.Current_X += self.Move_Speed
                        
                        #Maintain FPS reg
                        Video.FPS.Tick()
                    
                elif self.Current_X > int(wayX): #Move left?
                    #Move left however long is needed
                    while self.Current_X >= int(wayX):
                        #Update Animation Direction
                        self.Moving_Right = False
                        self.Moving_Left = True
                        self.Moving_Move_Up = False
                        self.Moving_Down = False
                        
                        #Move
                        self.Current_X -= self.Move_Speed
                        
                        #Maintain FPS reg
                        Video.FPS.Tick()
                
                #Update count
                count += 1
            
            


#     ________________________
# ___/ Function Declarations  \_________________________________________________

#Loads NPC Data
def LoadNPCData():
    global NPC_Objects
    
    #Go through each NPC object in NPC_DATA and pull information
    for npc in Networking.Client.NPC_DATA:
        data = str(npc)
        
        #Get NPC data
        Name = data[int(str(data).find("-Name:")) + 6 : int(str(data).find("-Health:"))]
        Health = data[int(str(data).find("-Health:")) + 8 : int(str(data).find("-CurrentX:"))]
        CurrentX = data[int(str(data).find("-CurrentX:")) + 10 : int(str(data).find("-CurrentY:"))]
        CurrentY = data[int(str(data).find("-CurrentY:")) + 10 : int(str(data).find("-Waypoints:"))]
        Waypoints = data[int(str(data).find("-Waypoints:")) + 11 : int(str(data).find("-MoveSpeed:"))]
        MoveSpeed = data[int(str(data).find("-MoveSpeed:")) + 11 : int(str(data).find("-ScriptFile:"))]
        ScriptFile = data[int(str(data).find("-ScriptFile:")) + 12 : int(str(data).find("-SpriteSheet:"))]
        SpriteSheet = data[int(str(data).find("-SpriteSheet:")) + 13 : int(str(data).find("-SpriteMap:"))]
        SpriteMap = data[int(str(data).find("-SpriteMap:")) + 11 : len(data)]
        print Name, Health, CurrentX, CurrentY, Waypoints, MoveSpeed, ScriptFile, SpriteSheet, SpriteMap
        
        #Add NPC to NPC_Objects
        tmpNPC = NPC.Manage.NPC_Obj(Name, Health, CurrentX, CurrentY, Waypoints, MoveSpeed, ScriptFile, SpriteSheet, SpriteMap)
        tmpNPC.Moving_Right = True #Set Default movement - Needed?
        
        NPC_Objects.append(tmpNPC)
        
    #Start NPC movement threads
    for npc in NPC_Objects:
        thread.start_new_thread(npc.Move, ())
        
#Renders NPCs
def RenderNPC():
    global NPC_Objects
    
    #Go through each NPC and render
    for npc in NPC_Objects:
        npc.Render()
        
#Animates NPCs
def AnimateNPC():
    global NPC_Objects
    
    #Go through each NPC and animate
    for npc in NPC_Objects:
        npc.Animate()
    
    
    
    