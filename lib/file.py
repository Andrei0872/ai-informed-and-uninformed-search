import os
from typing import List, Tuple

from lib.key import Key

class DeserializedFile:  
  path = ""
  key_attempts = 0
  # TODO(improvement): https://stackoverflow.com/questions/17493307/creating-set-of-objects-of-user-defined-class-in-python
  keys: List[Key] = []
  unfair_key: Tuple[int, int] = None

  def __init__(self, path) -> None:
    self.path = path
  
  def __str__(self) -> str:
    return str(self.__dict__)

  def __repr__(self) -> str:
    return str(self.__dict__)

# `raw_str`: 'a->b'
# return: (unfair_key_idx, affected_key_idx)
def deserialize_unfair_key(raw_str) -> Tuple[int, int]:
  [unfair_key, affected_key] = raw_str.split("->")

  return (int(unfair_key), int(affected_key))

def read_file(file_path):
  input_file = open(file_path, 'r')
  file = DeserializedFile(file_path)

  file.key_attempts = int(input_file.readline())
  file.unfair_key = deserialize_unfair_key(input_file.readline())
  file.keys = [Key(key_state, file.key_attempts) for key_state in input_file.readlines()]

  input_file.close()

  return file

def read_input_files(input_dir) -> List[DeserializedFile]:
  # TODO: ensure `input_dir_abs` exists
  input_dir_abs = os.path.join(os.getcwd(), input_dir)
  file_paths = [os.path.join(input_dir_abs, file) for file in os.listdir(input_dir_abs)]

  return [read_file(file_path) for file_path in file_paths]

def filter_out_unusable_keys(keys: List[Key]) -> List[Key]:
  return list(filter(lambda k: k.attempts > 0, keys))