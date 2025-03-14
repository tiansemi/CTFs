#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes

host = args.HOST or 'challs.actf.co'
port = int(args.PORT or 32400)

io = connect(host, port)

io.recvuntil(b"n = ")
n = int(io.recvline().strip())
io.recvuntil(b"e = ")
e = int(io.recvline().strip())
io.recvuntil(b"c = ")
c = int(io.recvline().strip())


print("n =", n)
print("e =", e)
print("c =", c)

# Get random number
r = randint(1, n)
print("r =", r)

c_blind = str((pow(r, e, n) * c) % n)
c_blind = c_blind.encode("ascii")
print(b"c_blind =", c_blind)

io.recvuntil(b"Text to decrypt:")
io.sendline(c_blind)

io.recvuntil(b"m = ")
p_blind = int(io.recvline().strip())
print(b"m = ",p_blind)

flag = (p_blind * pow(r, -1, n)) % n

print("flag =", long_to_bytes(flag))

io.close()
