# Write-up CTF : iUseArchBTW (Catégorie : Esoteric / Steganography)

## 1. Analyse Initiale

Le challenge nous fournit un fichier nommé `arch.archbtw`. La commande `file` nous indique qu'il s'agit d'un fichier texte ASCII avec de très longues lignes.

À l'ouverture du fichier, nous découvrons un texte répétitif composé uniquement de quelques mots-clés :

* `arch`
* `linux`
* `i`
* `use`
* `the`
* `way`
* `btw`

Ce comportement est typique des **langages de programmation ésotériques (Esolangs)**. Ces langages remplacent souvent les instructions classiques par des mots thématiques (ici, le "meme" bien connu de la communauté Linux).

## 2. Identification du Langage

En observant la structure, on remarque des motifs familiers pour les amateurs de CTF :

* `the` et `way` semblent encadrer un bloc (début et fin de boucle).
* `i` et `use` déplacent un pointeur.
* `arch` et `linux` incrémentent ou décrémentent une valeur.
* `btw` apparaît à la fin de certaines lignes, souvent après une série de modifications de valeurs (affichage de caractère).

Il s'agit d'une variante "Arch" du **Brainfuck**.

### Table de correspondance (Mapping)

| Mot-clé | Instruction BF | Description |
| --- | --- | --- |
| `arch` | `+` | Incrémente la cellule actuelle |
| `linux` | `-` | Décrémente la cellule actuelle |
| `i` | `>` | Déplace le pointeur vers la droite |
| `use` | `<` | Déplace le pointeur vers la gauche |
| `the` | `[` | Début de boucle (saute après `]` si la cellule est à 0) |
| `way` | `]` | Fin de boucle (retourne à `[` si la cellule n'est pas à 0) |
| `btw` | `.` | Affiche le caractère ASCII de la cellule actuelle |

## 3. Analyse de l'exécution

Le début du code fonctionne comme ceci :

1. `arch` (x6) : Met la cellule 0 à **6**.
2. `the linux i arch` (x8) `use way` : Une boucle qui décrémente la cellule 0 et incrémente la cellule 1 huit fois pour chaque unité.
* *Calcul : *


3. `i btw` : Déplace le pointeur sur la cellule 1 (valeur 48) et l'affiche.
* *Résultat : ASCII 48 = **'0'***.



Le programme continue ensuite de modifier la valeur de la cellule courante avant chaque instruction `btw` pour construire la chaîne de caractères.

## 4. Résolution Automatisée

Puisque le fichier contient des centaines d'instructions, une traduction manuelle est sujette à l'erreur. Un script Python a été utilisé pour :

1. Mapper les mots-clés vers les symboles Brainfuck.
2. Simuler une machine de Turing (ruban de mémoire et pointeur).
3. Interpréter les boucles imbriquées.

**Script utilisé :** (voir le script Python fourni précédemment).

## 5. Résultat

L'exécution du script révèle le flag final contenu dans la mémoire du programme :

**Flag :** `0xL4ugh{1_us3_4rch_l1nux_btw_4nd_y0u_sh0uld_t00_p4cm4n_r0ck5}`

---

### Conclusion

Ce challenge était une introduction ludique aux Esolangs. La principale difficulté résidait dans l'identification du mapping correct et la gestion des boucles, car une simple addition de mots par ligne n'aurait pas suffi à cause de la boucle d'initialisation au début.
