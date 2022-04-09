from collections import defaultdict
from functools import cmp_to_key, reduce
from typing import List, Tuple
from lib.file import DeserializedFile, filter_out_unusable_keys

from lib.node import Node, generate_successors, get_path_until_root, is_goal_state, serialize_path

# TODO: `h` functions

# Ensure `open` is sorted: asc by `f` and if `f1 == f2`, desc by `g`
def openComparator(node1: Node, node2: Node):
  if node1.f < node2.f:
    return -1
  
  if node1.f > node2.f:
    return 1
  
  if node1.f == node2.f:
    return -1 if node1.cost < node2.cost else 1

def a_star(start_node: Node, file: DeserializedFile, h_func):
  open: List[Node] = []
  open_dict = defaultdict()

  expanded_nodes = defaultdict()

  open.append(start_node)
  open_dict[start_node.get_state_as_str()] = start_node

  while len(open):
    crt_node = open.pop(0)
    open_dict[start_node.get_state_as_str()] = None

    if is_goal_state(crt_node):
      # TODO: print cost
      path = get_path_until_root(crt_node)
      print("cost: {}\n".format(crt_node.cost))
      print(serialize_path(path), '\n\n')
      continue

    # Marking the current node as `closed`.
    expanded_nodes[crt_node.get_state_as_str()] = True

    # if crt_node.applied_key != None:
    #   crt_node.applied_key.attempts -= 1

    # file.keys = filter_out_unusable_keys(file.keys)

    is_open_modified = False
    for successor in generate_successors(crt_node, file.keys, file.unfair_key):

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
def v1_heuristic(node: Node, _):
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

def non_admissible_heuristic(node: Node, _):
  return reduce(lambda sum, keyhole_state: sum + keyhole_state, node.state)