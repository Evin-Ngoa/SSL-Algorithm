"""
EVINGTONE NGOA MWAILONGO

HOW TO RUN
1. Open TWO Terminals. 
2. One Terminal run ``` python server.py```
3. Wait for server to generate certificates.
4. Second Terminal run   ``` python client.py```
"""
# first of all import the socket library 
import socket			 
import time		
import keyGen

# reserve a PORT on your computer in our 
# case it is 12345 but it can be anything 
PORT = 12345	
HOST = 'localhost'		
server_address = (HOST, PORT)	
SLEEPING_TIME = 3

def brand():
    print("-----------------------ALGORITHM DESCRIPTION-------------------------------------------")
    print("SSL ALGORITHM")
    print("1. Server Generates the certificates [Keys] and waits for client connection")
    print("2. Client sends ClientHello Message to Server")
    print("3. Server receives the message and sends ServerHello and its public key to Client")
    print("4. Clients receives the public key and generates secret key")
    print("5. The secret key is encrypted with the server public key and sent to the server.")
    print("6. The server receives the ciphertext and decrypts with its private key to get the key.")
    print("7. Handshake Done!")
    print("8. Client sends message to server while encrypted with the secret key.")
    print("9. Server Decrypts message using the private key shared earlier step 5.")
    print("---------------------------------------------------------------------------------------")
    print("\n\n")

# Generate Server Certificates
def genServerKeys():
    print(f"\n Generating Server Keys ... \n")

    time.sleep(SLEEPING_TIME)

    listKeys = keyGen.getPublicPrivate()

    return listKeys

# initiate Port Connection
def initPortConnection(PORT, HOST, server_address):

    listKeys = genServerKeys()

    print(f" SERVER CERTIFICATES =====> Public Key = ({listKeys[0]}, {listKeys[1]}) || Private Key= ({listKeys[2]}, {listKeys[3]})")
    
    # next create a socket object 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		 
    print(" Socket successfully created")

    time.sleep(SLEEPING_TIME)

    # Next bind to the PORT 
    # we have not typed any ip in the ip field 
    # instead we have inputted an empty string 
    # this makes the server listen to requests 
    # coming from other computers on the network 
    s.bind(server_address)		 
    print(" Socket bind to %s" %(PORT)) 
    time.sleep(SLEEPING_TIME)
    receiveMsg(s, listKeys)	

# Function to Listen and Receive
# Messages sent from Client
def receiveMsg(s, listKeys):
    # put the socket into listening mode 
    s.listen(5)	 
    print(" Socket is listening")
    brand()

    time.sleep(SLEEPING_TIME)

    # a forever loop until we interrupt it or 
    # an error occurs 
    while True: 

        # Establish connection with client. 
        conn, addr = s.accept()	 
        print('\n Got connection from', addr )
        time.sleep(SLEEPING_TIME)
        while True:
            # data = connection.recv(16)
            # print('received {!r}'.format(data))
            data = conn.recv(1024)
            print('\n Received From Client: {!r}'.format(data))
            time.sleep(SLEEPING_TIME)

            # decode Message
            decodedMsg = data.decode()
            if data:
                # Checking 1st Time 
                if(decodedMsg == 'ClientHello'):
                    print('\n Sending data back to the client...\n')
                    time.sleep(SLEEPING_TIME)

                    # Sends back Server Hello
                    # string with encoding 'utf-8'
                    message = 'ServerHello | (' + str(listKeys[0]) + ',' + str(listKeys[1]) +')'
                    bytMsg = bytes(message, 'utf-8')

                    # send a thank you message to the client. 
                    conn.sendall(bytMsg) 
                    # connection.sendall(data)
                elif(decodedMsg.find('-') != -1):
                    cipherTextList = decodedMsg.split('-')

                    # Converting all strings in th list to integers.
                    cipherTextList = list(map(int, cipherTextList))
                    time.sleep(SLEEPING_TIME)

                    print(f"\n Separated = {cipherTextList}")

                    plainText = keyGen.decryptRSA(cipherTextList , int(listKeys[2]), int(listKeys[3]))

                    print(f"\n PlainText = {plainText}")

                    print(f"\n RSA Handshake Completed!! ")
                else:
                    print(f"\n PlainText '_' => {plainText} \n ")
                    secretKey = extractKey(plainText)
                    print(f"\n secretKey Value '_' => {secretKey} \n ")

                    print(f"\n Else Msg => {decodedMsg} \n ")

                    splitText = decodedMsg.split('_')

                    # Converting all strings in th list to integers.
                    splitText = list(map(int, splitText))

                    print(f"\n splitText Integer => {splitText} \n ")

                    plainText = decryptionProcess(splitText, secretKey)

                    print(f"\n plainText => {plainText} \n ")

                    print(f"\n SSL-TLS COMMUNICATION DONE!!! \n ")
                    break

            else:
                print(' No data from client with Address : ', addr)
                break



        # Close the connection with the client 
    conn.close() 

# Extract Secret Key from
# Text Key
def extractKey(secretKeyText):
    splitText = secretKeyText.split('-')
    print(f"splitText => {splitText}\n")

    # convert the lastvalue into integer
    secretKeyValue = int(splitText[-1])
    print(f"secretKeyValue => {secretKeyValue}\n")

    return secretKeyValue

# Decrypting the Message from Client Using the 
# shared key
def decryptionProcess(cipherTxt, decryptionKey):
    decValList = []

    print("\nDecryption Key => ", decryptionKey)

    for char in cipherTxt:
        # Compute Original Unicode
        getUnicode = int(char / decryptionKey)
        # Convert Each Char from Unicode
        decryptedChar = chr(getUnicode)
        decValList.append( decryptedChar )

    plaintext = "".join(decValList)

    return plaintext

def main():
    initPortConnection(PORT, HOST, server_address)

main()