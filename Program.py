from AESAlgorithm import AESAlgorithm
from Crypto.Random import get_random_bytes
from Crypto.Util import number
import random
import hashlib

key = get_random_bytes(16)  # 16 bytes key for AES-128
aes = AESAlgorithm(key)
plaintext = 'Hello, world!'
c = aes.encrypt(plaintext)
print("Ciphertext:", c.ciphertext)
print("Nonce:", c.nonce)
decrypted_text = aes.decrypt(c)
print("Decrypted text:", decrypted_text)
raw_decrypted_text = aes.raw_decrypt(c.ciphertext, c.nonce)
print("Decrypted text:", raw_decrypted_text)
print(number.getPrime(20))
print(type(eval("900")))
sa = random.randint(10, 1000)
print(sa)
num = 261328
print(num)
print(hashlib.sha256(num.to_bytes(16,'big')).digest()[:16])
