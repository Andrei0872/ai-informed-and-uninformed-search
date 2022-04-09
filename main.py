
import os
from typing import List, Tuple
import json

class Config:
  input_dir = ""
  output_dir = ""
  nr_solutions = 0
  timeout_ms = 0

  def __str__(self) -> str:
    return str(self.__dict__)

class Key:
  value = ""
  attempts = 0

  def __init__(self, value: str, attempts) -> None:
    self.value = value.strip()
    self.attempts = attempts

  def __str__(self) -> str:
    return str(self.__dict__)

  def __repr__(self) -> str:
    return str(self.__dict__)

class DeserializedFile:  
  path = ""
  key_attempts = 0
  # TODO(improvement): https://stackoverflow.com/questions/17493307/creating-set-of-objects-of-user-defined-class-in-python
  keys: List[Key] = []
  unfair_key: Tuple[int, int] = None

  def __init__(self, path) -> None:
    self.path = path
  
  def __str__(self) -> str:
    return str(self.__dict__)

  def __repr__(self) -> str:
    return str(self.__dict__)

class Node:
  state: List[int] = []
  parent: 'Node' = None
  cost = 0
  
  def __init__(self, state) -> None:
    self.state = state

  def __str__(self) -> str:
    return str(self.__dict__)

  def __repr__(self) -> str:
    return str(self.__dict__)

def read_config_from_cli() -> Config:
  cfg = Config()

  if os.environ.get('ENV') != 'DEV':
    cfg.input_dir = input("Input directory: ")
    cfg.output_dir = input("Output directory: ")
    cfg.nr_solutions = int(input("Max # of solutions for each algorithm: "))
    cfg.timeout_ms = int(input("Timeout for each algorithm(ms): "))

  cfg.input_dir = "input"
  cfg.output_dir = "output"
  cfg.nr_solutions = 4
  cfg.timeout_ms = 2000

  return cfg

# `raw_str`: 'a->b'
# return: (unfair_key_idx, affected_key_idx)
def deserialize_unfair_key(raw_str) -> Tuple[int, int]:
  [unfair_key, affected_key] = raw_str.split("->")

  return (int(unfair_key), int(affected_key))

def read_file(file_path):
  input_file = open(file_path, 'r')
  file = DeserializedFile(file_path)

  file.key_attempts = int(input_file.readline())
  file.unfair_key = deserialize_unfair_key(input_file.readline())
  file.keys = [Key(key_state, file.key_attempts) for key_state in input_file.readlines()]

  input_file.close()

  return file

def read_input_files(input_dir) -> List[DeserializedFile]:
  # TODO: ensure `input_dir_abs` exists
  input_dir_abs = os.path.join(os.getcwd(), input_dir)
  file_paths = [os.path.join(input_dir_abs, file) for file in os.listdir(input_dir_abs)]

  return [read_file(file_path) for file_path in file_paths]

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
    successors.append(successor)

    successor.cost += get_cost(node, k, unfair_key)

  return successors

# TODO: filter out unusable keys

def get_lock_length(file: DeserializedFile):
  return len(file.keys[0].value)

if __name__ == "__main__":
  print("hello!")
  cfg = read_config_from_cli()
  # print(cfg)

  files = read_input_files("input")
  # print(files)

  # n = Node([1,1,1])
  # k = Key("dgd", 3)
  # print(generate_successors(n, [k], (0,2)))

  file = files[0]
  # print(file)

  lock_len = get_lock_length(file)
  n = Node([1] * lock_len)
  print(generate_successors(n, file.keys, file.unfair_key))
