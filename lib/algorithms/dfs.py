
from collections import defaultdict
from lib.file import DeserializedFile, filter_out_unusable_keys
from lib.node import Node, generate_successors, get_path_until_root, is_goal_state, serialize_path

from queue import LifoQueue

def dfs(node: Node, file: DeserializedFile, max_depth = float('inf')) -> str:
  stack = LifoQueue()
  visited = defaultdict()

  stack.put((node, 0))

  res = ""
  while stack.empty() == False:
    (crt_node, depth) = stack.get()
    # visited[crt_node.get_state_as_str()] = True

    if crt_node.applied_key != None:
      crt_node.applied_key.attempts -= 1

      if crt_node.applied_key.attempts <= 0:
        continue

    file.keys = filter_out_unusable_keys(file.keys)

    if is_goal_state(crt_node):
      path = get_path_until_root(crt_node)
      print(serialize_path(path), '\n\n')
      res += serialize_path(path) + "\n\n"
      continue

    if depth == max_depth:
      continue

    for successor in generate_successors(crt_node, file.keys, file.unfair_key):
      # if visited.get(successor.get_state_as_str()) == True:
      #   continue

      stack.put((successor, depth + 1))

  return res

# def dfs(node: Node, file: DeserializedFile, visited) -> str:
#   visited[node.get_state_as_str()] = True

#   if node.applied_key != None:
#     node.applied_key.attempts -= 1

#   file.keys = filter_out_unusable_keys(file.keys)

#   if is_goal_state(node):
#     path = get_path_until_root(node)
#     print(serialize_path(path), '\n\n')
#     res = serialize_path(path) + "\n\n"
#     return res

#   for successor in generate_successors(node, file.keys, file.unfair_key):
#     if visited.get(successor.get_state_as_str()) == True:
#       continue
    
#     dfs(successor, file, visited)

#   if node.applied_key != None:
#     node.applied_key.attempts += 1

#   visited[node.get_state_as_str()] = False