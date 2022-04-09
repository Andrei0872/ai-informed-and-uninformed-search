
from collections import defaultdict
import os
from typing import List, Tuple
from lib.file import DeserializedFile, read_input_files

from lib.key import Key

from lib.algorithms.bfs import bfs
from lib.node import Node, generate_successors, is_goal_state

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

def get_starting_node():
  lock_len = get_lock_length(file)
  return Node([1] * lock_len)

if __name__ == "__main__":
  cfg = read_config_from_cli()
  # print(cfg)

  files = read_input_files("input")
  # print(files)

  # n = Node([1,1,1])
  # k = Key("dgd", 3)
  # print(generate_successors(n, [k], (0,2)))

  file = files[0]
  # print(file)

  n = get_starting_node()

  # print(generate_successors(n, file.keys, file.unfair_key))
  # succ = generate_successors(n, file.keys, file.unfair_key)[7]
  # print(succ, '\n')
  # print(generate_successors(succ, file.keys, file.unfair_key))

  bfs(n, file)