def get_adjacent(letter):
    """Returns adjacent(s) of the letter in a list"""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXY'
    if letter == 'A':
        return [alphabet[1]]
    elif letter == 'Y':
        return [alphabet[-2]]
    else:
        idx = alphabet.index(letter)
        return [alphabet[idx-1], alphabet[idx+1]]
    

def get_grid(file_path):
    grid = {}
    with open(file_path) as f:
        for row_idx, line in enumerate(f):
            for col_idx, char in enumerate(line.strip().split()):
                if char != "-":
                    grid[(row_idx+1, col_idx+1)] = char
    return grid


def print_grid(variables, grid):
    """Helper function to print the grid"""
    for variable in variables:
        if variable[1] == 1:
            print("\n")
        if variable in grid.keys():
            if variable[1] == 1:
                print(f"{grid[variable]}  ", end="")
            elif variable[1] == 5:
                print(f"  {grid[variable]}", end="")
            else:
                print(f"  {grid[variable]}  ", end="")
                
        else:
            print(" - ", end="")
    print("\n")
