from Crypto.Cipher import AES
from CipherMessage import CipherMessage


# algorithm class used to encrypt and decrypt plaintext strings
class AESAlgorithm:
    # initialization of the AES class keeps the key stored for continuous use
    def __init__(self, key):
        self.key = key

    # encrypt method takes a plaintext string as input and outputs a CipherMessage object containing an encrypted
    # bytestream and a nonce used for encryption
    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CTR)
        ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
        return CipherMessage(ciphertext, cipher.nonce)

    # decrypt method takes a CipherMessage object containing an encrypted bytestream and a nonce as input and outputs
    # a plaintext string
    def decrypt(self, ciphermessage):
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=ciphermessage.nonce)
        plaintext = cipher.decrypt(ciphermessage.ciphertext)
        return plaintext.decode('utf-8')
