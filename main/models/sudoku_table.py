# -*- coding: utf-8 -*-

class SudokuTable:
  """Represents the complete 'physical' Sudoku table."""

  """"""
  def __init__(self, ordered_list: str, location: str):
    self.text = text
    self.location = location

  def __str__(self) -> str:
      return f"{self.text} ({self.location})"