from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key, reduce
from typing import List, Tuple
from lib.file import DeserializedFile, filter_out_unusable_keys

from lib.node import Node, generate_successors, get_path_until_root, is_goal_state
from lib.path import Path

# Ensure `open` is sorted: asc by `f` and if `f1 == f2`, desc by `g`.
def openComparator(node1: Node, node2: Node):
  if node1.f < node2.f:
    return -1
  
  if node1.f > node2.f:
    return 1
  
  if node1.f == node2.f:
    return -1 if node1.cost > node2.cost else 1

def a_star(start_node: Node, file: DeserializedFile, h_func, on_path_found):
  open: List[Node] = []
  open_dict = defaultdict()

  expanded_nodes = defaultdict()

  open.append(start_node)
  open_dict[start_node.get_state_as_str()] = start_node

  max_nr_nodes_in_memory = -1
  total_computed_successors = 0

  while len(open):
    max_nr_nodes_in_memory = max(max_nr_nodes_in_memory, len(open))

    crt_node = open.pop(0)
    open_dict[start_node.get_state_as_str()] = None

    if is_goal_state(crt_node):
      path = get_path_until_root(crt_node)
      on_path_found(Path(0, path, max_nr_nodes_in_memory, total_computed_successors))
      return

    # Marking the current node as `closed`.
    expanded_nodes[crt_node.get_state_as_str()] = True

    if crt_node.applied_key != None:
      crt_node.used_keys[crt_node.applied_key.value] += 1

      if crt_node.used_keys[crt_node.applied_key.value] > file.key_attempts:
        continue

    is_open_modified = False
    successors = generate_successors(crt_node, file.keys, file.unfair_key)
    total_computed_successors += len(successors)
    for successor in successors:

      g = successor.cost
      h = h_func(successor, file.unfair_key)
      next_f = g + h

      node_in_open = open_dict.get(successor.get_state_as_str())
      if node_in_open != None:
        # Part of `open`.
        if next_f < node_in_open.f:
          node_in_open.f = next_f
          node_in_open.cost = successor.cost
          node_in_open.applied_key = successor.applied_key
          node_in_open.parent = successor.parent

          is_open_modified = True
      elif expanded_nodes.get(successor.get_state_as_str()) == True:
        # Part of `closed``.
        if next_f < successor.f:
          expanded_nodes[successor.get_state_as_str()] = False
          successor.f = next_f

          open.append(successor)
          open_dict[successor.get_state_as_str()] = successor

          is_open_modified = True
      else:
        # First time the node is taken into account.
        if next_f < successor.f:
          successor.f = next_f

          open.append(successor)
          open_dict[successor.get_state_as_str()] = successor

          is_open_modified = True

    if is_open_modified == False:
      continue
    
    # Sort ONLY if the list has been modified.
    open = sorted(open, key=cmp_to_key(openComparator))

def trivial_heuristic(node: Node, _):
  return 0 if is_goal_state(node) else 1

# Number of keyholes that are still locked(i.e. `keyhole_state > 0`).
def non_admissible_heuristic(node: Node, _):
  return reduce(lambda nr_locked, keyhole_state: nr_locked + (1 if keyhole_state > 0 else 0), node.state, 0)

def v2_heuristic(node: Node, unfair_key: Tuple[int, int]):
  (guilty_idx, _) = unfair_key

  res = 0
  for i in range(0, len(node.state)):
    keyhole_state = node.state[i]

    if i == guilty_idx:
      res += 2 * keyhole_state
    else:
      res += keyhole_state

  return res

def v1_heuristic(node: Node, _):
  return reduce(lambda sum, keyhole_state: sum + keyhole_state, node.state)