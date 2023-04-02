
# A* algorithm to solve the water pitcher problem

## Introduction

The water pitcher problem is a classic problem in computer science. 
In this specific version text file is given with two lines, first for the capacities of the pitcher and second for the target amount. The goal is to measure target amount of water in the infinite pitcher. The problem can be represented as a graph where each node represents a possible state of the pitchers (i.e., how much water is in each pitcher) and each edge represents a possible pouring operation that can be performed to reach the next state.

The A* algorithm is a heuristic search algorithm that can be used to find the shortest path between two nodes in a graph. In the case of the water pitcher problem, average of two equations is used.
$$\frac{(|\sum volumes - target|) + (|infinitePitcher-target|)}{2}$$
Where $\sum volumes$ is sum of volumes across all pitchers, and $target$ is amount of water that should be filled in the $infinitePitcher$ (goal state). 

## Requirements

-   Python 3.x
-   `heapq` 
-   `numpy` 
-   `pytest`

## Usage

To run the A* algorithm on the water pitcher problem, simply run the `main.py` script with text file that contains the capacities and target volume:
`python main.py inputs/input1.txt` 

This will solve the problem and return the number of visited states and path to the problem if it exists otherwise it will output `-1`

## Testing
There are 3 test files with 11 test functions in total for several subroutines of the program. Following test cases are available:

`test_heuristic.py`
- `test_heuristic_case_1()`
- `test_heuristic_case_2()`
- `test_heuristic_case_2()`

`test_get_next_states.py`
- `test_get_next_states_case_1()`
- `test_get_next_states_case_2()`
- `test_get_next_states_case_3()`

`test_a_star.py`
- `test_a_star_case_1()`
- `test_a_star_case_2()`
- `test_a_star_case_3()`
- `test_a_star_case_4()`
- `test_a_star_case_5()`

Run `pytest` to test all the functions above.

## Implementation
In order to get all the states from the given state `get_next_states` function is used with arguments `state` and `capacities`. The A* algorithm is performed by the help of `a_star` function with `start_volumes`, `capacities`, `target_volume` input parameters. The heapq data structure is used to store states. After initializing with empty pitchers, in each step state with least `f` value is popped out of heap and checked if it is a goal state. If not, then generate next statesand add to the heap. After exploring all the states, limited number of iterations have been set if there is no path then program returns -1. Additional two functions `txt_parser` and `print_path` is used, former for parsing the input from text file and latter for printing the found path.

## Conclusion

The A* algorithm is an efficient and effective way to solve the water pitcher problem. By using a heuristic function to estimate the remaining cost to the goal state, the algorithm can quickly find the shortest path between the initial and goal states. The water pitcher problem is a good example of how the A* algorithm can be applied to real-world problems, and the implementation provided in this repository can serve as a starting point for other graph search problems.
