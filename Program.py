from AESAlgorithm import AESAlgorithm
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)  # 16 bytes key for AES-128
aes = AESAlgorithm(key)
plaintext = 'Hello, world!'
c = aes.encrypt(plaintext)
print("Ciphertext:", c.ciphertext)
decrypted_text = aes.decrypt(c)
print("Decrypted text:", decrypted_text)
