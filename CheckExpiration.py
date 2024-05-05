import datetime
import ExpirationDate
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)  # 16 bytes key for AES-128
expiration_date = ExpirationDate(datetime.datetime.now(), 1) #expires after 1 day

while(True):
    if(expiration_date.is_expired() == True):
        key = get_random_bytes(16) #key is updated
        expiration_date = expiration_date.genExpDate()
