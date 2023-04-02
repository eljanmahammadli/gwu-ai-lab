import heapq


class Territory:

  def __init__(self, name, neighbors):
    self.name = name
    self.neighbors = neighbors
    self.color = None
    self.domains = []
    self.n_neigh = len(self.neighbors)
    self.n_dom = len(self.domains)

  def __lt__(self, other):
    if self.n_dom == other.n_dom:
      return self.n_neigh > other.n_neigh
    return self.n_dom < other.n_dom

  def __repr__(self):
    return f"Territory(name='{self.name}', color='{self.color}', neighbors={self.neighbors}), domains={self.domains}"


class Arc:

  def __init__(self, tail, head):
    self.tail = tail
    self.head = head
    self.comp = 0

  def __repr__(self):
    return f"Arc(tail={self.tail}, head={self.head})"

  def __lt__(self, other):
    return self.comp < other.comp


class MapColoring:

  def __init__(self, variables, domains, constraints):
    self.variables = variables
    self.domains = domains
    self.constraints = constraints
    self.territories = {k: Territory(k, v) for k, v in self.constraints.items()}
    for ter in self.territories.values():
      ter.domains = domains.copy()

  def backtracking_search(self):
    return self.backtrack()

  def backtrack(self):

    if self.is_complete():
      assignment = {ter.name: ter.color for ter in self.territories.values()}
      return assignment

    var = self.select_unassigned_variable()
    for val in var.domains:
      # if self.is_consistent(var, val):
      # if forward checking is used, no need to consistency check
      self.territories[var.name].color = val
      self.forward_checking(var, val)
      self.ac_3()

      result = self.backtrack()
      if result is not None:
        return result

      # if consistency is violated
      print("consistency is violated")
      self.territories[var.name].color = None
    return None

  def select_unassigned_variable(self):
    heap = list(ter for ter in self.territories.values() if ter.color is None)
    heapq.heapify(heap)
    var = heapq.heappop(heap)
    return var

  def is_complete(self):
    assignment_list = [True for ter in self.territories.values() if ter.color is not None]
    if sum(assignment_list) == len(self.variables):
      return True
    return False

  def is_consistent(self, var, val):
    for n in var.neighbors:
      neigh = self.territories[n]
      if neigh.color is not None and neigh.color == val:
        return False
    return True

  def forward_checking(self, var, val):
    for neigh in self.constraints.get(var.name):
      try:
        self.territories[neigh].domains.remove(val)
      except ValueError:
        pass

  def ac_3(self):
    heap = []
    for k,v in constraints.items():
      for n in v:
        if (self.territories[k].color is None) and (self.territories[n].color is None):
          arc = Arc(k, n)
          heap.append(arc)

    while heap:
      arc = heapq.heappop(heap)
      if self.remove_inconsistent_values(arc):
        for n in self.territories[arc.tail].neighbors:
          new_arc = Arc(n, arc.tail)
          if str(new_arc) not in [str(a) for a in heap]:
            heapq.heappush(heap, new_arc)

  def remove_inconsistent_values(self, arc):
    removed = False
    for val in self.territories[arc.tail].domains:
      if len([v for v in self.territories[arc.head].domains if v != val]) == 0:
        self.territories[arc.tail].domains.remove(val)
        removed = True
    return removed


variables = ('WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T')
domains = ['Red', 'Green', 'Blue']
constraints = {
    "WA" : ("SA", "NT"),
    "NT" : ("WA", "SA", "Q"),
    "SA" : ("WA", "NT", "Q", "NSW", "V"),
    "Q"  : ("NT", "SA", "NSW"),
    "NSW": ("SA", "Q", "V"),
    "V"  : ("SA", "NSW"),
    "T"  : ()
}

mc = MapColoring(variables, domains, constraints)
result = mc.backtracking_search()
print(result)

