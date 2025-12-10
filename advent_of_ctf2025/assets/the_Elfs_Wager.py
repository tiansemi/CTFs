#!/usr/bin/python

hexbytes = "21312639732c36721d362a711d2f76732c2430762f713f" 
b = bytes.fromhex(hexbytes)
secret = ''.join(chr(x ^ 0x42) for x in b)
print(secret)
