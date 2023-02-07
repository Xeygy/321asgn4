import hashlib
import time

# part a
def sha256(message):
    return hashlib.sha256(message.encode())

# part b
string1 = "hello world"
s1_int = int.from_bytes(string1.encode('utf-8'), "big")
s2_int = s1_int ^ 1 # bit flip last bit
string2 = s2_int.to_bytes(s2_int.bit_length(), 'big').decode('utf-8')
print(sha256(string1).digest(), sha256(string2).digest())

# part c
def sha256modified(message, n):
    return bin(int.from_bytes(hashlib.sha256(message.encode()).digest(), "big"))[:n]

def collision_find(n):
    i = 0
    start_time = time.time()
    hashdict = {}
    while (True):
        hash = sha256modified(str(i), n)
        if hash in hashdict.keys():
            print(f"{n}:", i, time.time()-start_time)
            break
        hashdict[hash] = i
        i += 1

for i in range(8, 51, 2):
    collision_find(i)

# found "2693682" and "1743751" share hash:
# 1111101110000011001100110001011000000110000