from typing import List, Tuple
import heapq

# import helper functions
from helpers import get_adjacent, get_grid, print_grid
  

def get_unassigned_variables() -> List[Tuple[int, int]]:
    """
    Returns a list of unassigned variables, sorted by the number of remaining values in their domain.
    """
    unassigned_vars = [v for v in variables if v not in assigned_vars]
    return sorted(unassigned_vars, key=lambda v: len([n for n in get_neighbors(v) if n not in assigned_vars]))
  

def get_domain(variable: Tuple[int, int]) -> List[str]:
    """
    Returns the domain of the given variable, taking into account the current assignments.
    Returns the least domain variables first.
    """
    if variable in grid:
        return [grid[variable]]
    else:
        domain = set("ABCDEFGHIJKLMNOPQRSTUVWXY")
        for var in assigned_vars:
            domain.discard(grid[var])
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
  
  
def is_satisfied(variable: Tuple[int, int]) -> bool:
    """This function checks if variables has both of its adjacent letters in the neighbourhood"""
    if variable in assigned_vars:
        adjacents = get_adjacent(grid[variable])
        n_letters = [grid[n] if n in assigned_vars else None for n in get_neighbors(variable)]
        if len(list(set(adjacents) - set(n_letters))) == 0:
            return True
    return False
  

def is_complete():
    if len(assigned_vars) != len(variables):
        return False
    for var in variables:
        if not is_satisfied(var):
            return False
    return True
  

def assign(variable: Tuple[int, int], value: str) -> bool:
    """
    Assigns the given value to the given variable, and performs domain reduction to update the domains of the neighboring variables.
    Returns True if the assignment is consistent, and False otherwise.
    """
    grid[variable] = value
    assigned_vars.append(variable)
    domain_values[variable] = [value]
    return True

  
def unassign(variable: Tuple[int, int]):
    """
    Unassigns the given variable, and restores the domains of the neighboring variables.
    """
    del grid[variable]
    assigned_vars.remove(variable)
    for v in variables:
        domain_values[v] = get_domain(v)
        
        
def sort_values(variable):
    """Prioritizing the values which are adjacent to neighbors"""
    domain = domain_values[variable]
    
    n_values = [grid[n] for n in get_neighbors(variable) if n in assigned_vars]
    var_values = []
    for v in n_values:
        var_values.extend(get_adjacent(v))
        
    for value in var_values:
        if value in domain:
            domain.remove(value)
            domain.insert(0, value)

    return domain
  
  
def ac3():
    """
    Enforcing arc consistency using ac3 algorithm
    Idea is to remove the inconsistent elements from the domain of the tail if there is not 
      at least one value left in the domain of the head which would satisfy the constraint.
      
    Constraint is that each of the adjacent letters of the given cell should be in the neighbors,
      so that we can traverse from A-Y only via neighbors.
    
    """
    heap = []
    counter = 0
    for variable in variables:
        for neighbor in get_neighbors(variable):
            heap.append((counter, variable, neighbor))
              
    heapq.heapify(heap)
    while heap:
        arc = heapq.heappop(heap)
        if remove_inconsistent_values(arc):
            for variable in variables:
                new_arc = (counter, variable, arc[1])
                if new_arc not in heap:
                    heapq.heappush(heap, new_arc)
                    

def remove_inconsistent_values(arc):
    removed = False
    
    # if the head is satisfied then no need to remove values from tail
    if is_satisfied(arc[2]):
        return removed
    
    removed_values = []
    for value in domain_values[arc[1]]:
        grid_copy = grid.copy()
        grid_copy[arc[1]] = value
        assigned_vars_copy = assigned_vars.copy()
        assigned_vars_copy.append(arc[1])
        
        if arc[2] in assigned_vars_copy:
            neighbors = get_neighbors(arc[2])
            n_letters = [grid_copy[n] if n in assigned_vars_copy else None for n in neighbors]
            unassigned_count = n_letters.count(None)
            adjacents = get_adjacent(grid_copy[arc[2]])
            l = list(set(adjacents) - set(n_letters))

            if unassigned_count < len(l):
                removed_values.append(value)
                removed = True

    for value in removed_values:
        domain_values[arc[1]].remove(value)

    return removed
      
  
def backtrack() -> bool:
    """
    Runs the backtracking algorithm to find a solution to the grid world.
    Returns True if a solution is found, and False otherwise.
    """
    if is_complete():
        return True
    
    var = get_unassigned_variables()[0] # MRV
    ac3() # enforce the arc consistency
    domain = sort_values(var) # sort the values
    for value in domain:
        assign(var, value)
        result  = backtrack()
        if result:
            return True
        unassign(var)            
    return False
  
  
def backtracking_search():
    return backtrack()
  
if __name__ == "__main__":

    # get the input grid
    grid = get_grid("input.txt")

    # initialie variables, assigned variables and domain of them
    variables = [(i, j) for i in range(1, 6) for j in range(1, 6)]
    assigned_vars = [i for i in grid.keys()]
    domain_values = {v: get_domain(v) for v in variables}


    if backtracking_search():
        print(grid)
        print_grid(variables, grid)
    else:
        print("No solution found.")
