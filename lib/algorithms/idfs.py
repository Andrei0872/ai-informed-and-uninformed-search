from lib.algorithms.dfs import dfs
from lib.file import DeserializedFile
from lib.node import Node

def incremental_dfs(node: Node, file: DeserializedFile, max_depth):
  for depth in range(0, max_depth + 1):
    dfs(node, file, depth)