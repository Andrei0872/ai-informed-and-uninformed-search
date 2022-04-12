from typing import List, Tuple

from lib.key import Key
from lib.node import Node

class Path:
  value: List[Tuple[Node, Key]]
  found_at: int
  max_nr_nodes_in_memory: int
  total_computed_successors: int
  path_idx: int

  def __init__(self, path_idx, value, max_nr_nodes_in_memory, total_computed_successors) -> None:
    self.path_idx = path_idx
    self.value = value
    self.max_nr_nodes_in_memory = max_nr_nodes_in_memory
    self.total_computed_successors = total_computed_successors

  def __str__(self) -> str:
    res = "Index: {}\n".format(self.path_idx)
    res += "Length: {}\n".format(self.length)
    res += "Cost: {}\n".format(self.cost)
    res += "Found at: {}\n".format(self.found_at)
    res += "Max nr. of nodes in memory: {}\n".format(self.max_nr_nodes_in_memory)
    res += "Total nr. of computed successors: {}\n".format(self.total_computed_successors)
    res += "The path: \n"

    for i in range(len(self.value) - 1, -1, -1):
      (parent, applied_key) = self.value[i]

      if applied_key != None:
        res += "\t" + applied_key.value + "\n"

      res += "\t" + parent.get_state_as_str() + "\n"

    return res

  @property
  def cost(self):
    return self.value[0][0].cost

  @property
  def length(self):
    return len(self.value)