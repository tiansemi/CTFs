#!/usr/bin/python

with open("start.txt","r") as f :
	data=f.read()

s = ''.join(chr(int(b,2)) for b in data.split())
hexDecode=bytes.fromhex(s)
print(hexDecode)

import base64
decode64=base64.b64decode(hexDecode)
print(decode64)