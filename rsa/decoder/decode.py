import numpy as np
import textwrap
from typing import Callable


def fast_pow(a, e, n):
    res = 1
    for i in range(e):
        if((e >> i) % 2 == 1): 
            res = (res * a) % n
        a = (a*a) % n
        if 1 << i > e:
            break
    return res


def decode_fn(num: str, d: int, n:int) -> str:
    data_dec = fast_pow(int(num), d, n) 
    return format(data_dec, 'b').zfill(16) # chunk length from encoder!

def decode(data: str, decode_fn: Callable[[str, int, int], str], chunck_size = 16) -> str:
    with open("./d_n.txt", "r") as keys:
        lines = [line[:-1] for line in keys.readlines()]
        d, n = [int(l) for l in lines]
    chunks = data.split()
    decoded = map(decode_fn, chunks, [d]*len(chunks), [n]*len(chunks)) 
    ret = ''.join(d for d in decoded) 
    return ret

def decode_binary_string(bin_str: str) -> str:
    return ''.join(chr(int(bin_str[i*8:i*8+8],2)) for i in range(len(bin_str)//8))

def read_to_bin_str(path="../message2.txt") -> str:
    ret = ""
    with open(path, "rb") as f:
        barray = f.read()
        ret = ''.join(format(byte, '08b') for byte in barray)
    return ret

def write_output_file(string: str, path="../message3.txt"):
    with open(path, "w") as f:
        f.write(string)
    return

bin_data = read_to_bin_str()
num_data = decode_binary_string(bin_data)
decoded_bin = decode(num_data, decode_fn)
string = decode_binary_string(decoded_bin)
write_output_file(string)
