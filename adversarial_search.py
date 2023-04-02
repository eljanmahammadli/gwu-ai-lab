import math
import random
from time import perf_counter


class Node:

  def __init__(self, value=None, depth=None, spec=None):
    self.value = value
    self.depth = depth
    self.spec = spec
    self._successors = []

  def __repr__(self):
    return f"Node(value={self.value}, depth={self.depth}, spec={self.spec})"


class MiniMax:

  def __init__(self, branch_factor=None, term_nodes=None, expmax=False):
    self.branch_factor = branch_factor
    self.term_nodes = list(reversed(term_nodes))
    # depth grows exponentially w.r.t branch factor
    self.tree_depth = int(math.log(len(term_nodes), branch_factor)) + 1
    self.expmax = expmax

  def build_tree(self, temp_depth=0):
    if temp_depth == self.tree_depth:
      return None

    if temp_depth % 2 == 0:
      spec = 'Max'
    else:
      spec = 'Min' if self.expmax == False else 'Expmax'

    val = None if temp_depth != self.tree_depth-1 else self.term_nodes.pop()
    node = Node(val, temp_depth, spec)

    for i in range(self.branch_factor):
      child = self.build_tree(temp_depth+1)
      if node:
        node._successors.append(child)

    return node

  def max_value(self, node:Node):
    v = -math.inf
    for child in node._successors:
      v = max(v, self.value(child))
    return v

  def min_value(self, node:Node):
    v = math.inf
    for child in node._successors:
      v = min(v, self.value(child))
    return v

  def expectimax(self, node:Node):
    v = 0
    for child in node._successors:
      p = 1 / self.branch_factor
      v += p * self.value(child)
    return v

  def value(self, node:Node):
    if node.depth == self.tree_depth-1:
      return node.value

    if node.spec == 'Min':
      return self.min_value(node)
    if node.spec == 'Expmax':
      return self.expectimax(node)
    if node.spec == 'Max':
      return self.max_value(node)


class MiniMaxAlphaBeta(MiniMax):
  
  def __init__(self, branch_factor=None, term_nodes=None):
    MiniMax.__init__(self, branch_factor, term_nodes)
    
  def max_value(self, node:Node, alpha, beta):
    v = -math.inf
    for child in node._successors:
      v = max(v, self.value(child, alpha, beta))
      if v >= beta:
        return v
      alpha = max(alpha, v)
    return v
  
  def min_value(self, node:Node, alpha, beta):
    v = math.inf
    for child in node._successors:
      v = min(v, self.value(child, alpha, beta))
      if v <= alpha:
        return v
      beta = min(beta, v)
    return v
    
  def value(self, node:Node, alpha, beta):
    if node.depth == self.tree_depth-1:
      return node.value

    if node.spec == 'Min':
      return self.min_value(node, alpha, beta)
    if node.spec == 'Max':
      return self.max_value(node, alpha, beta)


# some test cases
random.seed(12)
tn1 = [3, 12, 8, 2, 4, 6, 14, 5, 2]
tn2 = [0, 40, 20, 30]
tn2_sq = [x**2 for x in tn2]

minimax = MiniMax(branch_factor=3, term_nodes=tn1, expmax=True)
node = minimax.build_tree()
print(minimax.value(node))

minimax = MiniMax(branch_factor=2, term_nodes=tn2_sq, expmax=True)
node = minimax.build_tree()
print(minimax.value(node))

minimax = MiniMaxAlphaBeta(branch_factor=3, term_nodes=tn1)
node = minimax.build_tree()
print(minimax.value(node, -math.inf, math.inf))


# Comparison between regular and alpha-beta pruned minimax
regular_sc = 0
alpha_beta_sc = 0

for i in range(20):

  tic = perf_counter()
  minimax = MiniMax(branch_factor=3, term_nodes=tn4)
  node = minimax.build_tree()
  minimax.value(node)
  toc1 = perf_counter() - tic
  print(f"{toc1:.5f}", end=' - ')

  tic = perf_counter()
  minimax = MiniMaxAlphaBeta(branch_factor=3, term_nodes=tn4)
  node = minimax.build_tree()
  minimax.value(node, -math.inf, math.inf)
  toc2 = perf_counter() - tic
  print(f"{toc2:.5f}", end=' - ')

  if toc2 < toc1:
    alpha_beta_sc += 1
    print("Alpha-beta pruning wins")
  else:
    regular_sc += 1
    print("Regualar minimax wins")

print(f"{regular_sc=}, {alpha_beta_sc=}")


