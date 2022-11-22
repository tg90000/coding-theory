import numpy as np
import textwrap
from typing import Callable

def read_to_bin_str(path="./data/data.txt") -> str:
    ret = ""
    with open(path, "rb") as f:
        barray = f.read()
        ret = ''.join(format(byte, '08b') for byte in barray)
    return ret

def gen_h_rec(dim: int, err_num: int, zn: int, err_num_iter: int = 1, acc_h_vec: list[int] = None, startindex: int = 0, ret_collection: list[list[int]] = []) -> list[list[int]]:
    for i in range(startindex, dim):
        for j in range(1,zn):
            h = [0] * dim if not acc_h_vec else acc_h_vec.copy()
            h[i] = j
            if err_num_iter == err_num:
                ret_collection.append(h)
            else:
                ret_collection.extend(gen_h_rec(dim, err_num, zn, err_num_iter+1, h, i+1, []))
    return ret_collection

def gen_syndromes(H: list[list[int]], err_num: int, zn: int) -> list[list[int]]:
    dimC = len(H) # cols, len of w
    list_all_h = [h for err in range(err_num) for h in gen_h_rec(dimC, err+1, zn)]
    list_all_h = [(np.array(h)).transpose() for h in list_all_h]
    ret = [np.remainder(h @ np.array(H), zn).tolist() for h in list_all_h]
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
    syndrome_list = gen_syndromes(MTX, 1, 2) # MTX #  single error correcting
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