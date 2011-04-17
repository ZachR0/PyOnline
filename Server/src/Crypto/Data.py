import Crypto.TinyCode

#Encryption Key
CRYPTO_KEY = "pyonline!crypto ENCRYPTION--00@@!!-PY0NLINE!"

#Encrypts data
def Encrypt(Raw_Data):
    global CRYPTO_KEY

    Data = Crypto.TinyCode.tinycode(CRYPTO_KEY, str(Raw_Data))

    return Data

#Decyrpts data
def Decrypt(Encrypted_Data):
    global CRYPTO_KEY

    Data = Crypto.TinyCode.tinycode(CRYPTO_KEY, str(Encrypted_Data), reverse=True)

    return Data