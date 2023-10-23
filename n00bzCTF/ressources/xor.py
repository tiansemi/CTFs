#!/usr/bin/env python3

def xor_encrypt_decrypt(plaintext, key):
    ciphertext = bytearray()
    for i in range(len(plaintext)):
        ciphertext.append(plaintext[i] ^ key[i % len(key)])
    return ciphertext

plaintext = b"7_E!\x1b\x15 U)U\x1cp>\x17W\x06\x15\\\x1b\rp\x1fV~\x14=[sT_\x00RZ:\x1cs\x15+P\x1ey\x017$t'+~\x1d_Fb\x1c"
key = b'YouCanNeverCatchJohnDoe!'
ciphertext = xor_encrypt_decrypt(plaintext, key)
print(ciphertext.decode('utf-8'))