from collections import defaultdict
from lib.file import DeserializedFile, filter_out_unusable_keys
from lib.node import Node, generate_successors, get_path_until_root, is_goal_state, serialize_path

from queue import Queue

def bfs(node: Node, file: DeserializedFile) -> str:
  visited = defaultdict()
  queue = Queue()

  queue.put(node)

  res = ""
  while queue.empty() == False:
    crt_node = queue.get()
    visited[crt_node.get_state_as_str()] = True

    if crt_node.applied_key != None:
      crt_node.applied_key.attempts -= 1

    file.keys = filter_out_unusable_keys(file.keys)

    if is_goal_state(crt_node):
      path = get_path_until_root(crt_node)
      print(serialize_path(path), '\n\n')
      res += serialize_path(path) + "\n\n"
      continue

    for successor in generate_successors(crt_node, file.keys, file.unfair_key):
      if visited.get(successor.get_state_as_str()) == True:
        continue

      queue.put(successor)

  return res