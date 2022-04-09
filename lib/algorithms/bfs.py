from lib.file import DeserializedFile, filter_out_unusable_keys
from lib.node import Node, generate_successors, get_path_until_root, is_goal_state, serialize_path

from queue import Queue

def bfs(node: Node, file: DeserializedFile) -> str:
  queue = Queue()

  queue.put(node)

  res = ""
  while queue.empty() == False:
    crt_node = queue.get()

    if crt_node.applied_key != None:
      crt_node.used_keys[crt_node.applied_key.value] += 1

      if crt_node.used_keys[crt_node.applied_key.value] > 3:
        continue

    if is_goal_state(crt_node):
      path = get_path_until_root(crt_node)
      print("cost: {}\n".format(crt_node.cost))
      print(serialize_path(path), '\n\n')
      res += serialize_path(path) + "\n\n"
      continue

    for successor in generate_successors(crt_node, file.keys, file.unfair_key):
      queue.put(successor)

  return res