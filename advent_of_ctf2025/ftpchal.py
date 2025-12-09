#!/usr/bin/python

data = open('./ftpchal.pcap','rb').read()
import re
# find all server responses containing 230
resp = [(m.start(), m.group()) for m in re.finditer(b'230 [^\r\n]*', data)]
print(resp, len(resp))
# find all commands positions
cmds=[]
for m in re.finditer(b'(USER|PASS) ([^\r\n]+)', data):
    cmds.append((m.start(), m.group()))
# find last before resp
target=resp[0][0]
sel=[c for c in cmds if c[0]<target]
print(sel[-1:])
sel=sel[-2:]
print(f"csd{{{sel[0][1].split()[1].decode()}_{sel[1][1].split()[1].decode()}}}")
