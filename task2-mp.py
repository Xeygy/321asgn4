import bcrypt
from nltk.corpus import words
from multiprocessing import Process, Queue
import time

N_PARTS = 8
word_dict = words.words("en")
word_dict = [w for w in word_dict if len(w) >= 6 and len(w) <= 10]
seg_size = len(word_dict)//N_PARTS
word_lists = []

# prints the current word it's checking every 1000 words.
def check_bcrypt(word_list, found_queue, wanted_hashes, salt, start_time):
    for indx, passwd in enumerate(word_list):
        curr_hashed = bcrypt.hashpw(passwd.encode('utf-8'), salt)
        if found_queue.empty():
            break
        if curr_hashed in wanted_hashes:
            print("found:", passwd, "for hash:", curr_hashed)
            t = (time.time() - start_time)
            print(f"time: {t//60}m {t%60}s")
            found_queue.get(timeout=5)
        if indx % 1000 == 0:
            print(passwd)

if __name__ == '__main__':
    # initialize chunks of data
    for i in range(N_PARTS-1):
        start, end = seg_size*i, seg_size*(i+1)
        word_lists.append(word_dict[start:end])
    word_lists.append(word_dict[end:])

    wanted_hashes = [
        b"$2b$13$6ypcazOOkUT/a7EwMuIjH.qbdqmHPDAC9B5c37RT9gEw18BX6FOay"
    ]
    num_hashes = len(wanted_hashes)
    salt = wanted_hashes[0][0:29]
    print("finding words for shared salt", salt)
    
    # Fills queue with the num of hashes we want to find
    # Proc removes one from queue if found. Once queue is empty, stop search.
    found_queue = Queue()
    for i in range(num_hashes):
        found_queue.put_nowait(i)
    
    procs = []
    start_time = time.time()
    for i in range(N_PARTS):
        proc = Process(target=check_bcrypt, args=(word_lists[i], found_queue, wanted_hashes, salt, start_time))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

