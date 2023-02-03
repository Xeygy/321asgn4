import bcrypt
from nltk.corpus import words
from multiprocessing import Pool, Event

N_PARTS = 8
word_dict = words.words("en")
seg_size = len(word_dict)//N_PARTS
word_lists = []

def check_bcrypt(word_list):
    hashed = b"$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq"
    for indx, passwd in enumerate(word_list):
        if bcrypt.checkpw(passwd.encode('utf-8'), hashed):
            print("found:", passwd)
        if indx % 1000 == 0:
            print(passwd)

if __name__ == '__main__':
    for i in range(N_PARTS-1):
        start, end = seg_size*i, seg_size*(i+1)
        word_lists.append(word_dict[start:end])
    word_lists.append(word_dict[end:])

    with Pool(N_PARTS) as p:
        p.map(check_bcrypt, word_lists)

# found: welcome
