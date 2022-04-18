
from collections import defaultdict
import errno
import functools
import os
import signal
from time import perf_counter
from typing import List, Tuple
from lib.algorithms.astar import a_star, non_admissible_heuristic, trivial_heuristic, v1_heuristic, v2_heuristic
from lib.algorithms.dfs import dfs
from lib.algorithms.idfs import incremental_dfs
from lib.file import DeserializedFile, read_input_files
from threading import Timer

from lib.key import Key

from lib.algorithms.bfs import bfs
from lib.node import Node, generate_successors, is_goal_state

from contextlib import suppress
import asyncio
from lib.path import Path

from lib.utils.timeout import timeout

class Config:
  input_dir = ""
  output_dir = ""
  nr_solutions = 0
  timeout_ms = 0

  def __str__(self) -> str:
    return str(self.__dict__)


def read_config_from_cli() -> Config:
  cfg = Config()

  # if os.environ.get('ENV') != 'DEV':
  #   cfg.input_dir = input("Input directory: ")
  #   cfg.output_dir = input("Output directory: ")
  #   cfg.nr_solutions = int(input("Max # of solutions for each algorithm: "))
  #   cfg.timeout_ms = int(input("Timeout for each algorithm(ms): "))

  cfg.input_dir = "input"
  cfg.output_dir = "output"
  cfg.nr_solutions = 4
  cfg.timeout_ms = 2000

  return cfg

def get_lock_length(file: DeserializedFile):
  return len(file.keys[0].value)

def get_starting_node(file: DeserializedFile):
  lock_len = get_lock_length(file)
  return Node([1] * lock_len)

def run_algorithms(cfg: Config, files: List[DeserializedFile]):
  nr_seconds = cfg.timeout_ms // 1000
  @timeout(nr_seconds)
  def run_algorithm(fn):
    fn()

  start_at = None
  paths = []
  def on_path_found(path: Path):
    path.found_at = perf_counter() - start_at
    paths.append(path)

  algs = [
    ("BFS", lambda starting_node, file: lambda: bfs(starting_node, file, cfg.nr_solutions, on_path_found)),
    ("DFS", lambda starting_node, file: lambda: dfs(starting_node, file, cfg.nr_solutions, on_path_found, float('inf'))),
    ("DFI", lambda starting_node, file: lambda: incremental_dfs(starting_node, file, cfg.nr_solutions, on_path_found, 5)),
    ("A* - v1 heuristic", lambda starting_node, file: lambda: a_star(starting_node, file, v1_heuristic, on_path_found)),
    ("A* - v2 heuristic", lambda starting_node, file: lambda: a_star(starting_node, file, v2_heuristic, on_path_found)),
    ("A* - non-admissible heuristic", lambda starting_node, file: lambda: a_star(starting_node, file, non_admissible_heuristic, on_path_found)),
    ("A* - trivial heuristic", lambda starting_node, file: lambda: a_star(starting_node, file, trivial_heuristic, on_path_found)),
  ]

  output_dir = os.path.join(os.getcwd(), cfg.output_dir)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  for file in files:
    input_file_name, _ = os.path.splitext(os.path.basename(file.path))
    output_file_name = os.path.join(output_dir, input_file_name + ".out")
    output_file = open(output_file_name, "w+")
  
    for (alg_name, alg) in algs:
      paths = []

      start_at = perf_counter()

      try:
        run_algorithm(alg(get_starting_node(file), file))
      except:
        paths.append("Timeout exceeded.\n")

      output_file.write("{} - unfair key = ({}, {})\n".format(alg_name, file.unfair_key[0], file.unfair_key[1]))
      
      for p in paths:
        output_file.write(str(p) + "\n")

      output_file.write("\n" + "=" * 50 + '\n\n')

    output_file.close()

if __name__ == "__main__":
  cfg = read_config_from_cli()
  # print(cfg)

  files = read_input_files("input")
  # print(files)

  # n = Node([1,1,1])
  # k = Key("dgd", 3)
  # print(generate_successors(n, [k], (0,2)))

  # file = files[3] # c
  # file = files[2] # 0
  # file = files[1] # b
  # file = files[0] # a
  # print(file)

  # n = get_starting_node(file)

  # print(generate_successors(n, file.keys, file.unfair_key))
  # succ = generate_successors(n, file.keys, file.unfair_key)[7]
  # print(succ, '\n')
  # print(generate_successors(succ, file.keys, file.unfair_key))

  # bfs(n, file)
  # dfs(n, file)
  # incremental_dfs(n, file, 5)
  # a_star(n, file, v1_heuristic)
  # a_star(n, file, v2_heuristic)
  # a_star(n, file, non_admissible_heuristic)

  run_algorithms(cfg, files)