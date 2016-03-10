import sys, pickle
try:  
    from AES_Decrypt import *
    from Crypto import Random
    from Crypto.PublicKey import RSA
except ImportError:
    raw_input("# pyCrypto module is not installed. Aborting the application...Please enter...")
    sys.exit(2)

RSA_KEY_SIZE = 1024      
BUF_SIZE = 65536        
RSA_BLOCK_SIZE = 128     
END_LINE = "\r\n"


class MyCrypto:   
    def __init__(self):
        self.rsa_key = RSA.generate(RSA_KEY_SIZE, Random.new().read)    # Server RSA key
        self.rsa_publicKey = self.rsa_key.publickey()

    def exchange_keys(self, clientSock):
    # 1 ------------ Pickle ( "Server_Public_Key" )
        pickled_rsa_publicKey = pickle.dumps(self.rsa_publicKey)
        clientSock.send(pickled_rsa_publicKey)
    # 2 ------------ Wait Client encrypt AES_KEY
        pickled_aes_key = clientSock.recv(BUF_SIZE)
        encrypt_aes_key = pickle.loads(pickled_aes_key)
    # Decryption encrypt_message
        decrypt_aes_key = self.rsa_key.decrypt(encrypt_aes_key)
        return decrypt_aes_key

    # This function encrypt and send all the data.
    def send_data(self, clientKEY, clientSock, msg_original):
        encrypted_data = encryptAES(clientKEY, msg_original)  
        clientSock.send(encrypted_data + END_LINE)

    # This function receive and decrypt all the data.
    def recv_data(self, clientKEY, clientSock):
        ret_string = clientSock.recv(BUF_SIZE).split(END_LINE)[0]
        return decryptAES(clientKEY, ret_string) 


