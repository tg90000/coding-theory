import numpy as np
import textwrap
from typing import Callable

def read_to_bin_str(path="./data/data.txt") -> str:
    ret = ""
    with open(path, "rb") as f:
        barray = f.read()
        ret = ''.join(format(byte, '08b') for byte in barray)
    return ret

def Hamming_7_4_H(bin_str: str, data_bits = 4) -> str:
    if data_bits !=4:
        raise ValueError(f"This code has 4 data bits, got data_bits={data_bits} as parameter instead.")
    bin_str = bin_str.zfill(7)
    ret = ""
    MTX = [
        [0,1,1],
        [1,0,1],
        [1,1,0],
        [1,1,1],
        [1,0,0],
        [0,1,0],
        [0,0,1]]
    syndrome_list = MTX #  single error correcting
    word = [int(s) for s in bin_str]
    G = np.array(MTX)
    w = np.array(word).transpose()
    syn = np.remainder(w @ G, 2).tolist()
    w = w.tolist()
    if syn != [0,0,0]:
        error_index = syndrome_list.index(syn)
        w[error_index] = 1 - w[error_index]
    arr = w[0:4]
    ret = ''.join(str(i) for i in arr)
    return ret

def default_mapper(bin_str: str, data_bits) -> str:
    bin_str = bin_str.zfill(4)
    return bin_str[0:data_bits]

def decode(bin_str: str, correction_fn: Callable[[str, int], str], data_bits = 4, data_word_len = 7, do_correct = True) -> str:
    words = textwrap.wrap(bin_str, data_word_len)
    decoded = []
    if do_correct:
        decoded = map(correction_fn, words, [data_bits]*len(words))
    else:
        decoded = map(default_mapper, words, [data_bits]*len(words))
    return ''.join(d for d in decoded)



def decode_binary_string(bin_str: str) -> str:
    return ''.join(chr(int(bin_str[i*8:i*8+8],2)) for i in range(len(bin_str)//8))


def write_output_file(string: str, path="./data/decoded.txt"):
    with open(path, "w") as f:
        f.write(string)
    return

bin_data = read_to_bin_str()
decoded_data = decode(bin_data, Hamming_7_4_H, 4, 7, True)
string = decode_binary_string(decoded_data)
write_output_file(string)