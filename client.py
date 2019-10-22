"""
EVINGTONE NGOA MWAILONGO

HOW TO RUN
1. Open TWO Terminals. 
2. One Terminal run ``` python server.py```
3. Wait for server to generate certificates.
4. Second Terminal run   ``` python client.py```
"""
# Import socket module 
import socket                
import time  
import keyGen    
import random
  
# Define the port on which you want to connect 
PORT = 12345	
HOST = 'localhost'		
server_address = (HOST, PORT)	
SLEEPING_TIME = 3
MESSAGE = 'Hello There, I am A client'  


# initiate Port Connection
def iniPortConnection():
    # Create a socket object 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

    # connect to the server on local computer 
    sock.connect(server_address) 

    # Sending Hello Message
    message = b'ClientHello'
    print(f"Sending \'ClientHello\' to Server ...")
    time.sleep(SLEEPING_TIME)
    initMsgSender(sock, message)
    
    while True:
        # Receiving Server Message
        # receive data from the server 
        data = sock.recv(1024)

        #decode Message
        decodedMsg = data.decode()
        if(decodedMsg.find('ServerHello') != -1):
            serverPublickey = receiveMsg(decodedMsg)

            # Client Generate Secret Key
            secretKey = secretKeyGen()

            # Encrypt the Secret Key With the 
    # Encrypt the Secret Key With the 
            # Encrypt the Secret Key With the 
            # the server Public Key
            cipherText = encryptSecretKey(serverPublickey, secretKey)

            # Send the CipherText
            cipherbyte = bytes(cipherText, 'utf-8')
            print(f"Sending \'secret Key\' to Server ...\n")
            
            time.sleep(SLEEPING_TIME)
            initMsgSender(sock, cipherbyte)
            print(f"CipherText Sent => {cipherText}")

            # Sleep for more time wait for server to decrypt key
            # Sleep for 9 sec [3 * 3]
            time.sleep(SLEEPING_TIME*4)

            cipherSecretTxt = encryptWithSecretKey(secretKey)

            # print(f"cipherSecretTxt  => {cipherSecretTxt}\n")

            # Convert each value in list into string
            cipherSecretTxt = list(map(str, cipherSecretTxt))

            cipherscrttext = "_".join(str(intVal) for intVal in cipherSecretTxt)
            print(f"cipherSecretTxt Cipher => {cipherscrttext}\n")
        else:
            print(f"Client Received ==> {decodedMsg}")
            print(f"\n HANDSHAKE COMPLETED !!! \n ")

            # Send the cipherSecretTxt
            cipherSecretbyte = bytes(cipherscrttext, 'utf-8')
            print(f"Sending \'{MESSAGE}\' encrypted with secret Key to Server ...\n")
            
            time.sleep(SLEEPING_TIME)
            initMsgSender(sock, cipherSecretbyte)
            print(f"Message CipherText Sent => {cipherText}")
            break

    # close the connection 
    sock.close() 

# Encrypting Secret Shared Key
def encryptWithSecretKey(secretKey):
    splitText = secretKey.split('-')
    print(f"splitText => {splitText}\n")

    # convert the lastvalue into integer
    secretKeyValue = int(splitText[-1])
    print(f"secretKeyValue => {secretKeyValue}\n")

    # Message to be transmitted
    cipherTxt = encryptionProcessData(MESSAGE, secretKeyValue)

    print(f"cipherTxtin function => {cipherTxt}\n")

    return cipherTxt

# Encryption Logic with Key
def encryptionProcessData(word, encryptionKey):
    encValList = []
    # Convert the word into list chars
    wordList = list(word)

    print("\nEncryption Key => ", encryptionKey)

    for char in wordList:
        unicodeChar = ord(char)
        # Hashing the word with the Key
        encValList.append( unicodeChar * encryptionKey)

    return encValList

# Encrypt secret key with server 
# public Key
def encryptSecretKey(serverPublickey, secretKey):
    print(f"\nEncrypting Secret Key...\n")

    time.sleep(SLEEPING_TIME)

    eVal = int(serverPublickey[0])
    nVal = int(serverPublickey[1])
    # print(f"\n eVal = {eVal} | nVal = {nVal} \n")
    cipherList = keyGen.encryptRSA(secretKey, eVal, nVal)

    print(f"\nCipher Secret Key => {cipherList}\n")

    # creating separator to be split 
    ciphertext = "-".join(str(intVal) for intVal in cipherList)

    return ciphertext

# Generate Client Secret Key
# encrypt with RSA 
# send to server to get the secret key
def secretKeyGen():
    Min = 1000000
    Max = 2000000
    print(f"\nGenerating Secret Key...\n")

    time.sleep(SLEEPING_TIME)
    secretVal = random.randint(Min,Max)
    secretK = "this-is-a-secret-key-" + str(secretVal)

    print(f"\nSecret Key => {secretK}\n")

    return secretK

# Handles Receiving Message 
# From Server
def receiveMsg(decodedMsg):
    # receive data from the server 
    # data = sock.recv(1024)

    #decode Message
    # decodedMsg = data.decode()

    print(f"\n Client Received ---> {decodedMsg}")

    keys = extractKeys(decodedMsg)

    print(f"\nServer Public Key => {keys} \n")

    return keys

def extractKeys(decodedMsg):

    # Remove of the pipe symbol 
    # generalResponseString => Hello FROM SERVER generalKeyString => (5,28757)
    generalResponseString, generalKeyString = decodedMsg.split(' | ')
    # print(f"generalResponseString => {generalResponseString} generalKeyString => {generalKeyString}")
    
    # Seperate by commas bracketE => (5 bracketN => 28757)
    bracketE ,bracketN = generalKeyString.split(',')
    # print(f"bracketE => {bracketE} bracketN => {bracketN}")

    # Remove Brackets  filteredE => ['', '5'] filteredN => ['28757', '']
    filteredE = bracketE.split('(')
    filteredN = bracketN.split(')')
    # print(f"filteredE => {filteredE} filteredN => {filteredN}")

    # Getting the exact values
    valE = filteredE[1]
    valN = filteredN[0]

    ENKey = [valE, valN]

    return ENKey

def initMsgSender(sock, message):
    sock.sendall(message)


def main():
    iniPortConnection()



main()