class Statistic:
  def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
      self.name = name
      self.value = value
      self.description = description
      self.min_value = min_value
      self.max_value = max_value

  def __str__(self):
      return f"{self.name}: {self.value}"

  def modify(self, amount: int):
      self.value = max(self.min_value, min(self.max_value, self.value + amount))