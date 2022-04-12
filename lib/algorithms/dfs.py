
from lib.file import DeserializedFile, filter_out_unusable_keys
from lib.node import Node, generate_successors, get_path_until_root, is_goal_state

from queue import LifoQueue

from lib.path import Path

def dfs(node: Node, file: DeserializedFile, max_nr_solutions, on_path_found, max_depth = float('inf')):
  stack = LifoQueue()

  stack.put((node, 0))

  nr_solutions = 0

  max_nr_nodes_in_memory = -1
  total_computed_successors = 0

  while stack.empty() == False:
    max_nr_nodes_in_memory = max(max_nr_nodes_in_memory, stack.qsize())
    
    (crt_node, depth) = stack.get()

    if crt_node.applied_key != None:
      crt_node.used_keys[crt_node.applied_key.value] += 1

      if crt_node.used_keys[crt_node.applied_key.value] > file.key_attempts:
        continue

    if is_goal_state(crt_node):
      path = get_path_until_root(crt_node)
      path_idx = nr_solutions

      on_path_found(Path(path_idx, path, max_nr_nodes_in_memory, total_computed_successors))

      nr_solutions += 1
      if nr_solutions == max_nr_solutions:
        return

      continue

    if depth == max_depth:
      continue

    successors = generate_successors(crt_node, file.keys, file.unfair_key)
    total_computed_successors += len(successors)

    for successor in successors:
      stack.put((successor, depth + 1))