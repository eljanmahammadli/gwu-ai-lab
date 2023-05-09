# Fruit Sorting Puzzle Solver
This is a Python implementation of an A* search algorithm to solve the Fruit Sorting problem.

The puzzle consists of a 3x10 grid of fruits with 3 different fruit types and each with 10 different sizes. The aim of the puzzle is to sort the fruits in row in ascending order of size.

The implementation uses a heuristic function h to estimate the distance to the goal state, and a cost function g to keep track of the distance traveled so far. The A* search algorithm is used to find the optimal solution by minimizing the sum of h and g.

## Usage
The program can be executed from the command line using the following command:
```
python fruit_sorting_puzzle.py
```


## Approach

The A* search algorithm is an informed search algorithm that evaluates the search space using a heuristic function. The algorithm maintains a priority queue of states to explore based on the cost function, which is the sum of the actual cost of reaching a state and an estimated cost of reaching the goal state. The heuristic function used in this code estimates the number of misplaced fruits, which is a measure of how far the current state is from the goal state.

## Heuristics

The heuristic used in this code is admissible, meaning that it never overestimates the actual cost of reaching the goal state. The heuristic is defined as the sum of the number of misplaced fruits in each row. A misplaced fruit is a fruit that is not in ascending order of size, or a fruit that is not grouped together with other fruits of the same type in the same row.

The heuristic is admissible because it counts the minimum number of moves required to reach the goal state, which is to sort each row in ascending order of size and group all fruits of the same type together in a row. The heuristic is also consistent, meaning that the estimated cost of reaching a successor state is less than or equal to the actual cost of reaching the successor state plus the estimated cost of reaching the goal state.

In summary, the A* search algorithm used in this code applies a consistent and admissible heuristic to explore the search space efficiently and find the optimal solution.






