#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline
import Maps.tiledtmxloader
import Player.MainPlayer
import Objects.Sign
import Objects.House_Exit
import Objects.House_Entrance
import Objects.Zone

#PyGame
import pygame
from pygame.locals import *

#     ________________________
# ___/ Variable Declarations  \_________________________________________________
Current_Level = None
Ground_ID = None
NonCollision_Primary_ID = None
NonCollision_Secondary_ID = None
Collision_ID = None
Collision_Layer = None
Level_Objects = []

ImageLoader = None
Renderer = None
Layer_Range = None


#     ________________________
# ___/  Class Declarations    \_________________________________________________
#Allows us to keep track of a tile's x,y pos
class Tile:
    Tile_Surface = None
    Tile_X = None
    Tile_Y = None

    def __init__(self, TileSurface, TileX, TileY):
        self.Tile_Surface = TileSurface
        self.Tile_X = TileX
        self.Tile_Y = TileY

class Tile_Rect:
    Rect = None
    def __init__(self, TileRect):
        self.Rect = TileRect

#Allows us to keep track of layer data - mainly tiles
class Layer:
    Tiled_Layer = None
    Tiles = []

    def __init__(self, Layer):
        self.Tiled_Layer = Layer
        self.Tiles = []

#Map Objects
class Map_Object:
    ID = None
    XPOS = None
    YPOS = None
    Width = None
    Height = None
    Name = None
    Type = None
    Properties = None
    Collision_Rect = None
    Being_Triggered = None

    def __init__(self, ObjID, ObjName, ObjType, ObjX, ObjY, ObjWidth, ObjHeight, ObjProperties):
        self.ID = ObjID
        self.Name = ObjName
        self.Type = ObjType
        self.XPOS = ObjX
        self.YPOS = ObjY
        self.Width = ObjWidth
        self.Height = ObjHeight
        self.Properties = ObjProperties
        self.Being_Triggered = False

        #Setup Collision Rect
        self.Collision_Rect = pygame.Rect(self.XPOS, self.YPOS, self.Width, self.Height)
        #self.Collision_Rect.center = (self.XPOS, self.YPOS) Causes issues with object area, offsets it way too much

    #Occurs when Player is within Object area
    def Trigger(self):
        #Make sure we are not already triggering
        if self.Being_Triggered == False:
            #Depending on Object Type, Do Different Actions
            if self.Type == "Sign":
                #Make sure the correct object properties are defined
                if "Message" in self.Properties.keys():
                    #Call Trigger Function - Passing Sign Message
                    #print "[Map Object Triggered]"
                    Objects.Sign.Trigger(self.ID, self.Properties["Message"])

                    #Update Trigger Value
                    self.Being_Triggered = True
                else:
                    print "[Object]: Sign Objects REQUIRE a \"Message\" Property Value!"

                    #Update Trigger Value
                    self.Being_Triggered = True
            elif self.Type == "Zone":
                #Make sure the correct object properties are defined
                if "Zone Name" in self.Properties.keys():
                    #Call Trigger Function
                    Objects.Zone.Trigger(self.ID, self.Properties["Zone Name"])

                    #Update Trigger Value
                    self.Being_Triggered = True
                else:
                    print "[Object]: Zone Objects REQUIRE a \"Zone Name\" Property Value!"

            elif self.Type == "House_Entrance":
                #Make sure the correct object propterties are defined
                if "Direction" in self.Properties.keys() and "Port Location" in self.Properties.keys():
                    #Call Trigger Function
                    Objects.House_Entrance.Trigger(self.ID, self.Properties["Direction"], self.Properties["Port Direction"], self.Properties["Port Location"])

                    #Update Trigger Value
                    self.Being_Triggered = True
                else:
                    print "[Object]: House_Entrance Objects REQUIRE a \"Direction\" and a \"Port Location\" Property Value!"
            elif self.Type == "House_Exit":
                #Make sure the correct object propterties are defined
                if "Direction" in self.Properties.keys() and "Port Direction" in self.Properties.keys() and "Port Location" in self.Properties.keys():
                    #Call Trigger Function
                    Objects.House_Exit.Trigger(self.ID, self.Properties["Direction"], self.Properties["Port Direction"], self.Properties["Port Location"])

                    #Update Trigger Value
                    self.Being_Triggered = True
                else:
                    print "[Object]: House_Exit Objects REQUIRE a \"Direction\" and a \"Port Location\" Property Value!"

            #Anyother Object Type (None)
            else:
                #Do nothing
                pass

    #Occurs when Player leaves Object area
    #Called in Events.Handle when player moves (DeTriggers all Objects)
    def DeTrigger(self):
        #Depending on Object Type, Do Different Actions
        if self.Type == "Sign":
            #Call DeTrigger Function
            Objects.Sign.DeTrigger()
        elif self.Type == "Zone":
            #Call DeTrigger Functions
            Objects.Zone.DeTrigger()
        #Anyother Object Type (None)
        else:
            #Do nothing
            pass

        #Update Trigger Value
        self.Being_Triggered = False


#     ________________________
# ___/ Function Declarations  \_________________________________________________
#Loads level data from TMX
def LoadLevel(Level_File):
    #Get Global Variables
    global Current_Level
    global Ground_ID
    global NonCollision_Primary_ID
    global NonCollision_Secondary_ID
    global Collision_ID
    global Collision_Layer
    global Level_Objects
    global ImageLoader
    global Renderer
    global Layer_Range

    #Set Level File
    Current_Level = Maps.tiledtmxloader.TileMapParser().parse_decode(Level_File)

    #Load Data
    ImageLoader = Maps.tiledtmxloader.ImageLoaderPygame()
    Current_Level.load(ImageLoader)

    Renderer = Maps.tiledtmxloader.RendererPygame(Current_Level)
    Layer_Range = range(len(Current_Level.layers))

    #Get important layers
    layer_count = 0
    for layer in Current_Level.layers[:]:
        if layer.name == "Ground":
            Ground_ID = layer_count
        elif layer.name == "Primary Non-Collision":
            NonCollision_Primary_ID = layer_count
        elif layer.name == "Secondary Non-Collision":
            NonCollision_Secondary_ID = layer_count
        elif layer.name == "Collision":
            Collision_ID = layer_count
            Collision_Layer = Layer(layer)

            idx = 0
            #Loop through all tiles
            for ypos in xrange(0, Collision_Layer.Tiled_Layer.height):
                for xpos in xrange(0, Collision_Layer.Tiled_Layer.width):
                    #Add offset in number of tiles
                    x = (xpos + Collision_Layer.Tiled_Layer.x) * Current_Level.tilewidth
                    y = (ypos + Collision_Layer.Tiled_Layer.y) * Current_Level.tileheight

                    #Get the gid at this position
                    img_idx = Collision_Layer.Tiled_Layer.content2D[xpos][ypos]

                    #Update the current tile x across count
                    idx += 1

                    #Make sure we have data
                    if img_idx:
                        #Get the actual image and its offset
                        offx, offy, screen_img = Current_Level.indexed_tiles[img_idx]

                        if screen_img.get_alpha():
                            screen_img = screen_img.convert_alpha()
                        else:
                            screen_img = screen_img.convert()
                            if Collision_Layer.Tiled_Layer.opacity > -1:
                                screen_img.set_alpha(None)
                                alpha_value = int(255. * float(Collision_Layer.Tiled_Layer.opacity))
                                screen_img.set_alpha(alpha_value)
                        screen_img = screen_img.convert_alpha()

                        #Add Collision Tiles To List
                        #TODO: Instead of keeping the tile images in memory, just use the Rect info
                        Collision_Layer.Tiles.append(Tile(screen_img, x + offx, y + offy)) #Keeps record of tile x,y

        layer_count += 1

    #Load Map Objects
    for Object_Group in Current_Level.object_groups:
        for Object in Object_Group.objects:
            #Add each map object to our map object list
            Level_Objects.append(Map_Object((len(Level_Objects) + 1), Object.name, Object.type, Object.x, Object.y, Object.width, Object.height, Object.properties))

            #Check if spawn point was defined
            if Object.type == "Spawn_Point":
                #Set Player X,Y to that of the defined spawn point
                #print "- Spawn_Point detected: (", Object.x, ",", Object.y, ")"
                if Player.MainPlayer.XPOS == None and Player.MainPlayer.YPOS == None:
                    Player.MainPlayer.XPOS = Object.x
                    Player.MainPlayer.YPOS = Object.y