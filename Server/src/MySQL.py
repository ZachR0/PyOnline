import pymysql

#MYSQL_SERVER = '5.22.194.34' #Hamachi
MYSQL_SERVER = '127.0.0.1' #Localy (When server running on VPS)
#MYSQL_SERVER = '66.11.227.39' #When server is running locally
MYSQL_PORT = 3306
MYSQL_USERNAME = 'pyonline_client'
MYSQL_PASS = 'tbaj*$&dlja'
MYSQL_DB = 'PyOnline'

Account_Table = 'Accounts'
Character_Table = 'Characters'
NPC_Table = 'NPC'
Server_Table = 'Server'

def Test():
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    conn = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
    Connection.autocommit(True)
    cur = conn.cursor()
    cur.execute("SELECT Password FROM Accounts WHERE Username='Zach'")
    # print cur.description
    #r = cur.fetchall()
    #print r
    # ...or...
    #for r in cur:
    #   print r

    Data = []
    count = 0
    for r in cur:
       Data.append(r[int(count)])
       count += 1

    print "Password for Zach's account is:", Data[0]

    cur.close()
    conn.close()

#Gets password from Account_Table based on username
def GetPassword(Username):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("SELECT Password FROM " + str(Account_Table) + " WHERE Username='" + str(Username) + "'")
        Cursor.execute(Command_Str)

        #Get data from the command
        Data = []
        count = 0
        for r in Cursor:
           Data.append(r[int(count)])
           count += 1

        #Data[0] should be the password
        return str(Data[0])
    except:

        return None

    return None

#Gets character id from Account_Table based on username
def GetCharID(Username):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("SELECT Character_ID FROM " + str(Account_Table) + " WHERE Username='" + str(Username) + "'")
        Cursor.execute(Command_Str)

        #Get data from the command
        Data = []
        count = 0
        for r in Cursor:
           Data.append(r[int(count)])
           count += 1

        
        
        

        #Data[0] should be the ID
        return str(Data[0])
    except:
        
        
        

        return None

    
    
    

    return None

#Gets character name based on char_id in Character_Table
def GetCharacterName(ID):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table
    
    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("SELECT Name FROM " + str(Character_Table) + " WHERE ID = '" + str(ID) + "'")
        Cursor.execute(Command_Str)

        #Get data from the command
        Data = []
        count = 0
        for r in Cursor:
           Data.append(r[int(count)])
           count += 1

        
        
        

        #Data[0] should be the name
        return str(Data[0])
    except:
        
        
        

        return None

    
    
    

    return None

#Gets character x cord based on char_id in Character_Table
def GetCharacterXPOS(ID):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("SELECT Last_XPos FROM " + str(Character_Table) + " WHERE ID = '" + str(ID) + "'")
        Cursor.execute(Command_Str)

        #Get data from the command
        Data = []
        count = 0
        for r in Cursor:
           Data.append(r[int(count)])
           count += 1

        
        
        

        #Data[0] should be the name
        return str(Data[0])
    except:
        
        
        

        return None

    
    
    

    return None

#Gets character y cord based on char_id in Character_Table
def GetCharacterYPOS(ID):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("SELECT Last_YPos FROM " + str(Character_Table) + " WHERE ID = '" + str(ID) + "'")
        Cursor.execute(Command_Str)

        #Get data from the command
        Data = []
        count = 0
        for r in Cursor:
           Data.append(r[int(count)])
           count += 1

        
        
        

        #Data[0] should be the name
        return str(Data[0])
    except:
        
        
        

        return None

    
    
    

    return None

#Gets character sprite info based on char_id in Character_Table
def GetCharacterSpriteInfo(ID):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("SELECT SpriteInfo_ID FROM " + str(Character_Table) + " WHERE ID = '" + str(ID) + "'")
        Cursor.execute(Command_Str)

        #Get data from the command
        Data = []
        count = 0
        for r in Cursor:
           Data.append(r[int(count)])
           count += 1

        
        
        

        #Data[0] should be the name
        return str(Data[0])
    except:
        
        
        

        return None

    
    
    

    return None

#Sets character last x cord based on char_id in Character_Table
def SetCharacterXPOS(ID, XPos):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("UPDATE " + str(Character_Table) + " SET Last_XPos = " + str(XPos) + " WHERE ID = '" + str(ID) + "'")
        Cursor.execute(Command_Str)

        
        
        
        
    except:
        pass

#Sets character last y cord based on char_id in Character_Table
def SetCharacterYPOS(ID, YPos):
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("UPDATE " + str(Character_Table) + " SET Last_YPos = " + str(YPos) + " WHERE ID = '" + str(ID) + "'")
        Cursor.execute(Command_Str)

        
        
        

    except:
        pass

#Gets Server Messages
def GetServerMessages():
    global MYSQL_SERVER
    global MYSQL_PORT
    global MYSQL_USERNAME
    global MYSQL_PASS
    global MYSQL_DB

    global Account_Table
    global Character_Table
    global NPC_Table
    global Server_Table
    
    Messages = []

    try:
        #Connect to the MySQL database
        Connection = pymysql.connect(host=MYSQL_SERVER, port=MYSQL_PORT, user=MYSQL_USERNAME, passwd=MYSQL_PASS, db=MYSQL_DB)
        Connection.autocommit(True)
        Cursor = Connection.cursor()

        #Execute the MySQL command
        Command_Str = str("SELECT Server_Message FROM " + str(Server_Table))
        Cursor.execute(Command_Str)

        #Get data from the command
        Data = Cursor.fetchall()

        for message in Data:
            Messages.append(message[0])

    except:
        pass

    #Return messages
    return Messages