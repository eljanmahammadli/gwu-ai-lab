import sys
import heapq
import itertools
import pprint


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


def get_fruit_index(tuples, element):
    for row in range(len(tuples)):
        for col in range(len(tuples[row])):
            if tuples[row][col] == element:
                return (row, col)
    return None


def get_goal_state_idx(goals):
    all_goal_idx = []
    for idx, goal in enumerate(goals):
        idx_map = {}
        for row in range(len(goal)):
            for col in range(len(goal[row])):
                fruit = goal[row][col]
                idx_map[fruit] = get_fruit_index(goal, fruit)
        all_goal_idx.append(idx_map)
    return all_goal_idx


def make_goal_states(state):
    # create list of each different fruits
    apples = []
    bananas = []
    oranges = []

    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col][0] == 'apple':
                apples.append(state[row][col])
            elif state[row][col][0] == 'banana':
                bananas.append(state[row][col])
            else:
                oranges.append(state[row][col])
    
    # sort the values
    apples = sorted(apples, key=lambda x: x[1])
    oranges = sorted(oranges, key=lambda x: x[1])
    bananas = sorted(bananas, key=lambda x: x[1])
    
    # create 6 goal combinations
    all_fruits = [apples, bananas, oranges]
    permutations = list(itertools.permutations(all_fruits))
    goal_states = []
    for perm in permutations:
        goal_states.append(list(perm))
    
    return goal_states


def manhattan_single(state, goal_idx_map):
    heuristic = 0
    true_pos = 0
    for row in range(len(state)):
        for col in range(len(state)):
            goal_idx = goal_idx_map[state[row][col]]
            distance = abs(row - goal_idx[0]) + abs(col - goal_idx[1])
            if distance == 0:
                true_pos += 1
            heuristic += distance
    return (heuristic, true_pos)

  
def manhattan_heuristic(state, goal_idx_maps):
    """
    Heuristic function that estimates the minimum number of swaps required to sort 
      the fruits in each row in ascending order.
    
    Args:
    - state: a tuple of tuples representing the current state of the game
    
    Returns:
    - An integer representing the estimated number of swaps required to reach 
        the goal state from the given state
    """
    hs = []
    tps = []
    for goal_idx_map in goal_idx_maps:
        mh, tp = manhattan_single(state, goal_idx_map)
        hs.append(mh)
        tps.append(tp)
        
    min_hs = min(hs) # minimum heuristic
    idx = hs.index(min_hs) # index of the minimum heuristic
    ntp = tps[idx] # number of true positions
    
#     h = min_hs / 2 / (ntp+0.0001)
#     return h
    return min(hs) / 2
    
    
def is_goal(state):
    """
    Check if the given state is the goal state, where each row is sorted 
      in ascending order of same type of the fruit sizes.
    
    Args:
    - state: a tuple of tuples representing the current state of the game
    
    Returns:
    - A boolean indicating whether the given state is the goal state or not
    """
    fruit_types = [['apple'], ['banana'], ['orange']]
    size_range = range(1, len(state[0]) + 1)

    for i, row in enumerate(state):
        fruits = [fruit for fruit, _ in row]
        if list(set(fruits)) not in fruit_types:
            return False

        sizes = [size for _, size in row]
        if sizes != sorted(sizes):
            return False

    return True
    
    
def get_move_lst(state):
    move_lst = []
    n_rows, n_cols = len(state), len(state[0])

    for i1 in range(n_rows):
        for j1 in range(n_cols):
            for i2 in range(n_rows):
                for j2 in range(n_cols):
                    if (i1 == i2 and j1 == j2) or (i1 != i2 and j1 != j2):
                        move_lst.append([i1, j1, i2, j2])
                        
    return move_lst
    
  

  
def a_star(initial_state):
    """
    Implement the A* search algorithm to find the optimal solution to the game, given the initial state.
    
    Args:
    - initial_state: a tuple of tuples representing the initial state of the game
    
    Returns:
    - A tuple (g, result_state), where g is the cost of the optimal solution and result_state is the goal state
    """
  
    goals = make_goal_states(initial_state)
    goal_idx_maps = get_goal_state_idx(goals)
    move_lst = get_move_lst(initial_state)
  
    heap = [(manhattan_heuristic(initial_state, goal_idx_maps), 0, initial_state)]
    heapq.heapify(heap)
    visited = set()
    while heap:
        f, g, state = heapq.heappop(heap)
        if state in visited:
            continue
        visited.add(state)
        if is_goal(state):
            return (g, state)

        for move in move_lst:
            i1, j1, i2, j2 = move
            new_state = swap(state, i1, j1, i2, j2)
            if new_state not in visited:
                new_g = g + 1
                f = new_g + manhattan_heuristic(new_state, goal_idx_maps)
                heapq.heappush(heap, (f, new_g, new_state))
    return None
    

  
def main():
    
    state = (
      (
          ('banana', 4),
          ('orange', 7),
          ('apple', 3),
          ('apple', 4),
          ('orange', 9),
          ('apple', 6),
          ('orange', 5),
          ('apple', 8),
          ('apple', 9),
          ('apple', 10)),
      (
          ('orange', 1),
          ('banana', 1),
          ('orange', 3),
          ('orange', 4),
          ('apple', 7),
          ('orange', 6),
          ('apple', 2),
          ('orange', 8),
          ('apple', 5),
          ('orange', 10)),
      (
          ('orange', 2),  
          ('banana', 2),
          ('banana', 3),
          ('apple', 1),
          ('banana', 5),
          ('banana', 6),
          ('banana', 7),
          ('banana', 8),
          ('banana', 9),
          ('banana', 10)))

    g, result_state = a_star(state)
    print("\n\nInitial state:")
    pprint.pprint(state)
    print("\n\nResult state:")
    pprint.pprint(result_state)
    print("\n\nNumber of swaps:", g)

if __name__ == '__main__':
    main()  
