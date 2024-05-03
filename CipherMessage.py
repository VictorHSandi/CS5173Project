# container class for the AES encrypted bytestream and the nonce (salt) used to encrypt/decrypt it
class CipherMessage:
    def __init__(self, ciphertext, nonce):
        self.ciphertext = ciphertext
        self.nonce = nonce
