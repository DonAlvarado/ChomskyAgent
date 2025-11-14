import random


# REGLAS POR CATEGORÍA

def gen_type3():
    V = ["S", "A", "B"]
    T = ["a", "b"]

    prods = {
        "S": [],
        "A": [],
        "B": [],
    }

    # Construir reglas regulares
    for A in V:
        # Terminal solo
        prods[A].append(random.choice(T))

        # Terminal + Variable
        prods[A].append(random.choice(T) + random.choice(V))

        # A veces epsilon
        if random.random() < 0.3:
            prods[A].append("ε")

    return prods


def gen_type2():
    V = ["S", "A", "B"]
    T = ["a", "b", "c"]

    prods = {
        "S": [],
        "A": [],
        "B": [],
    }

    # producir algo como S -> aAb | AB | Ba
    shapes = [
        "aA", "Aa", "AB", "BA", "aAB", "ABa", "aBA",
        "AaB", "BAa"
    ]

    for A in V:
        rhs = random.choice(shapes)
        prods[A].append(rhs)

        # producciones simples
        prods[A].append(random.choice(T))
        prods[A].append(random.choice(T) + random.choice(V))

    return prods


def gen_type1():
    V = ["S", "A", "B", "C"]
    T = ["a", "b", "c"]
    
    prods = {}

    # reglas contextuales
    left_shapes = [
        "AB", "BC", "CA", "AS", "SB", "BA"
    ]

    for i in range(random.randint(2, 4)):
        left = random.choice(left_shapes)

        size = random.randint(len(left), len(left) + 2)
        rhs = ""

        for _ in range(size):
            rhs += random.choice(V + T)

        prods[left] = [rhs]

    # S produce algo para iniciar
    prods["S"] = [random.choice(T) + "A"]

    return prods


def gen_type0():
    V = ["S", "A", "B", "C", "D"]
    T = ["a", "b", "c", "0", "1"]

    prods = {}

    lhs_options = V + ["AB", "BC", "CD", "DA"]
    rhs_symbols = V + T

    for i in range(random.randint(3, 6)):
        left = random.choice(lhs_options)
        size = random.randint(0, 4)
        rhs = "".join(random.choice(rhs_symbols) for _ in range(size)) or "ε"
        if left not in prods:
            prods[left] = []
        prods[left].append(rhs)

    return prods

# GENERADOR PRINCIPAL

def generate(grammar_type: str):
    if grammar_type == "regular":
        return {"productions": gen_type3(), "type": "Tipo 3"}

    if grammar_type == "cfl":
        return {"productions": gen_type2(), "type": "Tipo 2"}

    if grammar_type == "context":
        return {"productions": gen_type1(), "type": "Tipo 1"}

    if grammar_type == "irrestrict":
        return {"productions": gen_type0(), "type": "Tipo 0"}

    raise ValueError("Tipo inválido para generator")
