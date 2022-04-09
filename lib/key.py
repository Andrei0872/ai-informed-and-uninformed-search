class Key:
  value = ""
  attempts = 0

  def __init__(self, value: str, attempts) -> None:
    self.value = value.strip()
    self.attempts = attempts

  def __str__(self) -> str:
    return str(self.__dict__)

  def __repr__(self) -> str:
    return str(self.__dict__)
