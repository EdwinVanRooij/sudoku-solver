# -*- coding: utf-8 -*-

class SudokuTable:
  """Represents the complete 'physical' Sudoku table."""

  def __init__(self, rows: list):
    """Rows contains 9 SudokuRows."""
    self.rows = rows