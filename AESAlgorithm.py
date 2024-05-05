from Crypto.Cipher import AES
from CipherMessage import CipherMessage
import codecs

# algorithm class used to encrypt and decrypt plaintext strings
class AESAlgorithm:
    # initialization of the AES class keeps the key stored for continuous use
    def __init__(self, key):
        self.key = key
        self.format = 'ISO-8859-1'

    # encrypt method takes a plaintext string as input and outputs a CipherMessage object containing an encrypted
    # bytestream and a nonce used for encryption
    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CTR)
        ciphertext = cipher.encrypt(plaintext.encode(self.format))
        return CipherMessage(ciphertext, cipher.nonce)

    # decrypt method takes a CipherMessage object containing an encrypted bytestream and a nonce as input and outputs
    # a plaintext string
    def decrypt(self, ciphermessage):
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=ciphermessage.nonce)
        plaintext = cipher.decrypt(ciphermessage.ciphertext)
        return plaintext.decode(self.format)

    def raw_decrypt(self, ciphertext, nonce):
        CipherOBJ = CipherMessage(ciphertext,nonce)
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=CipherOBJ.nonce)
        plaintext = cipher.decrypt(CipherOBJ.ciphertext)
        return plaintext.decode(self.format)

