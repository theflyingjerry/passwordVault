import os
import hashlib
from pathlib import Path

salt =  os.urandom(32)
key = hashlib.pbkdf2_hmac('sha256','DCS21code'.encode('utf-8'),salt,100000)

storage = salt + key

p = Path.cwd()

hashFile = open(p/'hash.txt','wb')
hashFile.write(storage)
hashFile.close()