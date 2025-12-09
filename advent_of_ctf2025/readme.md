# The Mission Begins

### Attachments : Download [start.txt](./start.txt)

### Writeup : Download [start.py](./start.py)

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
