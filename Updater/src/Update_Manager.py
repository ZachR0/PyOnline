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

#PyOnline
import Video.PyGame
import Video.FPS

#PyGame
import pygame
from pygame.locals import *

from xml.dom import minidom
import urllib2

Update_Tmp_Path = "data/update_tmp"
Root_Path_From_Update_Tmp = "../../"
Clients_Node = None
Updating = False

current_Line = 0 #Used by Write() function

def Check():
    global Clients_Node
    global Updating

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
    
    #Enable Python GC
    gc.enable()

    #Init Video
    Video.PyGame.InitVideo()

    #Setup Video
    Video.PyGame.SetVideo(800, 640, False)

    #Init FPS System
    Video.FPS.Init()

    #Update Window Caption To Current Ver
    pygame.display.set_caption(str("PyOnline Update Manager"))

    #Start Update Thread
    thread.start_new_thread(Run_Update, ())
    Updating = True

    #Updater Loop
    while Updating == True:
        #Handle Events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #Stop PyGame
                    pygame.quit()

                    #Exit Completly
                    sys.exit(0)

        #Update Display
        pygame.display.flip()

        #FPS Regulation
        Video.FPS.Tick()

        #Python Garbage Collection
        gc.collect()

    #We should be done with updates! Go ahead and start up the client! ^.^
    Write("Updates complete! Starting up PyOnline...")
    pygame.display.flip()
    time.sleep(2)
    Platform_Data = os.uname()[0]
    if Platform_Data == "Darwin":
        #Startup Update Manager for OSX
        os.system("open ../../../PyOnline.app/")
        time.sleep(0.2)
        sys.exit(0)

    elif Platform_Data == "Windows": #TODO: What is os.uname[0] value under win32?
        pass
    elif Platform_Data == "Linux": #TODO: What is os.uname[0] value under *nix systems
        pass

#Runs the actual updating procress (This is ran in its own thread)
def Run_Update():
    global Update_Tmp_Path
    global Root_Path_From_Update_Tmp
    global Clients_Node
    global Updating
    global current_Line

    #Font for update stuff
    if str(os.uname()[0]) == "Darwin":
        Info_Font = pygame.font.Font("../../../PyOnline.app/Contents/Resources/data/fonts/VeraMoBd.ttf", 10)
    else:
        Info_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 10)

    #If using OSX, update tmp path location
    if str(os.uname()[0]) == "Darwin":
        tmp = "../../../PyOnline.app/Contents/Resources/"
        Update_Tmp_Path = str(str(tmp) + str(Update_Tmp_Path))

    #Update user on current progress
    Write("Starting to update - PLEASE DO NOT CLOSE!")
    time.sleep(0.2) #Delay for a moment

    #Detect platform
    Write("Detecting your OS platform...", update_line=False)
    Platform = None
    Platform_Data = os.uname()[0]

    if Platform_Data == "Darwin":
        Platform = "osx"
    elif Platform_Data == "Windows": #TODO: What is os.uname[0] value under win32?
        Platform = "win32"
    elif Platform_Data == "Linux": #TODO: What is os.uname[0] value under *nix systems
        Platform == "linux"

    #Update user on current progress
    Write(str(str("[Detected: ") + str(Platform) + str("]")), 180)

    #Get XML nodes for each client platform
    Write("Getting update information for your platform...")
    Win32_Node = None
    OSX_Node = None
    Linux_Node = None

    for i in range(0, len(Clients_Node)):
        #win32
        if Clients_Node[i].nodeName == "win32":
            Win32_Node = Clients_Node[i]
            print "Found Client Platform: win32"

        #osx
        elif Clients_Node[i].nodeName == "osx":
            OSX_Node = Clients_Node[i]
            print "Found Client Platform: osx"

        #linux
        elif Clients_Node[i].nodeName == "linux":
            Linux_Node = Clients_Node[i]
            print "Found Client Platform: linux"

    #Holds information about the files that will be updated
    Remote_Files = []
    Local_Files = []

    #Get information about update - win32
    if Platform == "win32":
        #Get file information for update
        for i in range(0, len(Win32_Node.childNodes)):
            #Go through each <file></file> block
            if Win32_Node.childNodes[i].nodeName == "file":
                #Get the remote file and local file information
                for i2 in range(0, len(Win32_Node.childNodes[i].childNodes)):
                    #Remote File
                    if Win32_Node.childNodes[i].childNodes[i2].nodeName == "updated_loc":
                        Remote_Files.append(str(Win32_Node.childNodes[i].childNodes[i2].childNodes[0].nodeValue))

                    #Local File
                    elif Win32_Node.childNodes[i].childNodes[i2].nodeName == "local_loc":
                        try:
                            Local_Files.append(str(Win32_Node.childNodes[i].childNodes[i2].childNodes[0].nodeValue))
                        except:
                            #Set to root directory if nothing is present
                            Local_Files.append("")


    #Get information about update - osx
    elif Platform == "osx":
        #Get file information for update
        for i in range(0, len(OSX_Node.childNodes)):
            #Go through each <file></file> block
            if OSX_Node.childNodes[i].nodeName == "file":
                #Get the remote file and local file information
                for i2 in range(0, len(OSX_Node.childNodes[i].childNodes)):
                    #Remote File
                    if OSX_Node.childNodes[i].childNodes[i2].nodeName == "updated_loc":
                        Remote_Files.append(str(OSX_Node.childNodes[i].childNodes[i2].childNodes[0].nodeValue))

                    #Local File
                    elif OSX_Node.childNodes[i].childNodes[i2].nodeName == "local_loc":
                        try:
                            Local_Files.append(str(OSX_Node.childNodes[i].childNodes[i2].childNodes[0].nodeValue))
                        except:
                            #Set to root directory if nothing is present
                            Local_Files.append("../../../")

    #Get information about update - linux
    elif Platform == "linux":
        #Get file information for update
        for i in range(0, len(Linux_Node.childNodes)):
            #Go through each <file></file> block
            if Linux_Node.childNodes[i].nodeName == "file":
                #Get the remote file and local file information
                for i2 in range(0, len(Linux_Node.childNodes[i].childNodes)):
                    #Remote File
                    if Linux_Node.childNodes[i].childNodes[i2].nodeName == "updated_loc":
                        Remote_Files.append(str(Linux_Node.childNodes[i].childNodes[i2].childNodes[0].nodeValue))

                    #Local File
                    elif Linux_Node.childNodes[i].childNodes[i2].nodeName == "local_loc":
                        try:
                            Local_Files.append(str(Linux_Node.childNodes[i].childNodes[i2].childNodes[0].nodeValue))
                        except:
                            #Set to root directory if nothing is present
                            Local_Files.append("")


    #Update user on current progress
    Write("Starting file download...")
    for i in range(0,len(Remote_Files)):
        print "Remote file \"" + str(Remote_Files[i]) + "\" is replacing local file \"" + str(Local_Files[i]) + "\""
    

    ############################################################################################################
    #Downlaod Demo from http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
    #url = "http://blog.zachr.co/images/PyOnline_Demo.png"

    #file_name = url.split('/')[-1]
    #u = urllib2.urlopen(url)
    #f = open(file_name, 'wb')
    #meta = u.info()
    #file_size = int(meta.getheaders("Content-Length")[0])
    #print "Downloading: %s Bytes: %s" % (file_name, file_size)

    #file_size_dl = 0
    #block_sz = int(file_size/10)
    #while True:
    #    buffer = u.read(block_sz)
    #    if not buffer:
    #        break

    #    file_size_dl += block_sz
    #    f.write(buffer)
    #    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    #    status = status + chr(8)*(len(status)+1)
    #    print status,

    #f.close()
    ############################################################################################################

    #Start downloading files
    #Remove any old update data in Update_Tmp_Path
    Write("Checking and removing any old temp files from any previous updates...")
    for root, dirs, files in os.walk(str(Update_Tmp_Path)):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    #Remove old Update_Tmp_Path folder
    if os.path.exists(str(Update_Tmp_Path)):
        os.removedirs(str(Update_Tmp_Path))


    #Create a new directory for downloads
    os.mkdir(str(Update_Tmp_Path))

    #Go through each Remote_File[] and download to Update_Tmp_Path(tmp folder for update data)
    for i in range(0, len(Remote_Files)):
        File_To_Download = str(Remote_Files[i])
        Save_Location = str(str(Update_Tmp_Path) + "/" + str(File_To_Download.split('/')[-1]))

        File_Remote = urllib2.urlopen(File_To_Download)
        File_Local = open(Save_Location, 'wb')
        Meta_Data = File_Remote.info()
        File_Remote_Size = int(Meta_Data.getheaders("Content-Length")[0])

        Write(str("Downloading " + str(File_To_Download.split('/')[-1])), 0, 15*(5+i))

        File_Remote_Size_dl = 0 #Keeps track of how much of the file is downloaded
        Block_SZ = int(File_Remote_Size/10) #Download buffer size

        old_Status = ""
        while True:
            buffer = File_Remote.read(Block_SZ)
            if not buffer:
                #File is downloaded, end download loop
                break

            #Update varibles
            File_Remote_Size_dl += Block_SZ

            #Write file data locally
            File_Local.write(buffer)

            #Update user on current status of download
            status = str(str(int(File_Remote_Size_dl / 1000)) + " KB /" +  str(int(File_Remote_Size / 1000)) + " KB" + "[" + str(File_Remote_Size_dl * 100. / File_Remote_Size) + "%]")

            #Clear old status buffer on screen
            Write(old_Status, int((len(str("Downloading " + str(File_To_Download.split('/')[-1]))) * 8)), update_line=False, black=True)

            #Write status buffer to screen
            Write(status, int((len(str("Downloading " + str(File_To_Download.split('/')[-1]))) * 8)), update_line=False)

            #Update old_Status Buffer
            old_Status = status

        #Close our local file
        File_Local.close()

        #Increase current_Line for the Write() function (so status for next file download is on a new line)
        current_Line += 15

    #Update user on current progress
    Write("All files are downloaded!")
    Write("Installing downloaded files accordingly...")

    #Go through each downloaded file and place them accordingly
    for i in range(0, len(Remote_Files)):
        #Get information about what files to move, and where
        Remote_File_Name = str(str(Remote_Files[i]).split('/')[-1])
        File_To_Move = str(str(Update_Tmp_Path) + "/" + str(Remote_File_Name))
        if len(str(Local_Files[i])) > 0:
            Move_Location = str(str(Local_Files[i]))
            #If using OSX, Move_Location
            if str(os.uname()[0]) == "Darwin":
                tmp = "../../../PyOnline.app/Contents/Resources/"
                Move_Location = str(str(tmp) + str(Move_Location))
        else:
            Move_Location = str(str(Local_Files[i]) + str(Remote_File_Name))
        Move_Path = str(Local_Files[i])

        #Check if the file is a .zip
        if zipfile.is_zipfile(File_To_Move):
            Write(str("Extracting " + str(Remote_File_Name) + "(may take some file if the file is large - PLEASE WAIT!)..."))

            #Open ZIP File
            zip = zipfile.ZipFile(File_To_Move)

            #Go through each file in the zip
            for File in zip.namelist():
                #Set Extract Location
                if len(str(Move_Path)) > 0:
                    Extract_Location = str(str(Move_Path) + "/" + str(File))
                else:
                    Extract_Location = str(str(Move_Path) + str(File))

                #print "Extracting", File, "to", Extract_Location

                #Make any directories from the zip file
                if str(File)[len(str(File))-1:len(str(File))] == "/":
                    #Only create directory if it doesn't exist
                    if os.path.exists(str(Extract_Location)) == False:
                        os.makedirs(str(Extract_Location))
                else:

                    #Before we extract the file, back up any old copies
                    if os.path.exists(str(Extract_Location)):
                        os.renames(str(Extract_Location), str(str(Extract_Location) + ".bak"))

                    #If its not a directory, pull the file
                    file(str(Extract_Location), 'wb').write(zip.read(str(File)))

                    #If we are running osx or linux, chomod files
                    if Platform == "osx" or Platform == "linux":
                        os.chmod(str(Extract_Location), 0777)
        else:
            #Make a backup of anyfiles that exist
            if os.path.exists(Move_Location):
                os.renames(str(Move_Location), str(str(Move_Location) + ".bak"))

            #Copy new files over
            Write(str("Updating ") + str(Remote_File_Name) + "...")
            #print "Attempting to move", File_To_Move, "to", Move_Location
            shutil.copy(str(File_To_Move), str(Move_Location))

    #Now that we are done with the update, pause for just a moment
    time.sleep(1)

    #Remove update.xml now that we are done
    if os.path.exists("update.xml"):
        #Remove old copy
        os.remove("update.xml")

    #Remove any update data in Update_Tmp_Path now that we are done
    Write("Removing all temp files from update...")
    for root, dirs, files in os.walk(str(Update_Tmp_Path)):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

    #Remove old Update_Tmp_Path folder now that we are done
    if os.path.exists(str(Update_Tmp_Path)):
        os.removedirs(str(Update_Tmp_Path))

    #Done Updating
    Updating = False


#Used to write text to the screen during updating
def Write(text, x=0, update_line=True, black=False):
    global current_Line

    #Font for update stuff
    if str(os.uname()[0]) == "Darwin":
        Info_Font = pygame.font.Font("../../../PyOnline.app/Contents/Resources/data/fonts/VeraMoBd.ttf", 10)
    else:
        Info_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 10)

    #Display Loding Information
    if black != True:
        InfoSurf = Info_Font.render(str(text), True, (255,255,255))
    else:
        InfoSurf = Info_Font.render(str(text), True, (0,0,0))

    Video.PyGame.Screen.blit(InfoSurf, (int(x),int(current_Line))) #Render Text

    if update_line == True:
        current_Line += 15


#Run Update Check
Check()