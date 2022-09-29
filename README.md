# RSA implementation
Toy code, assignment for Coding Theory class

### Requirements:
  - python3: numpy
  - C: gmp.h : Gnu MultiPrecision Library

### Example run:
  1. Generate keys in ./keygen/ :
     1. set params in keygen.c
     1. `gcc -o keygen keygen.c`
     1. `./keygen`
  1. Prepare message in ./ :
     1. edit message.txt (only alphanumeric rn)
  1. Encode the message in ./encoder/
     1. `python3 encode.py`
     1. check encoded string in ./message2.txt
  1. Decode from ./decoder/
     1. `python3 decode.py`
     1. check decoded message string in ./message3.txt


### Example for big numbers:
  1. Generate keys in ./keygen/ :
     1. set params in keygen.c
     1. `gcc -o keygen_big keygen_big.c -lgmp; ./keygen_big` (needs gmp.h)
     1. `./keygen_big`
  1. Prepare message in ./ :
     1. edit message.txt (only alphanumeric rn)
  1. Encode the message in ./encoder/
     1. `python3 encode.py`
     1. check encoded string in ./message2.txt
  1. Decode from ./decoder/
     1. `python3 decode.py`
     1. check decoded message string in ./message3.txt


