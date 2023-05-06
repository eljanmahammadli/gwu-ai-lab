# CSP Snake Solver 
This is the Python implementation of a CSP (Constraint Satisfaction Problem) solver for a "Snake - A through Y on a 5 x 5 grid" problem. The solver aims to fill a 5x5 grid with letters from A to Y such that each letter is adjacent to another in the grid.


## Usage
To use this program, simply provide a text file containing a 5x5 grid of letters as `input.txt`. The file should contain one row of letters per line, separated by four spaces. For example:

```txt
-    -    -    -    Y
R    A    -    -    -
-    -    -    -    -
-    E    -    -    -
-    -    -    -    K
```
Then, run the `main.py` script.
```bash
python3 main.py
```

The output will be printed to the console:

```txt
Q    P    O    X    Y 
R    A    B    W    V 
S    F    G    H    I 
T    E    D    C    J 
U    N    M    L    K 
```


## Code explanation
- `variables` is a list of tuples representing the coordinates of each variable in the 5x5 grid, i.e., [(1,1), (1,2), ..., (5,5)].
- `assigned_vars` is a list of tuples representing the coordinates of the variables assigned a value.
- `domain_values` is a dictionary mapping a variable to its domain, i.e., a list of possible values that can be assigned to it.
- `grid` is a dictionary mapping a variable to its assigned value, i.e., the letter assigned to it.

The domain values for each variable are initially set to the entire alphabet. However, when a value is assigned to a variable, the domain values of its neighbors are updated to exclude the assigned value. The `get_domain` function returns the domain of a variable by checking its neighbors' assigned values and removing them from the initial alphabet.

The `is_consistent` function checks if an assignment of a value to a variable is consistent with the current grid, i.e., the value is not already in the grid, and it does not violate the constraint that adjacent letters must be adjacent in the grid.

The `assign` function assigns a value to a variable and updates the domains of the neighboring variables by removing the assigned value. If a neighbor's domain becomes empty after domain reduction, the function returns False, indicating an inconsistent assignment.

The `unassign` function undoes an assignment of a variable, removes the variable from the grid, and restores the domains of the neighboring variables.

The `forward_check` function propagates domain reduction from the given variable to its unassigned neighbors. It removes any value from a neighbor's domain if it cannot be assigned to the neighbor without violating the constraint that adjacent letters must be adjacent in the grid. If a neighbor's domain becomes empty after domain reduction, the function returns False, indicating an inconsistent assignment.

The `get_unassigned_variables` function returns a list of unassigned variables sorted by the number of remaining values in their domain (MRV).

The `backtrack` employs a backtracking search, which recursively assigns a value to an unassigned variable, performs forward checking to reduce the domains of the neighboring variables, and backtracks if an inconsistent assignment is detected. If all variables are assigned values without violating the constraints, the solver returns True and prints the grid. If there is no solution, the solver returns False.
