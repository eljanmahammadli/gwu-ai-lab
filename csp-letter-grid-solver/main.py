from typing import List, Tuple



def adjacent_letters_constraint(x: str, y: str) -> bool:
    """
    Returns True if x and y must be adjacent in the grid, and False otherwise.
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    adj_letters = [
        ("A", "B"), ("B", "A"), ("B", "C"), ("C", "B"), ("C", "D"), ("D", "C"),
        ("D", "E"), ("E", "D"), ("E", "F"), ("F", "E"), ("F", "G"), ("G", "F"),
        ("G", "H"), ("H", "G"), ("H", "I"), ("I", "H"), ("I", "J"), ("J", "I"),
        ("J", "K"), ("K", "J"), ("K", "L"), ("L", "K"), ("L", "M"), ("M", "L"),
        ("M", "N"), ("N", "M"), ("N", "O"), ("O", "N"), ("O", "P"), ("P", "O"),
        ("P", "Q"), ("Q", "P"), ("Q", "R"), ("R", "Q"), ("R", "S"), ("S", "R"),
        ("S", "T"), ("T", "S"), ("T", "U"), ("U", "T"), ("U", "V"), ("V", "U"),
        ("V", "W"), ("W", "V"), ("W", "X"), ("X", "W"), ("X", "Y"), ("Y", "X")
    ]
    return (x, y) in adj_letters


def get_unassigned_variables() -> List[Tuple[int, int]]:
    """
    Returns a list of unassigned variables, sorted by the number of remaining values in their domain.
    """
    unassigned_vars = [v for v in variables if v not in assigned_vars]
    return sorted(unassigned_vars, key=lambda v: len(get_domain(v)))

def get_domain(variable: Tuple[int, int]) -> List[str]:
    """
    Returns the domain of the given variable, taking into account the current assignments.
    Returns the least domain variables first.
    """
    if variable in grid:
        return [grid[variable]]
    else:
        domain = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        for neighbor in get_neighbors(variable):
            if neighbor in assigned_vars:
                domain.discard(grid[neighbor])
        return list(domain)

def get_neighbors(variable: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Returns a list of neighbors of the given variable.
    """
    row, col = variable
    neighbors = []
    if row > 1:
        neighbors.append((row - 1, col))
    if row < 5:
        neighbors.append((row + 1, col))
    if col > 1:
        neighbors.append((row, col - 1))
    if col < 5:
        neighbors.append((row, col + 1))
    return neighbors

def is_consistent(variable: Tuple[int, int], value: str) -> bool:
    """
    Returns True if the assignment of the given value to the given variable is consistent with the constraints.
    """
    if value in [i for i in grid.values()]:
        return False
    
    for neighbor in get_neighbors(variable):
        if neighbor in assigned_vars:
            if adjacent_letters_constraint(value, grid[neighbor]):
                return True
    return False
    
def assign(variable: Tuple[int, int], value: str) -> bool:
    """
    Assigns the given value to the given variable, and performs domain reduction to update the domains of the neighboring variables.
    Returns True if the assignment is consistent, and False otherwise.
    """
    grid[variable] = value
    assigned_vars.append(variable)
    for neighbor in get_neighbors(variable):
        if neighbor not in assigned_vars:
            domain = get_domain(neighbor)
            if value in domain:
                domain.remove(value)
                if len(domain) == 0:
                    # Domain wipeout, inconsistent assignment
                    return False
                domain_values[neighbor] = domain
                domain_values[variable] = [value]
    return True

  
  
def unassign(variable: Tuple[int, int]):
    """
    Unassigns the given variable, and restores the domains of the neighboring variables.
    """
    domain_values[variable] = get_domain(variable)
    
    del grid[variable]
    assigned_vars.remove(variable)
    for neighbor in get_neighbors(variable):
        if neighbor not in assigned_vars:
            domain_values[neighbor] = get_domain(neighbor)
    
def forward_check(variable: Tuple[int, int]) -> bool:
    """
    Propagates domain reduction from the given variable to its unassigned neighbors.
    Returns True if the propagation is successful (all domains are non-empty), and False otherwise.
    """
    for neighbor in get_neighbors(variable):
        if neighbor not in assigned_vars:
            domain = domain_values[neighbor]
            for value in list(domain):
                if not any(is_consistent(neighbor, v) for v in get_domain(neighbor) if v != value):
                    domain.remove(value)
            if len(domain) == 0:
                # Domain wipeout, inconsistent assignment
                return False
    return True
    

def print_grid():
    for variable in variables:
        if variable[1] == 1:
            print("\n")
        if variable in grid.keys():
            print(f" {grid[variable]} ", end="")
        else:
            print(" - ", end="")

    print("\n")
      
  
def backtrack() -> bool:
    """
    Runs the backtracking algorithm to find a solution to the word puzzle.
    Returns True if a solution is found, and False otherwise.
    """
    if len(assigned_vars) == len(variables):
        # All variables have been assigned, a solution has been found
        return True
    
    var = get_unassigned_variables()[0]
    domain = get_domain(var)
    for value in domain:
        if is_consistent(var, value):
            assign(var, value)
            if forward_check(var):
                if backtrack():
                    return True
            unassign(var)
            
    return False
  
  
def backtracking_search():
    return backtrack()


if __name__ == "__main__":

    file_path = "input.txt"
    grid = {}
    with open(file_path) as f:
        for row_idx, line in enumerate(f):
            for col_idx, char in enumerate(line.strip().split()):
                if char != "-":
                    grid[(row_idx+1, col_idx+1)] = char


    variables = [(i, j) for i in range(1, 6) for j in range(1, 6)]
    assigned_vars = [i for i in grid.keys()]
    domain_values = {v: get_domain(v) for v in variables}


    if backtracking_search():
        print(grid)
        print_grid()
        print()
    else:
        print("No solution found.")