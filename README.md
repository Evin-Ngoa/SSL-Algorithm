
 > NAME        : EVINGTONE NGOA
 > TITLE       : SSL ALGORITHM [RSA AND SHARED KEY MODEL]
 > LANGUAGE    : PYTHON 3
 
 # SSL-TLS ALGORITHM
A very basic implementation of SSL Algorithm written in Python
### How It Works
---------------------------------------------------------------------------------------- 
1. Server Generates the certificates [Keys] and waits for client connection 
2. Client sends ClientHello Message to Server 
3. Server receives the message and sends ServerHello and its public key to Client 
4. Clients receives the public key and generates secret key 
5. The secret key is encrypted with the server public key and sent to the server. 
6. The server receives the ciphertext and decrypts with its private key to get the key. 
7. The server return finished message to client. Handshake Completed!!!
8. Client sends message to server while encrypted with the secret key. 
9. Server Decrypts message using the private key shared earlier step 5.
DONE
--------------------------------------------------------------------------------------- 
# How To Run
1. Clone The Project
2. Navigate Into The Folder
3. Open TWO Terminals
4. One Terminal run ``` python server.py```
5. Wait for server to generate certificates.
6. Second Terminal run   ``` python client.py```

## Enjoy!!



[Check out my Portfolio](http://evin.me.ke/ "Evin's portfolio")
![alt text](http://evin.me.ke/wp-content/uploads/2016/07/evin-100X50.png "Check Out My portfolio")