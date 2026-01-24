import sys

def solve_arch_challenge(file_path):
    # 1. Définition de la correspondance des mots-clés
    mapping = {
        "arch": "+",
        "linux": "-",
        "i": ">",
        "use": "<",
        "the": "[",
        "way": "]",
        "btw": "."
    }

    # 2. Lecture et traduction du fichier
    try:
        with open(file_path, 'r') as f:
            words = f.read().split()
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' est introuvable.")
        return

    bf_code = "".join([mapping[word] for word in words if word in mapping])
    
    # 3. Interpréteur Brainfuck simple
    tape = [0] * 30000
    ptr = 0
    pc = 0  # Program counter
    output = []

    # Pré-calcul des sauts de boucles pour la performance
    stack = []
    loops = {}
    for i, char in enumerate(bf_code):
        if char == "[":
            stack.append(i)
        elif char == "]":
            start = stack.pop()
            loops[start] = i
            loops[i] = start

    # Exécution
    while pc < len(bf_code):
        cmd = bf_code[pc]
        if cmd == "+":
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == "-":
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == ">":
            ptr += 1
        elif cmd == "<":
            ptr -= 1
        elif cmd == ".":
            output.append(chr(tape[ptr]))
        elif cmd == "[":
            if tape[ptr] == 0:
                pc = loops[pc]
        elif cmd == "]":
            if tape[ptr] != 0:
                pc = loops[pc]
        pc += 1

    print("Flag décodé :", "".join(output))

if __name__ == "__main__":
    solve_arch_challenge("arch.archbtw")