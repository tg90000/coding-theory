import numpy as np
from math import floor
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

def gen_syndromes(H: list[list[int]], list_all_h: list[list[int]], zn) -> list[list[int]]:
    ret = [np.remainder(np.array(h) @ np.array(H), zn).tolist() for h in list_all_h]
    return ret

def checker_from_generator(MTX: list[list[int]], zn: int) -> list[list[int]]:
    dim = len(MTX) # rows
    dim2 = len(MTX[0]) # cols
    # (E G)
    MTX = np.array(MTX)
    G = MTX[0:, dim:] # assuming C is systematic
    H_up = np.remainder(-1*G, zn) # 
    H = np.block([[H_up], [np.eye(dim2-dim)]]) # (-G // E)
    return H

def Hamming_H(bin_str: str, data_bits: int, zn: int, H: list[list[int]], h_dict: dict[str, list[int]]) -> str:
    code_len = len(H) # rows
    bin_str = bin_str.zfill(code_len) # len of code words
    ret = ""
    word = [int(s) for s in bin_str]
    H = np.array(H)
    w = np.array(word).transpose()
    syn = np.remainder(w @ H, zn).tolist()
    syn = [floor(bit) for bit in syn]
    w = w.tolist()
    if syn != [0]*(code_len-data_bits):
        syn_str = ''.join(str(floor(bit)) for bit in syn)
        h = h_dict[syn_str]
        h = [floor(bit) for bit in h] 
        w = [((ui - vi)%zn) for (ui, vi) in zip(w, h)] # w - syndrome_list[error_index]
    arr = w[0:data_bits] # systematic code
    ret = ''.join(str(i) for i in arr)
    return ret

def Hamming_7_4_H(bin_str: str, data_bits = 4, zn=2, G = None) -> str: # example code
    if data_bits !=4:
        raise ValueError(f"This code has 4 data bits, got data_bits={data_bits} as parameter instead.")
    bin_str = bin_str.zfill(7)
    ret = ""
    G = [[1,0,0,0,0,1,1],
    [0,1,0,0,1,0,1],
    [0,0,1,0,1,1,0],
    [0,0,0,1,1,1,1]]
    H = checker_from_generator(G, zn)
    syndrome_list = gen_syndromes(H, 1, 2) # MTX #  single error correcting
    word = [int(s) for s in bin_str]
    G = np.array(H)
    w = np.array(word).transpose()
    syn = np.remainder(w @ G, 2).tolist()
    w = w.tolist()
    if syn != [0,0,0]:
        error_index = syndrome_list.index(syn)
        w[error_index] = 1 - w[error_index]
    arr = w[0:4]
    ret = ''.join(str(i) for i in arr)
    return ret

def default_mapper(bin_str: str, data_bits: int) -> str:
    bin_str = bin_str.zfill(4)
    return bin_str[0:data_bits]

def decode(bin_str: str, correction_fn: Callable[[str, int], str] = default_mapper, G: list[list[int]] = None, data_bits = 4, data_word_len = 7, zn = 2, error_num = 1, do_correct = True) -> str:
    words = textwrap.wrap(bin_str, data_word_len)
    decoded = []
    num_w = len(words)
    H = checker_from_generator(G, zn)
    dimC = len(H)
    list_all_h = [h for err in range(error_num) for h in gen_h_rec(dimC, err+1, zn)]
    syndrome_list = gen_syndromes(H, list_all_h, zn) 
    syndrome_strings = [''.join(str(floor(bit)) for bit in syndrome) for syndrome in syndrome_list]
    correction_dict = dict(zip(syndrome_strings, list_all_h))
    if do_correct:
        decoded = map(correction_fn, words, [data_bits]*num_w, [zn]*num_w, [H]*num_w, [correction_dict]*num_w)
    else:
        decoded = map(default_mapper, words, [data_bits]*num_w)
    return ''.join(d for d in decoded)

def decode_binary_string(bin_str: str) -> str:
    return ''.join(chr(int(bin_str[i*8:i*8+8],2)) for i in range(len(bin_str)//8))

def write_output_file(string: str, path="./data/decoded.txt"):
    with open(path, "w") as f:
        f.write(string[:-1] + '\n')
    return

# Example with encoder: The (4,7) Hamming code from the lecture notes
bin_data = read_to_bin_str()
G = [[1,0,0,0,0,1,1],
[0,1,0,0,1,0,1],
[0,0,1,0,1,1,0],
[0,0,0,1,1,1,1]]
decoded_data = decode(bin_data, Hamming_H, G, 4, 7, 2, 1, True) # Use (4,7) Hamming code with generator defined above.
# decoded_data = decode(bin_str = bin_data, do_correct = False) # without correction for reference
string = decode_binary_string(decoded_data)
write_output_file(string)


# Example for Z3, data bits = 2, code length = 4, errors = 1
# original_word = "12"                      # (u), the original word
# encoded_word = "1201"                     # (uG), the enocoded word
# err_word = "1001"                         # one bit error, on the second bit
# test_generator = [[1,0,2,2], [0,1,2,1]]   # the generator matrix
# decoded_word = decode(
#     bin_str=err_word,                     # word with errors
#     correction_fn=Hamming_H,              # decoder function
#     G = test_generator,                   # generator matrix
#     data_bits=2,                          # original word length
#     data_word_len = 4,                    # code length
#     zn=3,                                 # the modulus p of the field Zp
#     error_num = 1                         # error correcting capability of the code
#     )
# print(decoded_word)