import sys
import heapq
import random    # for generating sample test case
random.seed(11)

def swap(state, row1, col1, row2, col2):
    """
    Swap the elements at positions (row1, col1) and (row2, col2) in the given state and return the new state.
    
    Args:
    - state: a tuple of tuples representing the current state of the game
    - row1, col1: the row and column indices of the first element to swap
    - row2, col2: the row and column indices of the second element to swap
    
    Returns:
    - A new tuple of tuples representing the new state after swapping the elements
    """
    state = list(map(list, state))
    state[row1][col1], state[row2][col2] = state[row2][col2], state[row1][col1]
    return tuple(map(tuple, state))

  
def h(state):
    """
    Heuristic function that estimates the minimum number of swaps required to sort 
      the fruits in each row in ascending order.
    
    Args:
    - state: a tuple of tuples representing the current state of the game
    
    Returns:
    - An integer representing the estimated number of swaps required to reach 
        the goal state from the given state
    """
    count = 0
    for row in state:
        for i in range(len(row) - 1):
            fruit, size = row[i]
            for j in range(i + 1, len(row)):
                if fruit == row[j][0] and size > row[j][1]:
                    count += 1
    return count

  
def is_goal(state):
    """
    Check if the given state is the goal state, where each row is sorted 
      in ascending order of same type of the fruit sizes.
    
    Args:
    - state: a tuple of tuples representing the current state of the game
    
    Returns:
    - A boolean indicating whether the given state is the goal state or not
    """
    for row in state:
        sizes = {}
        for fruit, size in row:
            if fruit not in sizes or sizes[fruit] <= size:
                sizes[fruit] = size
            else:
                return False
    return True


def a_star(initial_state):
    """
    Implement the A* search algorithm to find the optimal solution to the game, given the initial state.
    
    Args:
    - initial_state: a tuple of tuples representing the initial state of the game
    
    Returns:
    - A tuple (g, result_state), where g is the cost of the optimal solution and result_state is the goal state
    """
    heap = [(h(initial_state), 0, initial_state)]
    visited = set()
    while heap:
        _, g, state = heapq.heappop(heap)
        if state in visited:
            continue
        visited.add(state)
        if is_goal(state):
            return (g, state)
        n_rows, n_cols = len(state), len(state[0])
        for i1 in range(n_rows):
            for j1 in range(n_cols):
                for i2 in range(n_rows):
                    for j2 in range(n_cols):
                        if (i1 == i2 and j1 == j2) or (i1 != i2 and j1 != j2):
                            continue
                        new_state = swap(state, i1, j1, i2, j2)
                        if new_state not in visited:
                            new_g = g + 1
                            f = new_g + h(new_state)
                            heapq.heappush(heap, (f, new_g, new_state))
    return None
  
  
def main():
    
    # create state
    fruits = ['apple', 'orange', 'banana']
    size_range = range(1, 11)
    state = tuple(tuple((fruit, size) for size in size_range) for fruit in fruits)

    # randomize the state across all the rows
    all_fruits = [fruit for row in state for fruit in row]
    random.shuffle(all_fruits)
    state = tuple([tuple(all_fruits[i:i+10]) for i in range(0, 30, 10)])

    g, result_state = a_star(state)
    print("Random initial state:", state, "\n")
    print("Result state:",  result_state, "\n")
    print("Number of swaps:", g, "\n")


if __name__ == '__main__':
    main()  