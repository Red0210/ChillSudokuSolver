from z3 import *

# Crea una griglia 9x9 di variabili intere
X = [[Int(f"cell_{i}_{j}") for j in range(9)] for i in range(9)]

# Crea un solver Z3
s = Solver()

# Aggiungi il vincolo che ogni cella deve contenere un numero tra 1 e 9
for i in range(9):
    for j in range(9):
        s.add(X[i][j] >= 1, X[i][j] <= 9)

# Aggiungi il vincolo che ogni riga deve contenere numeri unici
for i in range(9):
    s.add(Distinct([X[i][j] for j in range(9)]))

# Aggiungi il vincolo che ogni colonna deve contenere numeri unici
for j in range(9):
    s.add(Distinct([X[i][j] for i in range(9)]))

# Aggiungi il vincolo che ogni sottoblocco 3x3 deve contenere numeri unici
for r in range(0, 9, 3):
    for c in range(0, 9, 3):
        s.add(Distinct([X[i][j] for i in range(r, r + 3) for j in range(c, c + 3)]))

# Definisci l'input del Sudoku (0 indica celle vuote)
input_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# Fissa i valori delle celle precompilate
for i in range(9):
    for j in range(9):
        if input_grid[i][j] != 0:
            s.add(X[i][j] == input_grid[i][j])

# Controlla se esiste una soluzione
if s.check() == sat:
    m = s.model()
    solution = [[m.evaluate(X[i][j]) for j in range(9)] for i in range(9)]
    print("Soluzione:")
    for row in solution:
        print([str(cell) for cell in row])
else:
    print("Nessuna soluzione trovata.")