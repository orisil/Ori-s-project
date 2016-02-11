
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import sys


BLOCK_SIZE = 32
INTERRUPT = u'\u0001'
PAD = u'\u0000'



# Strip your data after decryption (with pad and interrupt)
def StripPadding(data):
    return data.rstrip(PAD).rstrip(INTERRUPT)


# Decrypt the given encrypted data with the decryption cypher
def DecryptWithAES(decrypt_cipher, encrypted_data ):
    decoded_encrypted_data = b64decode(encrypted_data)
    decrypted_data = decrypt_cipher.decrypt(decoded_encrypted_data)
    return StripPadding(decrypted_data)


# Pad your data before encryption (with pad and interrupt)
def AddPadding(data, block_size):
    new_data = ''.join([data, INTERRUPT])
    new_data_len = len(new_data)
    remaining_len = block_size - new_data_len
    to_pad_len = remaining_len % block_size
    pad_string = PAD * to_pad_len
    return''.join([new_data, pad_string])


# Encrypt the given data with the encryption cypher
def EncryptWithAES(encrypt_cipher, plaintext_data):
    plaintext_padded = AddPadding(plaintext_data, BLOCK_SIZE)
    encrypted = encrypt_cipher.encrypt(plaintext_padded)
    return b64encode(encrypted)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


    def encryptAES(secretKEY, data_to_encrypt):
        try:

            # Creating the encryption & decryption cipher objects:
            # MODE - optional
            # IV - optional
            encryption_cypher = AES.new(secretKEY)

            # Encrypt the data
            encrypted_data = EncryptWithAES(encryption_cypher, data_to_encrypt)
            return   encrypted_data   

        # Catch the exceptions
        except Usage, err:
            print>>sys.stderr, err.msg
            print>>sys.stderr, "for help use --help"
        return None

    def decryptAES(secretKEY, encrypted_data ):
        try:
            # Creating the encryption & decryption cipher objects:
            # MODE - optional
            # IV - optional
            decryption_cypher = AES.new(secretKEY)

            # Decrypt the data
            decrypted_data = DecryptWithAES(decryption_cypher, encrypted_data)
            return   decrypted_data   
       # Catch The exceptions
        except Usage, err:
            print>>sys.stderr, err.msg
            print>>sys.stderr, "for help use --help"
        return None


