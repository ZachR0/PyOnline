##FROM: http://code.activestate.com/recipes/266586-simple-xor-keyword-encryption/ ##

#Modules
import random
import zlib

#Encrypts/Decrypts data based on a key
def tinycode(key, text, reverse=False):
    rand = random.Random(key).randrange
    if not reverse:
        text = zlib.compress(text)
    text = ''.join([chr(ord(elem)^rand(256)) for elem in text])
    if reverse:
        text = zlib.decompress(text)
    return text

#Converts a string to Hex
def strToHex(aString):
    hexlist = ["%02X " % ord(x) for x in aString]
    return ''.join(hexlist)