import Maps.Tiled
#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline
import Player.MainPlayer
import Video.PyGame
import Dialog.Popup
import Dialog.Global
import Camera.Manage

#PyGame
import pygame
from pygame.locals import *

def Trigger(ID, Message):
    #Make sure the player is facing the sign
    if Player.MainPlayer.Moving_Up == True:
        #Display Sign Message
        #print "[Object Sign Trigger]: ", Message

        #Display Sign Message In Dialog
        Dialog.Global.CURRENT_DIALOG_SURFACE = Dialog.Popup.Display(str(Message))


def DeTrigger():
    #Reset Dialog Display
    Dialog.Global.CURRENT_DIALOG_SURFACE = None
