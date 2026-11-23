from z3 import *

# 9x9 matrix of integer variables
X = [[ Int("x_%d_%d" % (i, j)) for j in range(9) ]
      for i in range(9) ]


# each cell contains a value in {1, ..., 9}
cells  = [ And(1 <= X[i][j], X[i][j] <= 9)
             for i in range(9) for j in range(9) ]

# each row contains a digit at most once
rows   = [ Distinct(X[i]) for i in range(9) ]

# each column contains a digit at most once
cols   = [ Distinct([ X[i][j] for i in range(9) ])
             for j in range(9) ]

# each 3x3 square contains a digit at most once
sq     = [ Distinct([X[i][j]
                        for i in range(3*r, 3*r+3) for j in range(3*c, 3*c+3) ])
             for r in range(3) for c in range(3) ]

sudoku_c = cells + rows + cols + sq

# sudoku instance, '0' for empty cells
# Funzione per leggere l'input dell'utente dalla console
def read_sudoku_from_console():
    print("Inserisci il Sudoku riga per riga. Usa 0 per le celle vuote.")
    print("Separare i numeri con spazi. Ad esempio: '1 0 0 0 7 0 0 2 0'")
    instance = []
    for i in range(9):
        while True:
            try:
                row = input(f"Inserisci la riga {i+1}: ")
                row_values = list(map(int, row.strip().split()))
                if len(row_values) != 9 or any(not (0 <= x <= 9) for x in row_values):
                    raise ValueError
                instance.append(row_values)
                break
            except ValueError:
                print("Input non valido. Assicurati di inserire 9 numeri tra 0 e 9.")
    return instance

# Leggi l'input dall'utente
instance = read_sudoku_from_console()



instance_c = [ If(instance[i][j] == 0,
                  True,
                  X[i][j] == instance[i][j])
               for i in range(9) for j in range(9) ]

# definition of output matrix
def print_matrix(matrix):
    for i, row in enumerate(matrix):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # orizzontal separators every 3 lines

        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  # vertical separators every 3 columns
            print(val, end=" ")
        
        print()  # new line at the end of each line

# solve the sudoku and return the solution
s = Solver()
s.add(sudoku_c + instance_c)
if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(9) ]
          for i in range(9) ]
    print_matrix(r)
else:
    print ("failed to solve")