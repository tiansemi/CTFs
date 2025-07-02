@site : http://ctf-spcs.mf.grsu.by/
@author : Moulo

# Homomorphic weak - crypto / misc
> The server uses a strong homomorphic cryptosystem, but the key generation module is too weak. Take advantage of this and decrypt the flag.
> nc ctf.mf.grsu.by 9055
> 
> Downloads : chall_9055.py
> 
## Solution : 
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import remote
from math import gcd, isqrt
from Crypto.Util.number import long_to_bytes

def lcm(a, b):
    return a // gcd(a, b) * b

def factor_n_small_diff(n, max_diff=10_000):
    """
    Recherche p,q tels que n = p*q et q-p <= max_diff
    Retourne (p,q) ou lève ValueError.
    """
    for d in range(1, max_diff + 1):
        D = d*d + 4*n
        s = isqrt(D)
        if s*s == D:
            p = (s - d) // 2
            q = p + d
            if p * q == n:
                return p, q
    raise ValueError("Échec de factorisation dans la borne donnée")

def paillier_decrypt(n, c, p, q):
    """
    Décrypte c sous Paillier avec g = n+1.
    """
    # 1) λ = lcm(p-1, q-1)
    lam = lcm(p-1, q-1)
    # 2) µ = (L(g^λ mod n^2))^{-1} mod n
    #    avec g = n+1 => L(g^λ) ≡ λ mod n  => µ = λ^{-1} mod n
    mu = pow(lam, -1, n)
    # 3) u = c^λ mod n^2
    n2 = n * n
    u = pow(c, lam, n2)
    # 4) m = L(u) * μ mod n, L(u) = (u-1)//n
    m = ((u - 1) // n) * mu % n
    # 5) conversion en bytes
    return long_to_bytes(m)

def main():
    # 1) Connexion au service
    conn = remote("ctf.mf.grsu.by", 9055)
    # 2) Lecture des lignes contenant n, g, c
    #    Format attendu :
    #       n = ...
    #       g = ...
    #       c = ...
    lines = []
    while len(lines) < 3:
        line = conn.recvline().decode().strip()
        if line.startswith("n =") or line.startswith("g =") or line.startswith("c ="):
            lines.append(line)
            print(line)
    # 3) Extraction des valeurs
    n = int(lines[0].split("=",1)[1].strip())
    g = int(lines[1].split("=",1)[1].strip())
    c = int(lines[2].split("=",1)[1].strip())

    # 4) Factorisation
    p, q = factor_n_small_diff(n)
    print(f"[+] p = {p}")
    print(f"[+] q = {q}")

    # 5) Déchiffrement
    flag = paillier_decrypt(n, c, p, q)
    print(f"[+] Décrypté : {flag!r}")

    # 6) Envoi du flag (sans saut de ligne supplémentaire)
    conn.sendline(flag)
    # Lecture de la réponse finale
    print(conn.recvall(timeout=2).decode())

if __name__ == "__main__":
    main()
```

# Homomorphic Fraud - crypto / misc

> You have found a bank server that stores customer balances encrypted (using the Paillier scheme). The server allows you to: view the encrypted customer balance and increase the balance. But there is a problem: the server does not check what number you "add" to the balance!
> Can you increase the balance to $1,000,000 without knowing the bank's secret key?
> nc ctf.mf.grsu.by 9054
> 
> Downloads : Paillier9054.py
> 

## Solution : 
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import remote
from Crypto.Util.number import inverse

def main():
    # 1) Connexion au service
    conn = remote("ctf.mf.grsu.by", 9054)

    # 2) Récupérer n, g et l'enc_balance envoyé par le serveur
    # Format attendu :
    #   [*] Public Key (n, g) = (n, g)
    #   [*] Encrypted Balance = enc_balance
    line = conn.recvline_contains(b"Public Key")
    # la ligne contient "(n, g) = (… , …)"
    parts = line.decode().split("=",1)[1].strip()
    # retire les parenthèses et sépare n et g
    n_str, g_str = parts.strip("() ").split(",")
    n = int(n_str)
    g = int(g_str)

    # lire la ligne de l’encrypted balance
    line = conn.recvline_contains(b"Encrypted Balance")
    enc_balance = int(line.decode().split("=",1)[1].strip())

    # 3) Construire l’enc_amount qui transformera enc_balance en encrypt(1e6)
    n2 = n * n
    target = 1_000_000

    # g = n+1, donc encrypt(target, r=1) = g^target mod n^2
    encrypt_target_r1 = pow(g, target, n2)

    # on veut : enc_balance * enc_amount ≡ encrypt_target_r1  mod n^2
    # donc  enc_amount ≡ encrypt_target_r1 * inv(enc_balance) mod n^2
    inv_balance = inverse(enc_balance, n2)
    enc_amount = (encrypt_target_r1 * inv_balance) % n2

    # 4) Envoyer notre "Enc(amount)"
    conn.sendline(str(enc_amount).encode())

    # 5) Lire la réponse
    resp = conn.recvall(timeout=2).decode()
    print(resp)

if __name__ == "__main__":
    main()
```

# ZKP 9+ - Misc / ZKP
Using the Schnorr scheme for a zero-knowledge proof protocol (ZKP), prove that you can find the discrete logarithm without revealing the secret of how you do it.

You are the Prover, the server is the Verifier. You are given a prime number p, a generator g of the multiplicative group Zp*, a value y = gx mod p. Prove by answering the server's questions that you know x.

nc ctf.mf.grsu.by 9049
Downloads : zkp9049.py

## Solution
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pwn import remote
from math import prod

def solve():
    # 1) Connexion
    conn = remote("ctf.mf.grsu.by", 9049)

    # 2) Read and parse the parameters
    # We'll read until we see the line "Parameters: p=..., g=..., y=..."
    line = conn.recvline_contains(b"Parameters")
    # Example: "Parameters: p=23, g=5, y=8"
    part = line.decode().split(":",1)[1]
    p_str, g_str, y_str = part.strip().split(",")
    p = int(p_str.split("=")[1])
    g = int(g_str.split("=")[1])
    y = int(y_str.split("=")[1])
    print(f"[+] Got p={p}, g={g}, y={y}")

    # 3) Compute x = log_g(y) mod p by brute force
    x = next(i for i in range(1, p-1) if pow(g, i, p) == y)
    print(f"[+] Discrete log found: x = {x}")

    # 4) Play ROUNDS rounds
    # The server says "Rounds: 3" before the loop, but we can just loop 3 times.
    for round_num in range(1, 4):
        # read the "=== Round i ===" prompt
        conn.recvuntil(f"=== Round {round_num}".encode())

        # a) prover chooses r and sends C = g^r mod p
        r = rand = __import__("random").randint(1, p-2)
        C = pow(g, r, p)
        conn.sendline(str(C).encode())
        print(f"[Round {round_num}] Sent C = {C}")

        # b) read the challenge
        line = conn.recvline_contains(b"Challenge e =")
        e = int(line.decode().split("=")[1].strip())
        print(f"[Round {round_num}] Got e = {e}")

        # c) compute and send s = r + e*x mod (p-1)
        s = (r + e * x) % (p - 1)
        conn.sendline(str(s).encode())
        print(f"[Round {round_num}] Sent s = {s}")

        # d) read verification result
        resp = conn.recvline().decode().strip()
        print(f"[Round {round_num}] {resp}")

        if "Verification failed" in resp:
            print("[-] Failed to convince the verifier.")
            return

    # 5) Finally, read the flag
    flag_line = conn.recvline_contains(b"Flag:")
    print(flag_line.decode().strip())

if __name__ == "__main__":
    solve()

```

# Error, another error ...  Misc / Crypto / Coding
My smart server stopped correcting data errors. Although before it could find a bad bit in a 7-bit block. Help!
nc ctf.mf.grsu.by 9057

Downloads : chall_9057.py

## Solution
```

```

# 

## Solution
```

```

# 

## Solution
```

```

# 

## Solution
```

```

# 

## Solution
```

```

# 

## Solution
```

```

# 

## Solution
```

```

# 

## Solution
```

```
