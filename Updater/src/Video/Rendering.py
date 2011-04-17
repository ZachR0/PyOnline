#     _________________
# ___/ Module Imports  \________________________________________________________
#System
import os
import os.path

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Function Declarations  \_________________________________________________
#Loads image from file, returns data
def LoadImg(File):
    Tmp_Image = None

    #Check if File exists
    if os.path.exists(File) == True:
        Tmp_Image = pygame.image.load(File)
        return Tmp_Image
    else:
        #Output error message
        print "[Video Rendering.py]: LoadImg failed! - \"", str(File),\
                "\" not found!"
        return None