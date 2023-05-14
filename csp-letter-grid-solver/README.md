# CSP Snake Solver 
This is the Python implementation of a CSP (Constraint Satisfaction Problem) solver for a "Snake - A through Y on a 5 x 5 grid" problem. The solver aims to fill a 5x5 grid with letters from A to Y such that each letter ahs its both adjacent letters in the neighbourhood. Basicly it allows us to traverse through A-Y via neighbors.


## Usage
To use this program, simply provide a text file containing a 5x5 grid of letters as `input.txt`. The file should contain one row of letters per line, separated by four spaces. 

For example:
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
S    T    U    V    Y
R    A    B    W    X
Q    D    C    H    I
P    E    F    G    J
O    N    M    L    K
```

## Code explanation
- `variables` is a list of tuples representing the coordinates of each variable in the 5x5 grid, i.e., [(1,1), (1,2), ..., (5,5)].
- `assigned_vars` is a list of tuples representing the coordinates of the variables assigned a value.
- `domain_values` is a dictionary mapping a variable to its domain, i.e., a list of possible values that can be assigned to it.
- `grid` is a dictionary mapping a variable to its assigned value, i.e., the letter assigned to it.

The domain values for each variable are initially set to the entire alphabet. However, when a value is assigned to a variable, the domain values of its neighbors are updated to exclude the assigned value. The `get_domain` function returns the domain of a variable by checking other variables' assigned values and removing them from the initial alphabet.

The `assign` function assigns a value to a variable and updates the domains of the neighboring variables by removing the assigned value. If a neighbor's domain becomes empty after domain reduction, the function returns False, indicating an inconsistent assignment.

The `unassign` function undoes an assignment of a variable, removes the variable from the grid, and restores the domains of the neighboring variables.

The `get_unassigned_variables` function returns a list of unassigned variables sorted by the number of unassigned neighbors (MRV).

The `backtrack` employs a backtracking search, which recursively assigns a value to an unassigned variable, performs arc consistency (AC3) to reduce the domains of the neighboring and other variables, and backtracks if an  assignment violates constraint. If all variables are assigned values without violating the constraints, the solver returns True and prints the grid. If there is no solution, the solver returns False.

`ac3` is responsible for enforcing arc consistency using ac3 algorithm. Idea is to remove the inconsistent elements from the domain of the tail if there is not at least one value left in the domain of the head which would satisfy the constraint. Constraint is that each of the adjacent letters of the given cell should be in the neighbors,so that we can traverse from A-Y only via neighbors. This function also uses `remove_inconsistent_values` function in order to remove insconsistent values from the tail of the arc.

`sort_values` function prioritizes the values which are adjacent to neighbors to selected first which makes the implementation much more optimal and effective.

`is_satisfied` checks if variables has both of its adjacent letters in the neighbourhood so that constraint is satisfied and successful.

`get_adjacent` returns adjacent(s) of the letter in a list.
