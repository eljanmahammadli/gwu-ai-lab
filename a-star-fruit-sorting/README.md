# Fruit Sorting Puzzle Solver
This is a Python implementation of an A* search algorithm to solve the Fruit Sorting problem.

The puzzle consists of a 3x10 grid of fruits with 3 different fruit types and each with 10 different sizes. The aim of the puzzle is to sort the fruits in row in ascending order of size. And each row should be consisting of only one type of fruit (this offers us 6 different goal state since there are 3 rows).

The implementation uses a heuristic function h to estimate the distance to the goal state, and a cost function g to keep track of the distance traveled so far. The A* search algorithm is used to find the optimal solution by minimizing the sum of h and g.

## Usage
The program can be executed from the command line using the following command:
```
python fruit_sorting_puzzle.py
```

Below is example input state:
```
state = ((('banana', 4),
  ('orange', 7),
  ('apple', 3),
  ('apple', 4),
  ('orange', 9),
  ('apple', 6),
  ('orange', 5),
  ('apple', 8),
  ('apple', 9),
  ('apple', 10)),
 (('orange', 1),
  ('banana', 1),
  ('orange', 3),
  ('orange', 4),
  ('apple', 7),
  ('orange', 6),
  ('apple', 2),
  ('orange', 8),
  ('apple', 5),
  ('orange', 10)),
 (('orange', 2),
  ('banana', 2),
  ('banana', 3),
  ('apple', 1),
  ('banana', 5),
  ('banana', 6),
  ('banana', 7),
  ('banana', 8),
  ('banana', 9),
  ('banana', 10)))
```

After running the code it will return the solution below:
```
result_state = ((('apple', 1),
  ('apple', 2),
  ('apple', 3),
  ('apple', 4),
  ('apple', 5),
  ('apple', 6),
  ('apple', 7),
  ('apple', 8),
  ('apple', 9),
  ('apple', 10)),
 (('orange', 1),
  ('orange', 2),
  ('orange', 3),
  ('orange', 4),
  ('orange', 5),
  ('orange', 6),
  ('orange', 7),
  ('orange', 8),
  ('orange', 9),
  ('orange', 10)),
 (('banana', 1),
  ('banana', 2),
  ('banana', 3),
  ('banana', 4),
  ('banana', 5),
  ('banana', 6),
  ('banana', 7),
  ('banana', 8),
  ('banana', 9),
  ('banana', 10)))
```


## Approach

The A* search algorithm is an informed search algorithm that evaluates the search space using a heuristic function. The algorithm maintains a priority queue of states to explore based on the cost function, which is the sum of the actual cost of reaching a state and an estimated cost of reaching the goal state. The heuristic function used in this code estimates the number of misplaced fruits, which is a measure of how far the current state is from the goal state.

## Heuristics

The heuristic used in this code is admissible, meaning that it never overestimates the actual cost of reaching the goal state. The heuristic is defined as the minimum of the 6 different manhattan distance  divided bt 2 (because of the swaps) between state and the goal state. This is because there are 6 possible goal states since there are 3 rows. The implementation also uses some optimization so that the swaps are all calculated and store once and before the algorithm. Another optimization is to store the index of the fruits (tuples) of all the possible goal state in a hash so to not to search them again.

The heuristic is admissible because it counts the minimum number of moves required to reach the goal state, which is to sort each row in ascending order of size and group all fruits of the same type together in a row. The heuristic is also consistent, meaning that the estimated cost of reaching a successor state is less than or equal to the actual cost of reaching the successor state plus the estimated cost of reaching the goal state.

In summary, the A* search algorithm used in this code applies a consistent and admissible heuristic to explore the search space efficiently and find the optimal solution.






