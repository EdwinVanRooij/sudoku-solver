# -*- coding: utf-8 -*-

class SudokuRow:
  """Represents a single row in the Sudoku table."""

  def __init__(self, numbers: list):
    """Numbers contains 9 integer/null values."""
    self.numbers = numbers