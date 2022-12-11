# Error correcting codes implementation
Toy code, assignment for Coding Theory class

### For demo, on a (4,7) Hamming code:
Requres Python 3.9 or later.
  - Fill up text.txt with some ascii text
  - run `python writer.py` that encodes it to binary
  - run `python noise_generator.py` that induces errors, maximum 1 per code word
  - run `python reader.py` that decodes text to decoded.txt
      - you can decode without error correction by swapping comments before line 114 and 115 of `reader.py`

### For assignment purposes:
  - Fill up text_one.txt with a single code word
  - run `python writer.py <param>`, this outputs data_one.txt as data word
  - run `python noise_generator.py <param>`, this outputs data_one.txt with error(s)
  - run `python reader.py <param>`, this outputs decoded_one.txt with the corrected codeword, same as text_one.txt
  - the example `<param>` can be:
    - test1 for a length 4 Hamming code over Z3
    - test2 for a length 24 extended binary Golay code
    - the generator matrices and fields can be changed in the code, the two above are just examples