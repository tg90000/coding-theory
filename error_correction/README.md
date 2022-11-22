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
  - comment line 108-117 of `reader.py`
  - uncomment line 120-135 of `reader.py`
  - fill the parameters
  - run `python reader.py`, which now writes the decoded word to the console