#!/usr/bin/python3

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from platform import platform
from random import randint
from os.path import exists
from os import urandom
from os import system
from sys import argv

def generateKeys():
    ident = str(randint(1100, 9999))
    standartKey = ident + "keybn"
    if exists(standartKey):
        question = input("Overwrite this file ? (y or n) ")
        if not question:
            print("No command! --> raise SystemExit")
            raise SystemExit
        else:
            if question == "y":
                open(standartKey, 'w').write('')
                for entropy in range(5):
                    keys = Fernet.generate_key().decode('utf-8')
                    open(standartKey, 'a').write(keys+"\n")
            else:
                print("No command! --> raise SystemExit")
                raise SystemExit
    else:
        for entropy in range(5):
            keys = Fernet.generate_key().decode('utf-8')
            open(standartKey, 'a').write(keys+"\n")
        
        if platform == 'win32':
            system("cls")
        else:
            system("clear")

        print("")
        print("")
        print("-----------------------------------------------------------------------------")
        print("")
        print("# # # # # Your new key ID -->",ident,"|    ",standartKey,"    |       AES-128-CBC")
        print("")
        print("-----------------------------------------------------------------------------")
        print("")
        print("")

def SignKeyFunc():
    signKeyF = str(input("Enter path to key : "))
    if not signKeyF:
        print("No command! --> raise SystemExit")
        raise SystemExit
    else:
        if not exists(signKeyF):
            print("File not found! --> raise SystemExit")
            raise SystemExit
        else:
            if signKeyF == argv[0]:
                print("Error! It is File --> raise SystemExit")
                raise SystemExit
            else:
                PswSignKey = str(input("Enter password to sign key : "))
                if not PswSignKey:
                    print("No command! --> raise SystemExit")
                    raise SystemExit
                else:
                    if PswSignKey == argv[0]:
                        print('Filename can not be password! --> raise SystemExit')
                        raise SystemExit
                    else:
                        secondVerification = str(input("Enter second verification code : "))
                        if not secondVerification:
                            print("No command! --> raise SystemExit")
                            raise SystemExit
                        else:
                            if secondVerification == argv[0]:
                                print("It can't be second verification code! --> raise SystemExit")
                                raise SystemExit
                            else:
                                DataKeyF = open(signKeyF, 'r').read().encode('utf-8')

                                startSign = PswSignKey.encode('utf-8')
                                saltSign = secondVerification.encode("utf-8")

                                kdf = PBKDF2HMAC(
                                    algorithm = hashes.SHA256(),
                                    salt = saltSign,
                                    length = 32,
                                    iterations = 900000
                                )
                                keyBase64Sign = urlsafe_b64encode(
                                    kdf.derive(startSign)
                                )
                                FernetKeyToken = Fernet(keyBase64Sign)
                                SignKey = FernetKeyToken.encrypt(DataKeyF)

                                open(signKeyF, 'wb').write(SignKey)

                                print("-----------------------------------------------------------------------------")
                                print("""
                The Key Was Successfully Signed!
                                """)
                                print("-----------------------------------------------------------------------------")
                        
def ChecKeyFunc():
    DecryptSignedKey = str(input("Enter path to key : "))
    if not DecryptSignedKey:
        print("No command! --> raise SystemExit")
        raise SystemExit
    else:
        if not exists(DecryptSignedKey):
            print("File not found! --> raise SystemExit")
            raise SystemExit
        else:
            if DecryptSignedKey == argv[0]:
                print('You don\'t decrypt this signed key! --> raise SystemExit')
                raise SystemExit
            else:
                PswSigneDec = str(input("Enter password for decryption key : "))
                if not PswSigneDec:
                    print('No command! --> raise SystemExit')
                    raise SystemExit
                else:
                    if PswSigneDec == argv[0]:
                        print("It can not be password! --> raise SystemExit")
                        raise SystemExit
                    else:
                        PswSecondVerify = str(input('Enter second verify code : '))
                        if not PswSecondVerify:
                            print("No command! --> raise SystemExit")
                            raise SystemExit
                        else:
                            if PswSecondVerify == argv[0]:
                                print("It can't be second verification code! --> raise SystemExit")
                                raise SystemExit
                            else:
                                ReadCipherKey = open(DecryptSignedKey, 'r').read().encode('utf-8')
                                PswKeyEncode = PswSigneDec.encode('utf-8')
                                CodedVerify = PswSecondVerify.encode('utf-8')

                                kdf = PBKDF2HMAC(
                                    algorithm = hashes.SHA256(),
                                    salt = CodedVerify,
                                    length = 32,
                                    iterations = 900000
                                )
                                keyBase64Sign = urlsafe_b64encode(
                                    kdf.derive(PswKeyEncode)
                                )
                                try:
                                    FernetKeyToken = Fernet(keyBase64Sign)
                                    SignKey = FernetKeyToken.decrypt(ReadCipherKey)
                                except:
                                    print("Incorrect Password! --> raise SystemExit")
                                    raise SystemExit

                                open(DecryptSignedKey, "wb").write(SignKey)
                                print("-----------------------------------------------------------------------------")
                                print("""
                The Key Was Successfully Checked!
                                """)
                                print("-----------------------------------------------------------------------------")

def encryptStream():
    loadFile = input("Enter path to file: ")
    if not loadFile:
        print("No command! --> raise SystemExit")
        raise SystemExit
    else:
        if not exists(loadFile):
            print("File not found! --> raise SystemExit")
            raise SystemExit
        else:
            if loadFile == argv[0]:
                print("You don't encrypt this file! --> raise SystemExit")
                raise SystemExit
            else:
                loadKeys = input("Enter path to keys: ")
                if not loadKeys:
                    print('No command! --> raise SystemExit')
                    raise SystemExit
                else:
                    if not exists(loadKeys):
                        print("File not found! --> raise SystemExit")
                        raise SystemExit
                    else:
                        if loadKeys == argv[0]:
                            print("Incorrect choose! --> raise SystemExit")
                            raise SystemExit
                        else:
                            getFile = open(loadFile, 'rb').read()
                            getKeys = open(loadKeys, 'r').read().split('\n')

                            cipherOne = Fernet(getKeys[3].encode('utf-8')) #4
                            cipherTwo = Fernet(getKeys[0].encode('utf-8')) #1
                            cipherThr = Fernet(getKeys[2].encode('utf-8')) #3
                            cipherFou = Fernet(getKeys[4].encode('utf-8')) #5
                            cipherFiv = Fernet(getKeys[1].encode('utf-8')) #2

                            iterOne = cipherOne.encrypt(getFile)
                            iterTwo = cipherTwo.encrypt(iterOne)
                            iterThr = cipherThr.encrypt(iterTwo)
                            iterFou = cipherFou.encrypt(iterThr)
                            iterFiv = cipherFiv.encrypt(iterFou)

                            file = open(loadFile, 'wb').write(iterFiv)

def decryptStream():
    encryptText = input("File for decryption : ")
    if not encryptText:
        print('No command! --> raise SystemExit')
        raise SystemExit
    else:
        if not exists(encryptText):
            print("File not found! --> raise SystemExit")
            raise SystemExit
        else:
            if encryptText == argv[0]:
                print("It isn't file for decryption! --> raise SystemExit")
                raise SystemExit
            else:
                decryptKeys = input("Enter path to key : ")
                if not decryptKeys:
                    print('No command! --> raise SystemExit')
                    raise SystemExit
                else:
                    if not exists(decryptKeys):
                        print("File not found! --> raise SystemExit")
                        raise SystemExit
                    else:
                        if decryptKeys == argv[0]:
                            print("It isn't key! --> raise SystemExit")
                            raise SystemExit
                        else:
                            encryptFile = open(encryptText, 'rb').read()
                            verifyKeys = open(decryptKeys, 'r').read().split('\n')
                            try:
                                decryptOne = Fernet(verifyKeys[1].encode('utf-8'))
                                decryptTwo = Fernet(verifyKeys[4].encode('utf-8'))
                                decryptThr = Fernet(verifyKeys[2].encode('utf-8'))
                                decryptFou = Fernet(verifyKeys[0].encode('utf-8'))
                                decryptFiv = Fernet(verifyKeys[3].encode('utf-8'))
                            except (ValueError, IndexError):
                                print("Incorrect Key! --> raise SystemExit")
                                raise SystemExit

                            try:
                                tryDecrypt1 = decryptOne.decrypt(encryptFile)
                                tryDecrypt2 = decryptTwo.decrypt(tryDecrypt1)
                                tryDecrypt3 = decryptThr.decrypt(tryDecrypt2)
                                tryDecrypt4 = decryptFou.decrypt(tryDecrypt3)
                                tryDecrypt5 = decryptFiv.decrypt(tryDecrypt4)
                                
                                ident = str(randint(1100, 9999))
                                fileOutDec = open("fileOut"+ident, 'wb').write(tryDecrypt5)

                                if platform != 'win32':
                                    system("clear")
                                else:
                                    system("cls")

                                print("")
                                print('')
                                print("Your decrypted file has ID -->",ident)
                                print("")
                                print('')
                                print("----------------------------------------------------------------")
                                print("# Please, rename the file! Otherwise you can't open this file!")
                                print("----------------------------------------------------------------")
                            except:
                                print("Decrypt Error! --> raise SystemExit")
                                raise SystemExit

def GetPlatformName():
    if platform == "win32":
        system("cls")
    else:
        system("clear")

    print("----------------------------------------------------------------")
    print("""
                11) Generate Key  | Open Key (default)
                22) Sign the Key  | Encrypt Key
                33) Check the Key | Decrypt Key
                44) Encrypt File  | AES-128-CBC
                55) Decrypt File  | AES-128-CBC
                00) Close Program | Exit (Ctrl + C)
    """)
    print("----------------------------------------------------------------")

def MainFunction():
    try:
        callFunctions = str(input("Enter command number : ( 11 or 33 ) "))
    except KeyboardInterrupt:
        print('\nSudden Stop!')
        raise SystemExit

    if callFunctions == "11":
        generateKeys()

    elif callFunctions == '22':
        SignKeyFunc()

    elif callFunctions == '33':
        ChecKeyFunc()

    elif callFunctions == "44":
        encryptStream()

    elif callFunctions == '55':
        decryptStream()

    elif callFunctions == "00":
        print("Closing --> raise SystemExit")
        raise SystemExit

    else:
        print("Unknown command! --> raise SystemExit")
        raise SystemExit

GetPlatformName()
MainFunction()

# BGDN-Group
# IMO +993 62632281
