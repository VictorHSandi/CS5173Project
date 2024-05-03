from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
from CipherMessage import CipherMessage


class AESAlgorithm:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CTR)
        ciphertext = cipher.encrypt(plaintext)
        return CipherMessage(ciphertext, cipher.nonce)

    def decrypt(self, ciphertext, nonce):
        cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8')
