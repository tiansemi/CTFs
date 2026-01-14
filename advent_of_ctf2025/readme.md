## see https://medium.com/@amreid537/cyberstudents-advent-of-ctf-2025-write-up-day-1-day-25-d472899b2fca#4197

# The Mission Begins

### Attachments : Download [start.txt](assets/start.txt)

### Writeup : Download [start.py](assets/start.py)

##### 🔍 *Étapes du décodage (pour comprendre le challenge)*

1. **Binaire → ASCII**

   * Chaque bloc de 8 bits est un caractère.
   * Le résultat était :
     `59334e6b6531637a62474d7762544e664f474644533138334d4639685a48597a546a64664d6a41794e58303d`

2. **ASCII → Hex brut**

   * La chaîne correspond en fait à du **hex**.

3. **Hex → Texte**

   * Décodé, on obtient :
     `Y3Nke1czbGMwbTNfOGFDS183MF9hZHYzTjdfMjAyNX0=`

4. **Base64 → flag final**

   * Ce qui donne :
     **`csd{W3lc0m3_8aCK_70_adv3N7_2025}`**


# The First Strike

### Attachments : Download [ftpchal.pcap](assets/ftpchal.pcap)

### Writeup : Download [ftpchal.py](assets/ftpchal.py)

##### 🔍 *Étapes (pour comprendre le challenge)*

   * Open file with Wireshark
   * Recherche google .  :
     `what is the ftp response code for user logged in`
   * Dans Wireshark filtrer "ftp.response.code == 230".
   * Click droit sur le paquet, puis follow "TCP stream" :
   * Ce qui donne :
     **`csd{Elf67_snowball}`**


# The Elf's Wager

### Attachments : Download [day4](assets/day4)

### Writeup : Download [the_Elfs_Wager.py](assets/the_Elfs_Wager.py)

##### 🔍 *Étapes (pour comprendre le challenge)*

   * Open file with radare2 :
     ```
     r2 assets/day4
     aaa
     afl
     s main
     pdd
     s fcn.00001362
     pdd
     iz | grep "!1&9s"
     px 23 @ 0x00002110
     ```
     If px 23 @ 0x00002110 showed:
     `0x402010  21 31 26 39 73 2c 36 72 5f 3a 78 6b 11 55 99 aa bb cc dd ee ff 00 11 22`
     You would replace HEXBYTES with 21312639732c36725f3a786b115599aabbccddeeff001122 and run the Python snippet which prints the flag.
   * Après les commandes `s main` et `pdd` envoyé la sortie à chatgpt pour compréhension du code. 
   * Après les commandes `s fcn.00001362` et `pdd` envoyé la sortie à chatgpt pour compréhension du code.
   * In python console  :
     ```
     b = bytes.fromhex(hexbytes)
     secret = ''.join(chr(x ^ 0x42) for x in b)
     print(secret)
     ```
   * Ce qui donne :
     **`csd{1nt0_th3_m41nfr4m3}`**


