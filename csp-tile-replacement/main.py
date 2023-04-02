import sys
from copy import deepcopy
import heapq
import pprint
import numpy as np

TILE_LEN = 4

def load_landscape(problem):
  """Function to load landscape and constraints
     
    Args:
      problem (str): path or name of the txt file

    Returns:
      landscape (np.array): 3 dimensional array (x, d, d) where x is the number of variables.
        It can be calculated by dividing the area of the landscape by area of (TILE_LEN*TILE_LEN)
      constraints (dict): targets and the number of tiles that can be used
  """
  with open (problem) as f:
    content = ''.join([line for line in f])
    
  landscape_str = content.split('#')[2].strip().split('\n')[1:]

  landscape_arr = []
  for i in range(len(landscape_str)):
    row = list(landscape_str[i])[::2]
    row = [int(i) if i != ' ' else np.nan for i in row]
    landscape_arr.append(row)

  landscape_arr = np.array(landscape_arr)

  tile_counts = [int(i.split('=')[-1]) for i in content.split('#')[3].split('\n')[1][1:-1].split(',')]
  
  targets = {int(i.split(":")[0]): int(i.split(":")[1]) for i in content.split('#')[4].strip().split('\n')[1:]}

  tile_constraints = {
    'FULL_BLOCK': tile_counts[2],
    'OUTER_BOUNDARY': tile_counts[0],
    'EL_SHAPE': tile_counts[1]
  }

  landscape = landscape_arr \
    .reshape(-1, TILE_LEN, landscape_arr.shape[1] // TILE_LEN, TILE_LEN) \
    .transpose(0, 2, 1, 3) \
    .reshape(-1, TILE_LEN, TILE_LEN)

  constraints = {
    "tile_counts": tile_constraints,
    "targets": targets
  }
  
  return (landscape, constraints)


class Tile:
  """Represents tile objects"""
  def __init__(self, identity):
    self.identity = identity
    
  def cover(self, i, j):
    """covers the (TILE_LEN, TILE_LEN) are with the given tile shape"""
    if self.identity == 'FULL_BLOCK':
      return True
    
    if self.identity == 'OUTER_BOUNDARY':
      if (i == 0 or i == TILE_LEN-1) or (j == 0 or j == TILE_LEN-1):
        return True
    
    if self.identity == 'EL_SHAPE':
      if (i == 0 or j == 0):
        return True
      
  def __repr__(self):
    return f'Tile(identity={self.identity})'
  

class Bush:
  """Represents (TILE_LEN, TILE_LEN) area. It is also considered as variable"""
  def __init__(self, identity, values, targets=None):
    self.identity = identity
    self.values = values
    self._backup = deepcopy(values)
    self.tile = None
    self.domain = []
  
  def place_tile(self, tile_id):
    """Place tile on the area"""
    self.tile = Tile(tile_id)
    for i in range(TILE_LEN):
      for j in range(TILE_LEN):
        if self.tile.cover(i, j):
          self.values[i][j] = np.nan
          
  def unassign(self):
    """Unassign the variable and restore bush numbers"""
    self.values = deepcopy(self._backup)
    self.tile = None
          
  def __lt__(self, other):
    return self.identity < other.identity
  
  def __repr__(self):
    return f'Bush(identity={self.identity}, tile={self.tile})'
  

class Arc:

  def __init__(self, tail, head):
    self.tail = tail
    self.head = head
    self.comp = 0
    
  def __repr__(self):
    return f"Arc(tail={self.tail}, head={self.head})"

  def __lt__(self, other):
    return self.comp < other.comp
  

class TilePlacementProblem:
  """CSP algorithm to find the solution
  
  """
  def __init__(self, landscape, constraints):
    self.landscape = landscape.copy()
    self.tile_counts = constraints['tile_counts']
    self.targets = constraints['targets']
    self.bushes = {k: Bush(k, v, self.targets) for k, v in enumerate(landscape)}
    self.counter = 0
    for bush_id in self.bushes.keys():
      self.bushes[bush_id].domain = ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']
    #   self.bushes[bush_id].domain = list(self.tile_counts.keys())
    
  def backtracking_search(self):
    return self.backtrack()
  
  def backtrack(self):
    self.counter += 1
    # if self.counter % 1000 == 0:
    #   print(self.counter, end=", ")
    
    if self.is_complete() is None:
      return None
    
    if self.is_complete():
      assignment = {k: v.tile for k, v in self.bushes.items()}
      return assignment
    
    var = self.select_unassigned_var()
    for tile_id in self.bushes[var].domain:
      if self.is_consistent(var, tile_id):
        self.bushes[var].place_tile(tile_id)
        self.tile_counts[tile_id] -= 1
        # self.forward_checking()
        # self.ac_3()

        result = self.backtrack()
        if result is not None:
          return result

      # unassign variable
        self.bushes[var].unassign()
        self.tile_counts[tile_id] += 1
        self.set_bush_domains()

    
    return None
  
  def is_complete(self):
    """If all the variables are assigned and count of bush types are satisfied,
         it returns True, otherwise None or False
    """
    assignment = [True for bush in self.bushes.values() if bush.tile is not None]
    if len(assignment) != self.landscape.shape[0]:
      return False
    
    land = np.array([a.values for a in self.bushes.values()])
    counts = np.unique(land, return_counts=True)[1]
    if (counts[0] == self.targets[1]) \
      and (counts[1] == self.targets[2]) \
      and (counts[2] == self.targets[3]) \
      and (counts[3] == self.targets[4]):
      return True
    # if all variables have been assigned but targets does not satisfy return None to unassign and continue
    return None
  
  def select_unassigned_var(self):
    """Selects unassigned variable"""
    heap = list(bush for bush in self.bushes.values() if bush.tile is None)
    heapq.heapify(heap)
    var = heapq.heappop(heap)
    return var.identity
  
  def is_consistent(self, var, tile_id):
    """Returns True if there is availabe tile left and 
         if the assignment does not cause inconsistency to the target count of bush types
    """
    # if there is no available tile left
    if self.tile_counts[tile_id] == 0:
      return False
    
    bushes = deepcopy(self.bushes)
    bushes[var].place_tile(tile_id)
    land = np.array([a.values for a in bushes.values()])
    counts = np.unique(land, return_counts=True)[1]
    
    # number of bushes should not be less than target
    if self.inconsistent_bush_counts(counts):
      return False
    return True
      
  def forward_checking(self):
    exp_tiles = [k for k, v in self.tile_counts.items() if v == 0]
    unasg_tiles = list(bush for bush in self.bushes.values() if bush.tile is None)
    
    for bush in unasg_tiles:
        
      for tile in bush.domain:
        if tile in exp_tiles:
          self.bushes[bush.identity].domain.remove(tile)
          continue
        bushes = deepcopy(self.bushes)
        bushes[bush.identity].place_tile(tile)
        land = np.array([a.values for a in bushes.values()])
        counts = np.unique(land, return_counts=True)[1]
        if self.inconsistent_bush_counts(counts):
        #   print(f"removed {tile} from {bush}")
          self.bushes[bush.identity].domain.remove(tile)

  def set_bush_domains(self):
    """Restores domain of the variables"""
    for bush_id in self.bushes.keys():
      self.bushes[bush_id].domain = ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE']

  def inconsistent_bush_counts(self, counts):
    """If there is any consistency about target counts"""
    if (counts[0] < self.targets[1]) \
      or (counts[1] < self.targets[2]) \
      or (counts[2] < self.targets[3]) \
      or counts[3] < self.targets[4]:
      return True
    return False
  
  def ac_3(self):
    heap = []
    for head in self.bushes.values():
      for tail in self.bushes.values():
        # tail  is assigned and head  is unassigned
        if (tail.tile is not None) and (head.tile is None) and (head.identity != tail.identity):
          arc = Arc(tail, head)
          heap.append(arc)
          
    while heap:
      arc = heapq.heappop(heap)
      if self.remove_inconsistent_values(arc):
        for n in self.bushes.values():
          if n.identity != arc.tail.identity:
            new_arc = Arc(n, arc.tail)
            if str(new_arc) not in [str(a) for a in heap]:
              heapq.heappush(heap, new_arc)
      
      
  def remove_inconsistent_values(self, arc):
    """
      Given tail, it checks domain of head and if there is at least one domain which
      makes bush counts inconsistents it returns True
    """
    bushes = deepcopy(self.bushes)
    bushes[arc.tail.identity].place_tile(arc.tail.tile)
    for dom in arc.head.domain:
      bushes[arc.head.identity].place_tile(dom)
      land = np.array([a.values for a in bushes.values()])
      counts = np.unique(land, return_counts=True)[1]
      if (counts[0] < self.targets[1]) \
        or (counts[1] < self.targets[2]) \
        or (counts[2] < self.targets[3]) \
        or counts[3] < self.targets[4]:
        
        return True
      bushes[arc.head.identity].unassign()
      
    return False


def main():
  filename = sys.argv[1]
  # 'problems/tilesproblem_01.txt'
  landscape, constraints = load_landscape(filename)
  tpp = TilePlacementProblem(landscape, constraints)
  result = tpp.backtracking_search()
  print('\n\n', tpp.counter)
  print(pprint.pformat(result))


if __name__ == "__main__":
    main()

