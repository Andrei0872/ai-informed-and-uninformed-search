from lib.algorithms.dfs import dfs
from lib.file import DeserializedFile
from lib.node import Node
from lib.path import Path

def incremental_dfs(node: Node, file: DeserializedFile, max_nr_solutions, on_path_found, max_depth):
  remaining_nr_solutions = max_nr_solutions

  def on_path_found_wrapper(path: Path):
    nonlocal remaining_nr_solutions

    path.path_idx = max_nr_solutions - remaining_nr_solutions

    remaining_nr_solutions -= 1
    on_path_found(path)

  for depth in range(0, max_depth + 1):
    dfs(node, file, remaining_nr_solutions, on_path_found_wrapper, depth)

    if remaining_nr_solutions == 0:
      return