import sys
import heapq
import numpy as np

class State:
    """Object to define the states
    
    Args:
      volumes (list(int)): amount of water in each pitcher
      _prev (State): mother state
    """
    def __init__(self, volumes, _prev=None):
        self.volumes = volumes
        self.g = 0
        self.h = 0
        self.f = 0
        self._prev = _prev
    
    # Comparision operation for choosing the state with least A* score 
    def __lt__(self, other):
        return self.f < other.f
    
    # Testing if the current state is the goal
    def __eq__(self, other):
        return self.volumes[0] == other
    
    # String representation for distinguishing the states
    def __str__(self):
        return f"volumes={self.volumes}"
    
    def __repr__(self):
        return f"State(volumes={self.volumes}, g={self.g}, h={self.h}, f={self.f})"

# Generating all the possible next states
def get_next_states(state, capacities):
    """ Generates all the possible next states
    
        Args:
          state (State): current state.
          capacities (list): given total volumes of pitchers.
          
        Returns:
          next_states (list(State)): all possible next states to visit.
            Initially attributes except volumes are zero. And one exception is 
            not to fully fill the inifinte pitcher when its volume is zero. 
    """
    
    next_states = []
    for i in range(len(capacities)):
        for j in range(len(capacities)):
            if i == j:
                continue
            next_volumes = state.volumes[:]
            if next_volumes[i] + next_volumes[j] <= capacities[j]:
                next_volumes[j] += next_volumes[i]
                next_volumes[i] = 0
            else:
                diff = capacities[j] - next_volumes[j]
                next_volumes[j] = capacities[j]
                next_volumes[i] -= diff
            if (str(State(next_volumes)) not in [str(h) for h in next_states]) and (str(State(next_volumes)) != str(state)):
                next_states.append(State(next_volumes))
    for i in range(1, len(capacities)):
        next_volumes = state.volumes[:]
        if next_volumes[i] == capacities[i]:
            continue
        next_volumes[i] = capacities[i]
        next_states.append(State(next_volumes))
    return next_states

# Heuristic function to estimate the distance from 
  # current state to goal state
def heuristic(state, target_volume):
    """Function to calculate the heuristics
    
       Args:
         state (State): current state.
         target_volume (int): the goal amount of water to be in infinite pitcher.
         
       Returns:
         h_tot (float): estimated heuristic value which is mean of two different
           heruistics. First being the absolute difference between sum of all
           volumes in all the pitcher and goal state; and the second is the
           absolute difference between infinite pitcher and goal state.
    """
    h1 = abs(sum(state.volumes) - target_volume)
    h2 = abs(state.volumes[0] - target_volume)
    # h_tot = (h1 + h2) / 2
    h_weg_avg = (h1 + 2*h2)
    return h_weg_avg


# A* algorithm implementation
def a_star(start_volumes, capacities, target_volume):
    """ Runs A* search algorithm
        Args:
          start_volumes (list) 
    """
    start_state = State(start_volumes)
    start_state.h = heuristic(start_state, target_volume)
    start_state.f = start_state.g + start_state.h
    
    # Initializing the heap with the `start_state`
    heap = [start_state]
    heapq.heapify(heap)
    visited = []
    visited_str = []

    
    MAX_V = 10 ** 4
    while heap and len(visited) < MAX_V:
        
        # if len(visited) % 10000 == 0:
        #     print(f"{len(visited)} visites states")
        
        """
        Terminate conditions:
            maximum number of iterations or a maximum depth
            available computation resourches
        """
        
#         if len(visited) % 1000 == 0:
#             print(len(visited), end=", ")

        state = heapq.heappop(heap)
        visited.append(state)
        visited_str.append(str(state))
        if state == target_volume:
            return (state.g, state, visited)

        next_states = get_next_states(state, capacities)
        
        # Generating next states and adding them to the heap
        for next_state in next_states:

            next_state.g = state.g + 1
            next_state.h = heuristic(next_state, target_volume)
            next_state.f = next_state.g + next_state.h
            next_state._prev = state

            # checking if we come accross to the same state
                # and if its A* score is less than previous one
                    # then we add it
            if (str(next_state) in visited_str):
                if next_state.f < visited[visited_str.index(str(next_state))].f:
                    heapq.heappush(heap, next_state)
                else:
                    continue
            else:
                heapq.heappush(heap, next_state)

    return (-1, state, visited)
            
def txt_parser(filename=None):
    if filename is None:
        raise ValueError("No file name given")
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
    pitcher_capacities = [int(cap.strip()) for cap in lines[0].split(",")]
    pitcher_capacities.insert(0, np.inf)
    start_volumes = [0 for _ in range(len(pitcher_capacities))]
    target_volume = int(lines[1])

    return (pitcher_capacities, start_volumes, target_volume)

def print_path(result_state):
    """Function to show the path to the goal state"""
    print("\n")
    print(repr(result_state))
    prev = True
    while prev:
        try:
            if repr(result_state._prev) is not None:
                print(repr(result_state._prev))
                result_state = result_state._prev
        except AttributeError:
            prev = False

def main():
    # grabbing filename
    filename = sys.argv[1]

    # getting pitcher volumes and target amount
    pitcher_capacities, start_volumes, target_volume = txt_parser(filename)
    print(f"\nCapacities: {pitcher_capacities}")
    print(f"Target: {target_volume}")


    # run
    res, result_state, visited = a_star(start_volumes, pitcher_capacities, target_volume)
    
    if res != -1:
        print_path(result_state)
        # print("\n", len(visited), "state visited")
        print(f"\nOutput: {res}\n")
    else:
        print(-1)

    # print_path(result_state)
    # print_path(len(visited))

if __name__ == "__main__":
    main()
