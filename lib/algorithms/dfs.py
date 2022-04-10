
from lib.file import DeserializedFile, filter_out_unusable_keys
from lib.node import Node, generate_successors, get_path_until_root, is_goal_state, serialize_path

from queue import LifoQueue

def dfs(node: Node, file: DeserializedFile, max_depth = float('inf')) -> str:
  stack = LifoQueue()

  stack.put((node, 0))

  res = ""
  while stack.empty() == False:
    (crt_node, depth) = stack.get()

    if crt_node.applied_key != None:
      crt_node.used_keys[crt_node.applied_key.value] += 1

      if crt_node.used_keys[crt_node.applied_key.value] > file.key_attempts:
        continue

    if is_goal_state(crt_node):
      path = get_path_until_root(crt_node)
      print("cost: {}\n".format(crt_node.cost))
      print(serialize_path(path), '\n\n')
      res += serialize_path(path) + "\n\n"
      continue

    if depth == max_depth:
      continue

    for successor in generate_successors(crt_node, file.keys, file.unfair_key):
      stack.put((successor, depth + 1))

  return res