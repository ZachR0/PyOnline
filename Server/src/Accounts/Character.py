import time
import Crypto.Data
import MySQL
def Initial_Setup(Auth_Status, client_socket, Account_Username):
    Char_ID = "NaN"
    Char_Name = "NaN"
    Char_X = "NaN"
    Char_Y = "NaN"
    Char_SpriteSheet = "NaN"
    Char_SpriteMap = "NaN"

    #Make sure we are authenticated (Security check)
    if Auth_Status == True:
        try:
            #Get Client Character ID
            Char_ID = MySQL.GetCharID(Account_Username)

            #Get character name
            Char_Name = MySQL.GetCharacterName(Char_ID)

            #Get character x,y
            Char_X = MySQL.GetCharacterXPOS(Char_ID)
            Char_Y = MySQL.GetCharacterYPOS(Char_ID)

            #Get SpriteInfo ID
            SpriteInfoID = MySQL.GetCharacterSpriteInfo(Char_ID)

            #Set Sprite Information Accordingly
            if SpriteInfoID == "0":
                Char_SpriteSheet = "data/sprites/player/Inu/Inu.png"
                Char_SpriteMap = "data/sprites/player/Inu/SpriteMap.sm"

            elif SpriteInfoID == "1":
                Char_SpriteSheet = "data/sprites/player/Ash/Ash.png"
                Char_SpriteMap = "data/sprites/player/Ash/SpriteMap.sm"

            else:
                Char_SpriteSheet = "data/sprites/player/Inu/Inu.png"
                Char_SpriteMap = "data/sprites/player/Inu/SpriteMap.sm"

            #Send sprite info to client
            client_socket.send(Crypto.Data.Encrypt(Char_SpriteSheet))
            time.sleep(0.02) #Delay sending (prevent flood / allow processing time)
            client_socket.send(Crypto.Data.Encrypt(Char_SpriteMap))
            time.sleep(0.02) #Delay sending (prevent flood / allow processing time)

            #Send character name to client
            client_socket.send(Crypto.Data.Encrypt(Char_Name))
            time.sleep(0.02) #Delay sending (prevent flood / allow processing time)

            #Send character x,y to client
            client_socket.send(Crypto.Data.Encrypt(Char_X))
            time.sleep(0.02) #Delay sending (prevent flood / allow processing time)
            client_socket.send(Crypto.Data.Encrypt(Char_Y))
            time.sleep(0.02) #Delay sending (prevent flood / allow processing time)
        except Exception,e:
            print e

    #Return character information
    return Char_ID, Char_Name, Char_X, Char_Y, Char_SpriteSheet, Char_SpriteMap