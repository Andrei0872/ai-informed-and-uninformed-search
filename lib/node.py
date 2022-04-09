from typing import List, Tuple
from lib.key import Key
import random

class Node:
  state: List[int] = []
  parent: 'Node' = None
  cost = 0
  applied_key: Key = None

  f = float('inf')
  
  def __init__(self, state) -> None:
    self.state = state

  def __str__(self) -> str:
    return str(self.__dict__)

  def __repr__(self) -> str:
    return str(self.__dict__)

  def get_state_as_str(self):
    return "".join(map(str, self.state))

def get_cost(node: Node, key: Key, unfair_key: Tuple[int, int]):
  cost = 0
  for i in range(0, len(node.state)):
    action = key.value[i]
    keyhole_state = node.state[i]

    if action != 'd':
      continue

    if keyhole_state > 0:
      cost += 1

  (guilty_idx, affected_idx) = unfair_key
  can_guilty_keyhole_be_unlocked = node.state[guilty_idx] > 0 and key.value[guilty_idx] == 'd'
  can_affected_keyhole_be_unlocked = key.value[affected_idx] == 'd'
  if can_guilty_keyhole_be_unlocked and can_affected_keyhole_be_unlocked:
    # `can_guilty_keyhole_be_unlocked` will lead to the _affected keyhole_ to be locked once more.
    # But, if `can_affected_keyhole_be_unlocked == True`, the previous lock operation will be canceled.
    cost -= 1

  return cost

def apply_action_to_keyhole(keyhole_state: int, action: str):
  if action == 'g':
    return keyhole_state
  
  if action == 'd':
    return keyhole_state - 1 if keyhole_state > 0 else 0
  
  if action == 'i':
    return keyhole_state + 1

def apply_unfair_key_to_state(state: List[int], unfair_key: Tuple[int, int], unfair_key_action_pair: Tuple[str, str]):
  (guilty_action, affected_action) = unfair_key_action_pair
  (guilty_idx, affected_idx) = unfair_key

  can_guilty_keyhole_be_unlocked = state[guilty_idx] > 0 and guilty_action == 'd'
  if can_guilty_keyhole_be_unlocked == False:
    return
  
  state[affected_idx] += 1

def apply_key_to_node(node: Node, key: Key, unfair_key: Tuple[int, int]) -> Node:
  crt_state = node.state[:]
  
  # Why we'doing this here: after applying the key, the `guilty` keyhole can become 0
  # as a result of 2 states. For instance: the key state was **already `0`**(case in which there there is nothing to do)
  # or the key state was `1`(case in which we have to lock once more time the `affected` keyhole).
  (guilty_idx, affected_idx) = unfair_key
  apply_unfair_key_to_state(crt_state, unfair_key, (key.value[guilty_idx], key.value[affected_idx]))
  
  new_state = [apply_action_to_keyhole(crt_state[i], key.value[i]) for i in range(0, len(crt_state))]

  return Node(new_state)

def generate_successors(node: Node, keys: List[Key], unfair_key: Tuple[int, int]) -> List[Node]:
  successors = []

  for k in keys:
    successor = apply_key_to_node(node, k, unfair_key)
    successor.cost = node.cost + get_cost(node, k, unfair_key)
    successor.parent = node
    successor.applied_key = k

    successors.append(successor)

  # random.shuffle(successors)
  return successors

def is_goal_state(node: Node):
  return all(map(lambda keyhole_value: keyhole_value == 0, node.state))

def get_path_until_root(node: Node) -> List[Tuple[Node, Key]]:
  path = []

  while node:
    path.append((node, node.applied_key))

    node = node.parent

  return path

def serialize_path(path: List[Tuple[Node, Key]]) -> str:
  res = ""
  for i in range(len(path) - 1, -1, -1):
    (parent, applied_key) = path[i]

    if applied_key != None:
      res += applied_key.value + "\n"

    res += parent.get_state_as_str() + "\n"
  
  return res