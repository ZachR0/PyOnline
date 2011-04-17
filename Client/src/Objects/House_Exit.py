#     _________________
# ___/ Module Imports  \________________________________________________________
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
# ___/ Function Declaration  \__________________________________________________
def Trigger(ID, Direction, Port_Direction, Port_Location):
    #Make sure player is facing correct direction
    if (Direction == "Up" and Player.MainPlayer.Moving_Up == True) or \
        (Direction == "Down" and Player.MainPlayer.Moving_Down == True) or \
        (Direction == "Left" and Player.MainPlayer.Moving_Left == True) or \
        (Direction == "Right" and Player.MainPlayer.Moving_Right == True):

            #Get the X,Y cord to port the player to
            Port_X = None
            Port_Y = None

            #Go through each map object
            for i in range(0, len(Maps.Tiled.Level_Objects)):
                #Get info from the correct object
                if Maps.Tiled.Level_Objects[i].Name == Port_Location:
                    if Direction == "Up":
                        Port_X = Maps.Tiled.Level_Objects[i].XPOS + (Maps.Tiled.Level_Objects[i].Width / 2)
                        Port_Y = Maps.Tiled.Level_Objects[i].YPOS - ((Maps.Tiled.Level_Objects[i].Height / 2) + \
                                                                        Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_height())
                        #Port_X = Maps.Tiled.Level_Objects[i].XPOS + (Maps.Tiled.Level_Objects[i].Width / 2)
                        #Port_Y = Maps.Tiled.Level_Objects[i].YPOS - (Maps.Tiled.Level_Objects[i].Height / 2)
                    elif Direction == "Down":
                        Port_X = Maps.Tiled.Level_Objects[i].XPOS + (Maps.Tiled.Level_Objects[i].Width / 2)
                        Port_Y = Maps.Tiled.Level_Objects[i].YPOS + ((Maps.Tiled.Level_Objects[i].Height / 2) + \
                                                                        Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_height())
                        #Port_X = Maps.Tiled.Level_Objects[i].XPOS + (Maps.Tiled.Level_Objects[i].Width / 2)
                        #Port_Y = Maps.Tiled.Level_Objects[i].YPOS + (Maps.Tiled.Level_Objects[i].Height / 2)
                    elif Direction == "Left":
                        Port_X = Maps.Tiled.Level_Objects[i].XPOS + ((Maps.Tiled.Level_Objects[i].Width / 2) + \
                                                                        Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_width())
                        Port_Y = Maps.Tiled.Level_Objects[i].YPOS + (Maps.Tiled.Level_Objects[i].Height / 2)
                        #Port_X = Maps.Tiled.Level_Objects[i].XPOS + (Maps.Tiled.Level_Objects[i].Width / 2)
                        #Port_Y = Maps.Tiled.Level_Objects[i].YPOS + (Maps.Tiled.Level_Objects[i].Height / 2)
                    elif Direction == "Right":
                        Port_X = Maps.Tiled.Level_Objects[i].XPOS - ((Maps.Tiled.Level_Objects[i].Width / 2) + \
                                                                        Player.MainPlayer.Sprites[Player.MainPlayer.Current_Frame].get_width())
                        Port_Y = Maps.Tiled.Level_Objects[i].YPOS + (Maps.Tiled.Level_Objects[i].Height / 2)
                        #Port_X = Maps.Tiled.Level_Objects[i].XPOS - (Maps.Tiled.Level_Objects[i].Width / 2)
                        #Port_Y = Maps.Tiled.Level_Objects[i].YPOS + (Maps.Tiled.Level_Objects[i].Height / 2)
                    break

            #Update player x,y
            Player.MainPlayer.XPOS = Port_X
            Player.MainPlayer.YPOS = Port_Y

            #Reset player direction
            if Port_Direction == "Up":
                Player.MainPlayer.Moving_Up == True
                Player.MainPlayer.Moving_Down == False
                Player.MainPlayer.Moving_Left == False
                Player.MainPlayer.Moving_Right == False

                Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Up

            elif Port_Direction == "Down":
                Player.MainPlayer.Moving_Up == False
                Player.MainPlayer.Moving_Down == True
                Player.MainPlayer.Moving_Left == False
                Player.MainPlayer.Moving_Right == False

                Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Down

            elif Port_Direction == "Left":
                Player.MainPlayer.Moving_Up == False
                Player.MainPlayer.Moving_Down == False
                Player.MainPlayer.Moving_Left == True
                Player.MainPlayer.Moving_Right == False

                Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Left

            elif Port_Direction == "Right":
                Player.MainPlayer.Moving_Up == False
                Player.MainPlayer.Moving_Down == False
                Player.MainPlayer.Moving_Left == False
                Player.MainPlayer.Moving_Right == True

                Player.MainPlayer.Current_Frame = Player.MainPlayer.Min_Frame_Right



def DeTrigger():
    #Do nothing
    pass
