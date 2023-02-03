# import nltk
# nltk.download('words')
import bcrypt
from nltk.corpus import words
word_dict = words.words("en")
print(len(word_dict))

def check_bcrypt(hashed):
    for indx, passwd in enumerate(word_dict):
        if bcrypt.checkpw(passwd.encode('utf-8'), hashed):
            print("found:", passwd)
        if indx % 1000 == 0:
            print(passwd)

# check_bcrypt(b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq")

# passwd = b's$cret12'

# salt = bcrypt.gensalt()
# hashed = bcrypt.hashpw(passwd, salt)
# print(hashed)
hashed = b'$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq'
# passwd = 's$cret12'.encode('utf-8')
# if bcrypt.checkpw(passwd, hashed):
#     print("match")
# else:
#     print("does not match")
salt = hashed[0:29]
hashed = bcrypt.hashpw(b"welcome", salt)
print(hashed)
# hashed.split(b"$", 3)[2])
