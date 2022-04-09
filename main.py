
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

if __name__ == "__main__":
  print("hello!")
  cfg = read_config_from_cli()
  # print(cfg)

